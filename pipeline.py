#!/usr/bin/env python3
"""
Velocity Vault - 100% FREE AI YouTube Shorts Automation
DeepSeek + Replicate FLUX + Piper TTS + FFmpeg
Target: 100M views in 6 months
"""

import os
import json
import time
from datetime import datetime
import logging
from typing import Dict, List
from dotenv import load_dotenv
import replicate
import openai

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VelocityVaultPipeline:
    def __init__(self):
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.replicate_token = os.getenv('REPLICATE_API_TOKEN')
        self.youtube_token = os.getenv('YOUTUBE_OAUTH_TOKEN')
        self.channel_id = os.getenv('YOUTUBE_CHANNEL_ID')
        
        # Setup DeepSeek API (OpenAI-compatible)
        openai.api_key = self.deepseek_api_key
        openai.api_base = "https://api.deepseek.com/v1"
        
        # Setup Replicate
        os.environ['REPLICATE_API_TOKEN'] = self.replicate_token
    
    def generate_script(self, topic: str, pillar: str) -> Dict:
        """Generate a script using DeepSeek API (FREE)"""
        logger.info(f"Generating script for: {topic}")
        
        prompt = f"""
        Create a compelling YouTube Short script (45-60 seconds) about {topic}.
        Pillar: {pillar}
        
        Format:
        {{
            "title": "...",
            "hook": "..." (First 5-10 seconds - must grab attention),
            "body": "..." (Main content),
            "cta": "..." (Call-to-action),
            "duration": 50
        }}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            content = response['choices'][0]['message']['content']
            logger.info(f"✓ Script generated")
            return json.loads(content)
        except Exception as e:
            logger.error(f"Script generation failed: {e}")
            return {}
    
    def generate_image(self, prompt: str) -> str:
        """Generate image using Replicate FLUX (FREE Tier)"""
        logger.info(f"Generating image for: {prompt}")
        
        try:
            output = replicate.run(
                "black-forest-labs/flux-schnell",
                input={"prompt": prompt}
            )
            logger.info(f"✓ Image generated")
            return output[0] if isinstance(output, list) else output
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return None
    
    def batch_generate(self, count: int = 10):
        """Generate batch of videos"""
        logger.info(f"\n{'='*60}")
        logger.info(f"VELOCITY VAULT - AI SHORTS BATCH GENERATION")
        logger.info(f"Generating {count} Shorts...")
        logger.info(f"{'='*60}\n")
        
        topics = [
            ("The 2-Minute Rule", "psychology"),
            ("Stop Checking Your Phone", "productivity"),
            ("Motivation vs Discipline", "psychology"),
            ("Sleep = Performance", "productivity"),
            ("The 70/20/10 Money Rule", "finance"),
        ]
        
        for i in range(count):
            topic, pillar = topics[i % len(topics)]
            logger.info(f"\n[{i+1}/{count}] Processing: {topic}")
            
            # Generate script
            script = self.generate_script(topic, pillar)
            if not script:
                continue
            
            # Generate image
            image_url = self.generate_image(f"Professional thumbnail for: {topic}")
            
            # Create video metadata
            metadata = {
                "title": f"{script.get('title', topic)} | Velocity Vault",
                "description": f"{script.get('hook')}\n\n{script.get('body')}\n\n{script.get('cta')}\n\nSubscribe! 🚀 #Shorts #Motivation #AI",
                "duration": script.get('duration', 45),
                "image_url": image_url,
                "script": script,
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info(f"✓ Video {i+1} prepared for upload")
            
            # Save metadata
            with open(f"videos/video_{i+1:03d}_metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"BATCH GENERATION COMPLETE")
        logger.info(f"Generated {count} video scripts & images")
        logger.info(f"Next: Add voice-overs (Piper TTS) & compose videos (FFmpeg)")
        logger.info(f"{'='*60}\n")

if __name__ == "__main__":
    import sys
    
    pipeline = VelocityVaultPipeline()
    
    # Get count from args or default to 10
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    
    pipeline.batch_generate(count=count)
