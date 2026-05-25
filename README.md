# Mobile Vault - AI marketplace for phones

Mobile Vault is a Vinted-style marketplace concept focused on mobile phones.
The first working feature is an AI listing assistant: upload a phone photo,
optionally add seller notes, and get a ready-to-publish listing draft.

## What the AI prepares

- Identifies likely phone brand and model from the image and notes
- Suggests the marketplace category and subcategory
- Drafts a Slovak listing title and buyer-friendly description
- Extracts useful attributes such as storage, color, defects, accessories, and battery notes
- Suggests a price structure with confidence and rationale
- Adds search keywords and follow-up seller questions for missing details

## Setup

### Prerequisites

```bash
Python 3.10+
```

### Install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure AI

```bash
cp .env.example .env
```

Set an OpenAI-compatible API key and model in `.env`. If you use a model with
vision support, the assistant can analyze the uploaded photo directly. Without
an API key, it falls back to basic filename and note detection.

## Generate a listing

```bash
python pipeline.py ./photos/iphone_13_128gb.jpg \
  --notes "128 GB, kondícia dobrá, batéria 88 %, bez prasklín" \
  --output-dir listings
```

The command writes a JSON draft such as:

```json
{
  "title": "Apple iPhone 13",
  "category": "Mobily",
  "subcategory": "iPhone",
  "brand": "Apple",
  "model": "iPhone 13",
  "condition": "good",
  "suggested_price": {
    "amount": 450,
    "currency": "EUR",
    "confidence": "medium",
    "reason": "Estimated from model, storage, condition, and seller notes."
  },
  "description": "..."
}
```

## Environment variables

- `MARKETPLACE_AI_API_KEY` - API key for the AI provider
- `MARKETPLACE_AI_BASE_URL` - OpenAI-compatible API base URL
- `MARKETPLACE_AI_MODEL` - AI model name
- `LISTING_LANGUAGE` - Listing language, defaults to `sk`
- `LISTING_CURRENCY` - Listing currency, defaults to `EUR`
- `OUTPUT_DIR` - Default output directory for generated listing JSON files
- `LOG_LEVEL` - Python logging level

## Notes

AI output should be reviewed before publishing. Ask the seller to confirm
condition, battery health, account lock status, warranty, accessories, and any
visible defects before a listing goes live.

Fallback listings need extra review because they use only simple pattern
matching from filenames and seller notes when AI analysis is unavailable.
