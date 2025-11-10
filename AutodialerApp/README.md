# 🤖 Autodialer - AI Powered Calling System

An intelligent autodialer application that can automatically call phone numbers using Twilio's API, with AI-powered voice messages and natural language command processing via Google Gemini.

## Features

- 📱 **Bulk Calling**: Upload up to 100 phone numbers and call them automatically
- 🤖 **AI Voice**: Uses Twilio's text-to-speech for professional AI-generated voice calls
- 🧠 **Natural Language Commands**: Use AI prompts like "make a call to +18001234567" or "start calling uploaded numbers"
- 📊 **Call Logging**: Real-time tracking of call status, success/failure rates
- 🔒 **Test Safe**: Designed for testing with +1800 numbers (free with Twilio trial)
- 🎯 **Sequential Calling**: Calls numbers one by one with configurable delays

## Prerequisites

- Ruby 3.2 or higher
- Bundler gem (`gem install bundler`)
- Twilio account (free trial available)
- Google Gemini API key (free tier available)

## Installation

1. **Clone/Download** this project to your local machine

2. **Install Dependencies**:
   ```bash
   bundle install
   ```

3. **Configure Environment**:
   - Copy `env_example.txt` to `.env`
   - Fill in your Twilio and Gemini API credentials

4. **Run the Application**:
   ```bash
   ruby app.rb
   ```

5. **Access the Dashboard**:
   Open http://localhost:4567 in your browser

## Configuration

### Twilio Setup
1. Sign up at [twilio.com](https://www.twilio.com)
2. Get your Account SID and Auth Token from the console
3. Purchase or use a trial phone number
4. Add your credentials to `.env`

### Gemini AI Setup
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the key to your `.env` file

## Usage

### Uploading Phone Numbers
- Paste phone numbers in the text area (one per line or comma-separated)
- Use test numbers starting with +1800 (free to call)
- Maximum 100 numbers per batch

### AI Voice Commands
Type natural language commands like:
- "make a call to +18001234567"
- "start calling all uploaded numbers"
- "upload new phone numbers"

### Starting Calls
- Click "Start Calling All Numbers" to begin sequential calling
- Monitor progress in real-time through the dashboard
- View detailed logs and statistics

## Testing

For testing purposes, use these +1800 numbers:
- +18001234567
- +18009876543
- +18005551234

These numbers are free to call with Twilio trial accounts and won't charge real people.

## Architecture

- **Backend**: Sinatra web framework (Ruby)
- **Calling**: Twilio Voice API
- **AI Processing**: Google Gemini API integration
- **Voice**: Twilio text-to-speech (Alice voice)
- **Frontend**: Vanilla JavaScript with responsive design

## Security Notes

- Never commit `.env` files with real API keys
- Use environment variables for all sensitive data
- Test with trial accounts before production use
- Monitor API usage to avoid unexpected charges

## API Endpoints

- `GET /` - Main dashboard
- `POST /upload_contacts` - Upload phone numbers
- `POST /start_calling` - Initiate calling sequence
- `POST /ai_prompt` - Process AI commands
- `GET /call_logs` - Retrieve call logs
- `POST /call_status` - Twilio status callbacks

## Troubleshooting

### Common Issues
- **"Could not find gem"**: Run `bundle install`
- **"Invalid Twilio credentials"**: Check your `.env` file
- **"Port already in use"**: Change the port in `app.rb`

### Logs
Check the console output for detailed error messages and API responses.

## License

This project is for educational and testing purposes. Ensure compliance with local telecommunications laws and Twilio's terms of service.

## Disclaimer

This tool is designed for legitimate business communications and testing purposes only. Misuse for spam, harassment, or unauthorized calling may violate laws and service terms.
