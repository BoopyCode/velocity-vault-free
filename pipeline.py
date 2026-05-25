#!/usr/bin/env python3
"""
Mobile Vault - AI marketplace listing generator for phones.

Upload a phone photo and optional notes; AI prepares a ready-to-publish listing
with detected device details, category, price guidance, title, and description.
"""

import argparse
import base64
import json
import logging
import mimetypes
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv() -> bool:
        return False

try:
    from openai import OpenAI
except ModuleNotFoundError:
    OpenAI = None

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


class MobileMarketplaceAI:
    """Generate AI-assisted marketplace listings from mobile phone photos."""

    def __init__(self) -> None:
        api_key = os.getenv("MARKETPLACE_AI_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("MARKETPLACE_AI_BASE_URL", "https://api.deepseek.com/v1")

        self.model = os.getenv("MARKETPLACE_AI_MODEL", "deepseek-chat")
        self.currency = os.getenv("LISTING_CURRENCY", "EUR")
        self.language = os.getenv("LISTING_LANGUAGE", "sk")
        self.client: Optional[Any] = None

        if api_key and OpenAI:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        elif api_key:
            logger.warning("openai package is not installed; using fallback mode.")
        else:
            logger.warning("No AI API key configured; using filename-based fallback.")

    def create_listing(
        self,
        photo_path: Path,
        notes: str = "",
        output_dir: Path = Path("listings"),
    ) -> Dict[str, Any]:
        """Create a marketplace listing JSON file for a phone photo."""
        if not photo_path.exists() or not photo_path.is_file():
            raise FileNotFoundError(f"Photo not found: {photo_path}")

        listing = self._generate_with_ai(photo_path, notes) if self.client else None
        if not listing:
            listing = self._fallback_listing(photo_path, notes)

        listing["source_photo"] = str(photo_path)
        listing["generated_at"] = datetime.now().isoformat()

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{photo_path.stem}_listing.json"
        output_path.write_text(
            json.dumps(listing, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        logger.info("Listing saved to %s", output_path)
        return listing

    def _generate_with_ai(self, photo_path: Path, notes: str) -> Optional[Dict[str, Any]]:
        image_data_url = self._image_data_url(photo_path)
        prompt = self._prompt(notes)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert phone marketplace assistant. "
                            "Return only valid JSON and never invent facts that "
                            "cannot be inferred from the image or user notes."
                        ),
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_data_url},
                            },
                        ],
                    },
                ],
                temperature=0.3,
            )
            content = response.choices[0].message.content or ""
            return self._parse_json(content)
        except Exception as exc:
            logger.error("AI listing generation failed: %s", exc)
            return None

    def _prompt(self, notes: str) -> str:
        return f"""
Create a ready-to-publish marketplace listing for a mobile phone from the photo.
Use language: {self.language}. Currency: {self.currency}.

User notes:
{notes or "No extra notes provided."}

Return this JSON shape:
{{
  "title": "short listing title",
  "category": "Mobily",
  "subcategory": "Android phone | iPhone | Accessories | Unknown",
  "brand": "detected brand or Unknown",
  "model": "detected model or Unknown",
  "condition": "new | like_new | good | used | damaged | unknown",
  "detected_attributes": {{
    "storage": "if known",
    "color": "if visible",
    "battery_health": "if provided",
    "included_accessories": [],
    "visible_defects": []
  }},
  "suggested_price": {{
    "amount": 0,
    "currency": "{self.currency}",
    "confidence": "low | medium | high",
    "reason": "short pricing rationale"
  }},
  "description": "buyer-friendly description",
  "search_keywords": [],
  "seller_questions": []
}}
""".strip()

    @staticmethod
    def _image_data_url(photo_path: Path) -> str:
        mime_type = mimetypes.guess_type(photo_path)[0] or "image/jpeg"
        image_bytes = photo_path.read_bytes()
        encoded = base64.b64encode(image_bytes).decode("ascii")
        return f"data:{mime_type};base64,{encoded}"

    @staticmethod
    def _parse_json(content: str) -> Optional[Dict[str, Any]]:
        cleaned = content.strip()
        fenced = re.search(r"```(?:json)?\s*(.*?)```", cleaned, re.DOTALL)
        if fenced:
            cleaned = fenced.group(1).strip()

        try:
            parsed = json.loads(cleaned)
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError as exc:
            logger.error("AI returned invalid JSON: %s", exc)
            return None

    def _fallback_listing(self, photo_path: Path, notes: str) -> Dict[str, Any]:
        name = f"{photo_path.stem} {notes}".lower()
        brand = self._detect_brand(name)
        subcategory = "iPhone" if brand == "Apple" else "Android phone"
        if brand == "Unknown":
            subcategory = "Unknown"

        title_parts = [brand if brand != "Unknown" else "Mobilný telefón"]
        model_hint = self._detect_model_hint(name)
        if model_hint:
            title_parts.append(model_hint)

        return {
            "title": " ".join(title_parts),
            "category": "Mobily",
            "subcategory": subcategory,
            "brand": brand,
            "model": model_hint or "Unknown",
            "condition": "unknown",
            "detected_attributes": {
                "storage": self._detect_storage(name) or "Unknown",
                "color": "Unknown",
                "battery_health": "Unknown",
                "included_accessories": [],
                "visible_defects": [],
            },
            "suggested_price": {
                "amount": 0,
                "currency": self.currency,
                "confidence": "low",
                "reason": (
                    "AI API key is not configured, so price cannot be estimated "
                    "reliably from the photo."
                ),
            },
            "description": (
                "Predám mobilný telefón. Doplňte presný model, stav, kapacitu "
                "úložiska, batériu, príslušenstvo a reálne fotografie detailov."
            ),
            "search_keywords": [brand, "mobil", "smartfón"],
            "seller_questions": [
                "Aký je presný model a kapacita úložiska?",
                "Aký je stav batérie a sú na zariadení poškodenia?",
                "Je telefón odhlásený z účtov a pripravený na predaj?",
            ],
        }

    @staticmethod
    def _detect_brand(text: str) -> str:
        brands = {
            "iphone": "Apple",
            "apple": "Apple",
            "samsung": "Samsung",
            "xiaomi": "Xiaomi",
            "redmi": "Xiaomi",
            "huawei": "Huawei",
            "honor": "Honor",
            "motorola": "Motorola",
            "nokia": "Nokia",
            "oneplus": "OnePlus",
            "oppo": "Oppo",
            "realme": "Realme",
            "sony": "Sony",
            "google": "Google",
            "pixel": "Google",
        }
        for marker, brand in brands.items():
            if marker in text:
                return brand
        return "Unknown"

    @staticmethod
    def _detect_model_hint(text: str) -> str:
        patterns = [
            r"iphone\s?\d{1,2}\s?(?:pro|max|mini|plus)?",
            r"galaxy\s?s\d{1,2}\s?(?:ultra|plus|fe)?",
            r"pixel\s?\d{1,2}\s?(?:pro|a)?",
            r"redmi\s?note\s?\d{1,2}",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).title()
        return ""

    @staticmethod
    def _detect_storage(text: str) -> str:
        match = re.search(r"\b(32|64|128|256|512)\s?gb\b|\b1\s?tb\b", text, re.I)
        return match.group(0).upper().replace(" ", "") if match else ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an AI marketplace listing for a mobile phone photo."
    )
    parser.add_argument("photo", type=Path, help="Path to the uploaded phone photo")
    parser.add_argument(
        "--notes",
        default="",
        help="Optional seller notes, e.g. storage, battery health, defects",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(os.getenv("OUTPUT_DIR", "listings")),
        help="Directory where listing JSON files are saved",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    assistant = MobileMarketplaceAI()
    result = assistant.create_listing(args.photo, args.notes, args.output_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))
