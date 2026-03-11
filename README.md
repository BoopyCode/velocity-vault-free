# velocity-vault-free# 🚀 Velocity Vault - AI YouTube Shorts Automation

**100% FREE Stack: DeepSeek + FLUX + Piper + FFmpeg**

Automatically generate and upload engaging YouTube Shorts with AI. Target: **100M views in 6 months**.

## 📊 Project Status
- ✅ YouTube Channel Created: [Velocity Vault](https://www.youtube.com/channel/UCp3eKZhxDGwruAdId9pxgcg)
- ✅ GitHub Repository: Ready for deployment
- 🔄 AI Automation Pipeline: In development
- 🎬 Video Generation: 3-5 Shorts/day

## 🛠️ FREE Stack Components

### 1. **Script Generation - DeepSeek API (FREE)**
```python
# DeepSeek is completely free (up to reasonable limits)
pip install openai  # Using OpenAI-compatible API
```
- **API Endpoint:** https://api.deepseek.com/v1
- **Models:** `deepseek-chat` (fast & free)
- **Use:** Generate compelling Shorts scripts

### 2. **Image/Video Generation - Replicate FLUX (FREE Tier)**
```bash
pip install replicate
```
- **Model:** `black-forest-labs/flux-schnell`
- **Cost:** 1000 monthly free credits (enough for 100+ images/month)
- **Speed:** Ultra-fast generation
- **Use:** AI-generated visuals for Shorts

### 3. **Voice Synthesis - Piper TTS (100% Open Source)**
```bash
pip install piper-tts
```
- **No API keys needed**
- **Runs locally on CPU**
- **Multiple voices available**
- **Use:** Natural-sounding voice-overs

### 4. **Video Composition - FFmpeg (FREE)**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# Mac
brew install ffmpeg

# Windows
choco install ffmpeg
```
- Video editing & composition
- Audio synchronization
- Format conversion

### 5. **Upload Automation - YouTube API (FREE)**
- Unlimited uploads (requires OAuth2 setup)
- Schedule publishing
- Auto-optimize metadata

## 🔧 Installation & Setup

### Prerequisites
```bash
Python 3.10+
FFmpeg
Git
```

### 1. Clone Repository
```bash
git clone https://github.com/BoopyCode/velocity-vault-free.git
cd velocity-vault-free
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup API Keys
```bash
# Create .env file
cp .env.example .env
```

Edit `.env` with your credentials:
```
# DeepSeek (FREE - get from https://platform.deepseek.com)
DEEPSEEK_API_KEY=sk_xxxxx

# Replicate (FREE - get from https://replicate.com)
REPLICATE_API_TOKEN=xxxxx

# YouTube OAuth (setup in Google Cloud Console)
YOUTUBE_OAUTH_TOKEN=xxxxx
YOUTUBE_CHANNEL_ID=UCp3eKZhxDGwruAdId9pxgcg
```

### 5. Run Pipeline
```bash
python pipeline.py --videos 10 --daily-schedule
```

## 📝 Content Strategy

### Video Pillars (Rotate Daily)
1. **Psychology/Mindset** (40%)
   - Motivation hacks
   - Mental health tips
   - Behavioral psychology

2. **Productivity/Habits** (40%)
   - Time management
   - Focus techniques
   - Daily routines

3. **Finance/Money** (20%)
   - Money mindset
   - Budgeting tips
   - Wealth building

### Example Scripts
```yaml
- Title: "The 2-Minute Rule"
  Hook: "Most people wait for the perfect moment..."
  Body: "The 2-minute rule: Start with just 2 minutes..."
  CTA: "What's ONE thing you'll commit to?"
  Duration: 45 seconds
```

## 📈 Growth Projections (6 Months)

```
Month 1: 50k subs | 2-3M views
Month 2: 200k subs | 8-10M views  
Month 3: 500k subs | 20M views
Month 4: 1M subs | 35M views
Month 5: 2M subs | 25M views
Month 6: 3-4M subs | 15-20M views
────────────────────────────────
TOTAL: 100-120M views ✅
```

## 🎯 Key Features

- ✅ **100% Free** - No paid subscriptions
- ✅ **Automated** - 3-5 videos daily
- ✅ **Scalable** - Easy to add more content pillars
- ✅ **Open Source** - Fully transparent code
- ✅ **YouTube Optimized** - SEO + algorithm hacks
- ✅ **CI/CD Ready** - GitHub Actions integration

## 📚 Documentation

- [Setup Guide](./docs/SETUP.md)
- [API Configuration](./docs/API_SETUP.md)
- [Content Creation](./docs/CONTENT.md)
- [Troubleshooting](./docs/TROUBLESHOOTING.md)

## 🤝 Contributing

Fork the repo, make improvements, and submit PRs!

## 📄 License

MIT - Free to use and modify

---

**Created:** March 2026  
**YouTube Channel:** [@velocityvault_yt](https://www.youtube.com/channel/UCp3eKZhxDGwruAdId9pxgcg)
