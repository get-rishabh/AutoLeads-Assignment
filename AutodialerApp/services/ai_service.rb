require 'httparty'

class AIService
  def initialize(api_key)
    @api_key = api_key
    @base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
  end

  def process_command(prompt)
    return mock_response(prompt) unless @api_key && !@api_key.empty?

    begin
      response = HTTParty.post(
        "#{@base_url}?key=#{@api_key}",
        headers: {
          'Content-Type' => 'application/json'
        },
        body: {
          contents: [{
            parts: [{
              text: build_prompt(prompt)
            }]
          }]
        }.to_json
      )

      if response.success?
        parse_gemini_response(response.parsed_response)
      else
        mock_response(prompt)
      end
    rescue => e
      mock_response(prompt)
    end
  end

  def generate_blog_article(title)
    unless @api_key && !@api_key.empty?
      return { success: false, error: 'GEMINI_API_KEY is not set or empty' }
    end

    require_relative '../models/article'

    # Try flash model first
    result = generate_with_model(title, 'gemini-2.5-flash')
    
    # If flash fails with 503 (overloaded) or 429 (rate limit), fallback to pro
    if !result[:success] && result[:error]
      error_code = result[:error_code] || extract_error_code(result[:error])
      if error_code == 503 || error_code == 429
        # Fallback to pro model
        result = generate_with_model(title, 'gemini-2.5-pro', fallback: true)
      end
    end
    
    result
  end

  def generate_with_model(title, model_name, fallback: false)
    begin
      model_url = "https://generativelanguage.googleapis.com/v1beta/models/#{model_name}:generateContent"
      
      response = HTTParty.post(
        "#{model_url}?key=#{@api_key}",
        headers: {
          'Content-Type' => 'application/json'
        },
        body: {
          contents: [{
            parts: [{
              text: build_blog_prompt(title)
            }]
          }]
        }.to_json
      )

      if response.success?
        parsed = response.parsed_response
        content = parse_blog_response(parsed)
        if content && !content.empty?
          article = Article.new(title, content)
          { success: true, article: article, model: model_name, fallback: fallback }
        else
          { success: false, error: "Failed to parse article content. Response: #{parsed.inspect[0..200]}" }
        end
      else
        parsed = response.parsed_response rescue {}
        error_code = response.code
        error_msg = parsed['error'] || parsed['message'] || "HTTP #{response.code}: #{response.message}"
        { success: false, error: "API request failed: #{error_msg}", error_code: error_code }
      end
    rescue => e
      { success: false, error: "Exception: #{e.message}" }
    end
  end

  def extract_error_code(error_string)
    # Extract HTTP error code from error message
    match = error_string.match(/HTTP (\d+)/)
    return match[1].to_i if match
    
    # Check for error code in various formats (Ruby hash, JSON, etc.)
    if error_string.match(/["']code["']\s*[=:>]\s*503/) || error_string.include?('503')
      return 503
    elsif error_string.match(/["']code["']\s*[=:>]\s*429/) || error_string.include?('429')
      return 429
    end
    
    nil
  end

  private

  def build_prompt(user_input)
    "You are an AI assistant for an autodialer system. Analyze this user input and respond with a JSON object containing:
- action: The action to take ('call', 'start_calling', 'upload_contacts', 'get_logs', 'unknown')
- phone_number: Extracted phone number if applicable (format as +1XXXXXXXXXX)
- message: A brief confirmation message
- confidence: Your confidence level (0-1)

User input: '#{user_input}'

Respond only with valid JSON, no additional text."
  end

  def parse_gemini_response(response)
    begin
      if response['candidates'] && response['candidates'].first
        text = response['candidates'].first['content']['parts'].first['text']
        # Extract JSON from the response
        json_match = text.match(/\{.*\}/m)
        if json_match
          JSON.parse(json_match[0])
        else
          mock_response("")
        end
      else
        mock_response("")
      end
    rescue => e
      mock_response("")
    end
  end

  def mock_response(prompt)
    prompt_down = prompt.downcase

    # Simple keyword matching as fallback
    if prompt_down.include?('call') && extract_phone_number(prompt)
      phone = extract_phone_number(prompt)
      {
        'action' => 'call',
        'phone_number' => phone,
        'message' => "Initiating call to #{phone}",
        'confidence' => 0.8
      }
    elsif prompt_down.include?('start') && (prompt_down.include?('call') || prompt_down.include?('dial'))
      {
        'action' => 'start_calling',
        'message' => 'Starting calls to all uploaded contacts',
        'confidence' => 0.9
      }
    elsif prompt_down.include?('upload') || prompt_down.include?('import') || prompt_down.include?('add')
      {
        'action' => 'upload_contacts',
        'message' => 'Please provide phone numbers to upload',
        'confidence' => 0.7
      }
    elsif prompt_down.include?('log') || prompt_down.include?('status') || prompt_down.include?('report')
      {
        'action' => 'get_logs',
        'message' => 'Retrieving call logs and statistics',
        'confidence' => 0.8
      }
    else
      {
        'action' => 'unknown',
        'message' => 'I didn\'t understand that command. Try: "call +18001234567" or "start calling"',
        'confidence' => 0.3
      }
    end
  end

  def extract_phone_number(text)
    # Look for phone number patterns
    phone_patterns = [
      /(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})/,
      /(\+?1?[-.\s]?)?([0-9]{3})[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})/,
      /\+?1?([0-9]{10})/
    ]

    phone_patterns.each do |pattern|
      match = text.match(pattern)
      if match
        # Clean and format the number
        digits = match.captures.compact.join.gsub(/\D/, '')
        return "+1#{digits}" if digits.length == 10
        return "+#{digits}" if digits.length == 11 && digits.start_with?('1')
      end
    end

    nil
  end

  private

  def build_blog_prompt(title)
    "You are a professional technical writer. Write a comprehensive, well-structured blog article about the following topic:

Topic: '#{title}'

Requirements:
- Write in a clear, engaging style suitable for developers
- Include an introduction, main content sections, and conclusion
- Use proper markdown formatting (headers, code blocks, lists)
- Make it informative and educational
- Keep it between 800-1500 words
- Include practical examples where relevant
- Use proper technical terminology

Return only the article content in markdown format, no additional text or explanations."
  end

  def parse_blog_response(response)
    begin
      if response && response['candidates'] && response['candidates'].first
        candidate = response['candidates'].first
        if candidate['content'] && candidate['content']['parts'] && candidate['content']['parts'].first
          text = candidate['content']['parts'].first['text']
          return text.strip if text && !text.empty?
        end
      end
      nil
    rescue => e
      nil
    end
  end
end
