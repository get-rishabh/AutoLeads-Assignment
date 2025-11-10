# 🚀 AeroLeads - Complete Lead Generation & Outreach Suite

A comprehensive AI-powered lead generation and outreach platform that combines LinkedIn data scraping, automated calling, and content generation into a unified system.

## 📋 Overview

AeroLeads consists of three integrated components:

1. **🔍 LinkedIn Scraper** - Extract professional contact data from LinkedIn profiles
2. **📞 Autodialer** - AI-powered automated calling system with natural language commands
3. **📝 Blog Generator** - AI content creation for marketing and lead nurturing

## 🏗️ System Architecture

```
LinkedIn Profiles → AI Data Extraction → Contact Database → Automated Calling
                                             ↓
                                    AI Blog Content Generation → Marketing Outreach
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (for LinkedIn Scraper)
- **Ruby 3.2+** (for Autodialer & Blog Generator)
- **Google Chrome** (for LinkedIn scraping)
- **API Keys**: Gemini AI, Twilio (for calling)

### 1. Clone & Setup
```bash
git clone https://github.com/get-rishabh/AutoLeads-Assignment.git
cd AutoLeads-Assignment
```

### 2. Get API Keys
- **Gemini AI**: https://makersuite.google.com/app/apikey (Free)
- **Twilio**: https://twilio.com (Free trial available)

### 3. Configure Environment
```bash
# LinkedIn Scraper
cd "LinkedIn Scraper"
cp env_example.txt .env
# Edit .env with your Gemini API key

# Autodialer & Blog Generator
cd ../AutodialerApp
cp env_example.txt .env
# Edit .env with your Twilio credentials and Gemini API key
```

### 4. Install Dependencies
```bash
# LinkedIn Scraper
cd "LinkedIn Scraper"
pip install -r requirements.txt

# Autodialer & Blog Generator
cd ../AutodialerApp
bundle install
```

## 🔍 Component 1: LinkedIn Scraper

**Location**: `LinkedIn Scraper/`

A sophisticated LinkedIn profile scraper that uses AI to extract structured data from professional profiles.

### Features
- 🤖 AI-powered data extraction with Google Gemini
- 🔐 Manual authentication (you log in yourself)
- 🎯 Multi-profile scraping
- 📊 CSV export with comprehensive profile data
- 🕵️ Stealth techniques to minimize detection
- 🎨 Clean Streamlit web interface

### Quick Start
```bash
cd "LinkedIn Scraper"
streamlit run app.py
# Opens at http://localhost:8501
```

### Usage Workflow
1. **Login**: Click "Open Browser & Login to LinkedIn"
2. **Authenticate**: Manually log in to LinkedIn in the opened browser
3. **Input URLs**: Paste LinkedIn profile URLs (one per line)
4. **Scrape**: Click "Start Scraping" to extract data
5. **Export**: Download results as CSV

### Extracted Data
- Basic info (name, headline, location)
- Work experience & education
- Skills and professional summary
- Contact information when available

⚠️ **Legal Notice**: This tool violates LinkedIn's Terms of Service. Use only with test accounts for educational purposes.

## 📞 Component 2: Autodialer

**Location**: `AutodialerApp/`

An intelligent calling system that combines Twilio's voice API with AI natural language processing.

### Features
- 📱 Bulk calling (up to 100 numbers)
- 🤖 AI voice synthesis (professional voice)
- 🧠 Natural language commands ("call +18001234567")
- 📊 Real-time call tracking and logging
- 🔒 Test-safe with free +1800 numbers
- 🎯 Sequential calling with configurable delays

### Quick Start
```bash
cd AutodialerApp
ruby app.rb
# Opens at http://localhost:4567
```

### Usage Workflow
1. **Upload Contacts**: Paste phone numbers (one per line)
2. **AI Commands**: Use natural language like "start calling all numbers"
3. **Monitor**: Watch real-time progress and call logs
4. **Review**: Check detailed call statistics and outcomes

### Testing
Use these free test numbers:
- +18001234567
- +18009876543
- +18005551234

## 📝 Component 3: Blog Generator

**Location**: `AutodialerApp/` (integrated)

AI-powered content generation system for creating blog articles and marketing materials.

### Features
- 🤖 AI article generation with Google Gemini
- 📝 Multiple article creation in batch
- 🎨 Clean blog interface
- 🔗 SEO-friendly URLs and slugs
- 📊 Content management dashboard

### Usage
1. **Access Blog**: Visit `http://localhost:4567/blog`
2. **Generate Content**: Use the admin interface to create articles
3. **Batch Generation**: Submit multiple article titles at once
4. **View Articles**: Browse generated content with clean formatting

## 🔄 Complete Workflow

### Lead Generation Pipeline

1. **Data Collection** (LinkedIn Scraper)
   - Identify target professionals on LinkedIn
   - Extract contact information and professional details
   - Export structured data as CSV

2. **Contact Enrichment** (Manual/Automated)
   - Add phone numbers to contact database
   - Verify and clean contact information

3. **Automated Outreach** (Autodialer)
   - Upload contact lists
   - Configure AI voice messages
   - Execute automated calling campaigns

4. **Content Marketing** (Blog Generator)
   - Generate relevant blog content
   - Create lead magnets and educational materials
   - Support ongoing lead nurturing

### Integration Points

- **Data Flow**: LinkedIn scraper → CSV export → Autodialer contact import
- **AI Services**: Shared Gemini API across all components
- **Content Strategy**: Blog content supports lead nurturing campaigns
- **Analytics**: Call logs and scraping results inform optimization

## ⚙️ Configuration

### Environment Variables

Create `.env` files in each component directory:

```env
# Shared across components
GEMINI_API_KEY=your_gemini_api_key_here

# Autodialer specific
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+15551234567
```

### Port Configuration

- **LinkedIn Scraper**: http://localhost:8501 (Streamlit)
- **Autodialer & Blog**: http://localhost:4567 (Sinatra)

## 🛠️ Development & Testing

### Testing Each Component

```bash
# Test LinkedIn Scraper
cd "LinkedIn Scraper"
python -c "import scraper; print('Scraper imports OK')"

# Test Autodialer
cd ../AutodialerApp
ruby -c app.rb

# Test Blog Generator
curl -X POST http://localhost:4567/blog/generate \
  -d "titles=Test Article Title"
```

### Debugging

- **LinkedIn Scraper**: Check browser console and Streamlit logs
- **Autodialer**: Monitor Sinatra console output
- **Blog Generator**: Check AI service logs and article generation responses

## 🔒 Security & Compliance

### API Key Management
- Never commit `.env` files
- Rotate API keys regularly
- Monitor API usage to avoid rate limits

### Legal Considerations
- LinkedIn scraping violates their ToS
- Telemarketing laws vary by jurisdiction
- Obtain proper consent for automated calling
- Use for educational/testing purposes only

### Data Privacy
- Respect individual privacy rights
- Implement proper data retention policies
- Secure sensitive contact information
- Comply with GDPR and similar regulations

## 📊 Monitoring & Analytics

### Key Metrics to Track
- **Scraping Success Rate**: Profiles successfully scraped vs attempted
- **Call Connection Rate**: Calls answered vs total calls
- **Content Engagement**: Blog views and lead conversions
- **API Usage**: Monitor costs and rate limits

### Logging
- All components generate detailed logs
- Call logs include timestamps and outcomes
- Error logs help with troubleshooting

## 🚀 Deployment

### Local Development
All components run locally for development and testing.

### Production Considerations
- **LinkedIn Scraper**: Consider using proxies for production-scale scraping
- **Autodialer**: Implement proper rate limiting and compliance checks
- **Blog Generator**: Add content moderation and SEO optimization

### Scaling
- Implement database storage for large contact lists
- Add job queues for high-volume calling
- Consider cloud deployment for reliability

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branches
3. Test all components thoroughly
4. Submit pull requests with detailed descriptions

### Code Standards
- Follow existing code patterns
- Add comprehensive documentation
- Include unit tests for new features
- Update README for significant changes

## 📞 Support & Documentation

### Troubleshooting
- Check component-specific README files
- Verify API keys and configuration
- Monitor logs for error messages
- Test with minimal data sets first

### Resources
- **Twilio Docs**: https://www.twilio.com/docs
- **Gemini AI**: https://ai.google.dev/docs
- **Sinatra**: http://sinatrarb.com/documentation.html
- **Streamlit**: https://docs.streamlit.io

## 📄 License

This project is for educational and testing purposes. Commercial use requires proper licensing and compliance with platform terms of service.

## ⚠️ Disclaimer

This suite is designed for legitimate business communications and testing. Misuse for spam, harassment, or unauthorized activities may violate laws and service terms. Always obtain proper consent and follow applicable regulations.

---

**Built with ❤️ for lead generation and business development professionals**
