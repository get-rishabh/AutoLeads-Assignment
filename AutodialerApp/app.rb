require 'sinatra'
require 'sinatra/json'
require 'twilio-ruby'
require 'dotenv/load'
require 'json'

# Load environment variables
Dotenv.load

# Load our custom classes
require_relative 'models/contact'
require_relative 'models/call_log'
require_relative 'models/article'
require_relative 'services/twilio_service'
require_relative 'services/ai_service'
require_relative 'services/autodial_job'

# Initialize services
TWILIO_ACCOUNT_SID = ENV['TWILIO_ACCOUNT_SID'] || 'demo_sid'
TWILIO_AUTH_TOKEN = ENV['TWILIO_AUTH_TOKEN'] || 'demo_token'
TWILIO_PHONE_NUMBER = ENV['TWILIO_PHONE_NUMBER'] || '+15551234567'

GEMINI_API_KEY = ENV['GEMINI_API_KEY'] || ''

# Initialize services
$twilio_service = TwilioService.new(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER)
$ai_service = AIService.new(GEMINI_API_KEY)
$autodial_job = AutodialJob.new($twilio_service)

# Initialize blog articles storage
$articles = []

class AutodialerApp < Sinatra::Base
  configure do
    set :public_folder, 'public'
    set :views, 'views'
  end

  # Blog routes
  get '/blog' do
    @articles = $articles.sort_by { |a| a.created_at }.reverse
    erb :blog_index
  end

  get '/blog/:slug' do
    @article = $articles.find { |a| a.slug == params[:slug] }
    if @article
      erb :blog_article
    else
      status 404
      "Article not found"
    end
  end

  # API endpoint to generate blog articles
  post '/blog/generate' do
    content_type :json

    titles_input = params[:titles]
    if titles_input.nil? || titles_input.empty?
      return { success: false, error: 'No article titles provided' }.to_json
    end

    begin
      # Parse titles (one per line)
      titles = titles_input.split("\n").map(&:strip).reject(&:empty?)

      if titles.empty?
        return { success: false, error: 'No valid titles found' }.to_json
      end

      generated_articles = []
      errors = []

      titles.each do |title|
        result = $ai_service.generate_blog_article(title)
        if result[:success] && result[:article]
          $articles << result[:article]
          article_hash = result[:article].to_h
          # Add fallback and model info if available
          article_hash[:fallback] = result[:fallback] if result.key?(:fallback)
          article_hash[:model] = result[:model] if result.key?(:model)
          generated_articles << article_hash
        elsif result[:error]
          errors << "#{title}: #{result[:error]}"
        end
      end

      if generated_articles.empty? && errors.any?
        {
          success: false,
          error: "Failed to generate articles. Errors: #{errors.join('; ')}"
        }.to_json
      else
        {
          success: true,
          count: generated_articles.length,
          articles: generated_articles,
          errors: errors
        }.to_json
      end
    rescue => e
      { success: false, error: "Failed to generate articles: #{e.message}" }.to_json
    end
  end

  # Main dashboard
  get '/' do
    erb :index
  end

  # API endpoint to upload/process phone numbers
  post '/upload_contacts' do
    content_type :json

    phone_numbers = params[:phone_numbers]
    if phone_numbers
      # Parse phone numbers (comma-separated or newline-separated)
      numbers = phone_numbers.split(/[\n,]/).map(&:strip).reject(&:empty?)

      $autodial_job.clear_data
      $autodial_job.add_contacts(numbers)

      contacts_data = $autodial_job.instance_variable_get(:@contacts).map(&:to_h)
      { success: true, count: contacts_data.length, contacts: contacts_data }.to_json
    else
      { success: false, error: 'No phone numbers provided' }.to_json
    end
  end

  # API endpoint to start calling
  post '/start_calling' do
    content_type :json

    result = $autodial_job.start_calling(request.base_url)
    result.to_json
  end

  # API endpoint for AI prompt processing
  post '/ai_prompt' do
    content_type :json

    prompt = params[:prompt]
    if prompt.nil? || prompt.empty?
      return { success: false, error: 'No prompt provided' }.to_json
    end

    # Process AI prompt
    response = $ai_service.process_command(prompt)
    response.to_json
  end

  # Get call logs
  get '/call_logs' do
    content_type :json
    $autodial_job.get_call_logs.to_json
  end

  # Get statistics
  get '/stats' do
    content_type :json
    $autodial_job.get_stats.to_json
  end

  # Twilio webhook for call status updates
  post '/call_status' do
    call_sid = params['CallSid']
    call_status = params['CallStatus']
    call_duration = params['CallDuration']

    # Update call log
    $autodial_job.update_call_status(call_sid, call_status, call_duration)

    content_type 'text/xml'
    '<Response></Response>'
  end


end

# TwiML endpoint for call instructions (mount within the app)
class AutodialerApp < Sinatra::Base
  get '/twiml' do
    content_type 'text/xml'
    $twilio_service.generate_twiml
  end
end

# Allow running with `ruby app.rb`
if __FILE__ == $0
  AutodialerApp.run! port: 4567, bind: '127.0.0.1'
end
