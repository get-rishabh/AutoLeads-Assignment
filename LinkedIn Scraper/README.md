# LinkedIn Profile Scraper

A Streamlit-based web application for scraping LinkedIn profile data using Selenium with stealth techniques.

## ⚠️ Important Warning

**This tool violates LinkedIn's Terms of Service (Section 8.2).** Use of this tool may result in:
- Account suspension or permanent ban
- IP address blocking
- Legal consequences
- CAPTCHA challenges and rate limiting

**This project is for educational purposes only.** We strongly recommend using LinkedIn's official API for any production use case.

## Features

- 🤖 **AI-powered parsing** with Google Gemini (semantic understanding)
- 🔐 Manual LinkedIn authentication (user logs in themselves)
- 🎯 Scrape multiple profile URLs
- 📊 Extract comprehensive profile data
- 💾 Export to CSV format
- 🕵️ Stealth techniques to reduce detection
- 🎨 Clean Streamlit UI

## Extracted Data Fields

The scraper extracts the following information from LinkedIn profiles:

- **Basic Information**: Name, Headline, Location, Profile URL
- **About/Summary**: Profile summary text
- **Current Position**: Current company and job title
- **Work Experience**: Previous positions, companies, and durations
- **Education**: Schools, degrees, and fields of study
- **Skills**: Top skills listed on profile

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser installed
- Stable internet connection
- **Gemini API key** (FREE at https://makersuite.google.com/app/apikey)

### Setup Steps

1. **Clone or download this repository**

2. **Get Gemini API Key**
   - Go to https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API Key"
   - Copy the key

3. **Configure API Key**
   - Copy `env_example.txt` to `.env`
   - Add your API key: `GEMINI_API_KEY=your-key-here`
   - Save the file

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Verify Chrome installation**
   - Make sure Google Chrome is installed on your system
   - The script will automatically download the appropriate ChromeDriver

📖 **Note:** Gemini API is completely FREE with generous rate limits

## Quick Start

### Installation & First Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

📖 **For detailed usage instructions, see [USAGE_GUIDE.md](USAGE_GUIDE.md)**

## Usage

### Step 2: Login to LinkedIn

1. Click the **"Open Browser & Login to LinkedIn"** button
2. A Chrome browser window will open with the LinkedIn login page
3. **Manually log in** to your LinkedIn account
   - Enter your credentials
   - Complete any security checks (2FA, CAPTCHA, etc.)
4. After successfully logging in, return to the Streamlit app
5. Click **"Confirm Login"** to verify authentication

### Step 3: Enter Profile URLs

1. In the text area, enter LinkedIn profile URLs (one per line)
2. Format: `https://www.linkedin.com/in/username/`
3. Example:
```
https://www.linkedin.com/in/johndoe/
https://www.linkedin.com/in/janedoe/
https://www.linkedin.com/in/bobsmith/
```

### Step 4: Start Scraping

1. Click **"Start Scraping"** button
2. The app will process each profile with delays between requests
3. Progress bar will show current status
4. Wait for completion (typically 5-10 seconds per profile)

### Step 5: Download Results

1. Preview the scraped data in the table
2. Click **"Download CSV"** to download the results
3. Or click **"Save to Output Folder"** to save locally in the `output/` directory

## Project Structure

```
AeroLeads/
├── app.py                 # Main Streamlit application
├── scraper.py            # LinkedIn scraper with Selenium
├── ai_parser.py          # Gemini AI data extraction
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── output/              # Output directory for CSV files
```

## Configuration

### Scraping Delays

The scraper includes human-like delays to avoid detection:
- **Between page actions**: 2-5 seconds
- **Between profiles**: 4-7 seconds
- **Smooth scrolling**: 0.5-1.5 seconds per increment

You can adjust these in `scraper.py` by modifying the `human_like_delay()` method.

### Browser Options

The scraper uses undetected-chromedriver with stealth options. Additional Chrome options can be added in `scraper.py`:

```python
options.add_argument('--your-option-here')
```

## Limitations

- **Detection Risk**: LinkedIn actively detects automated scraping
- **Rate Limiting**: Scraping too many profiles too quickly will trigger restrictions
- **Data Availability**: Can only scrape data visible to the logged-in account
- **Profile Privacy**: Private profiles or connection-only data may not be accessible
- **HTML Changes**: LinkedIn frequently updates their HTML structure
- **Recommended Limit**: 5-10 profiles per session, with breaks between sessions

## Documentation

All documentation is in this README file.

## Troubleshooting

🔧 **For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

### Quick Fixes

#### Browser doesn't open
- Ensure Google Chrome is installed
- Try reinstalling `undetected-chromedriver`: `pip install --upgrade undetected-chromedriver`

### Login verification fails
- Make sure you're fully logged into LinkedIn (check the feed page)
- Complete any security challenges
- Try logging out and logging in again

### CAPTCHA appears
- This is expected behavior from LinkedIn
- Complete the CAPTCHA manually
- Reduce scraping frequency
- Take longer breaks between sessions

### Data extraction incomplete
- LinkedIn's HTML structure may have changed
- Some profiles have different layouts
- Private or restricted profiles return limited data
- Check the error column in the CSV for specific issues

### Account restricted
- You've been detected by LinkedIn's anti-scraping measures
- Wait 24-48 hours before trying again
- Consider using a different account
- Reduce scraping frequency significantly

### Data showing "N/A"
**Most Common Issue!** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions:
- LinkedIn HTML structure may have changed
- Insufficient wait time for page load
- Profile privacy settings
- Session expired

**Quick test:** Run `python test_scraper.py <profile_url>` to debug

## Best Practices

1. **Use Test Accounts**: Never use your primary LinkedIn account
2. **Scrape Responsibly**: Limit to 5-10 profiles per session
3. **Add Delays**: Don't rush - longer delays = less detection
4. **Monitor Activity**: Watch for CAPTCHA or login prompts
5. **Respect Privacy**: Only scrape publicly available information
6. **Have Backups**: Keep your data as LinkedIn may restrict access

## Technical Details

### Stealth Techniques Used

- **undetected-chromedriver**: Bypasses basic automation detection
- **Random delays**: Mimics human browsing behavior
- **Smooth scrolling**: Gradual page scrolling instead of instant jumps
- **Session persistence**: Maintains login state across scrapes
- **No automation flags**: Disables WebDriver automation indicators

### Dependencies

- `streamlit`: Web interface
- `selenium`: Browser automation
- `undetected-chromedriver`: Stealth Chrome driver
- `pandas`: Data manipulation and CSV export
- `webdriver-manager`: Automatic driver management
- **`google-generativeai`**: Gemini AI for data extraction
- **`beautifulsoup4`**: HTML parsing
- **`python-dotenv`**: Environment variable management

## Legal & Ethical Considerations

**By using this tool, you acknowledge:**

- Scraping LinkedIn violates their Terms of Service
- You use this tool at your own risk
- Account suspension/ban is possible
- This is for educational purposes only
- You will not use this for commercial purposes without proper authorization
- You should use LinkedIn's official API for legitimate business use

## Alternative Solutions

For legitimate business use, consider:

- **LinkedIn Official API**: https://developer.linkedin.com/
- **LinkedIn Recruiter**: Official recruiting solution
- **LinkedIn Sales Navigator**: Official sales solution
- **Third-party API services**: Legal data providers with LinkedIn partnerships

## Support

This project is provided as-is for educational purposes. For issues:

1. Check the Troubleshooting section above
2. Review LinkedIn's current HTML structure (it changes frequently)
3. Ensure all dependencies are properly installed
4. Test with a fresh throwaway account

## License

This project is for educational purposes only. Use at your own risk.

## Disclaimer

The developers of this tool are not responsible for:
- Account suspensions or bans
- Violation of LinkedIn's Terms of Service
- Any legal consequences
- Data accuracy or completeness
- Any damages resulting from use of this tool

**Use LinkedIn's official API for any production or commercial use.**

