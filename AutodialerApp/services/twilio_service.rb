require 'twilio-ruby'

class TwilioService
  def initialize(account_sid, auth_token, phone_number)
    @account_sid = account_sid
    @auth_token = auth_token
    @phone_number = phone_number
    @client = Twilio::REST::Client.new(@account_sid, @auth_token)
  end

  def make_call(to_number, twiml_url, status_callback_url = nil)
    begin
      call_params = {
        from: @phone_number,
        to: to_number,
        url: twiml_url
      }

      # Add status callback if provided
      if status_callback_url
        call_params.merge!(
          status_callback: status_callback_url,
          status_callback_event: ['initiated', 'ringing', 'answered', 'completed'],
          status_callback_method: 'POST'
        )
      end

      call = @client.calls.create(call_params)
      { success: true, call_sid: call.sid }
    rescue Twilio::REST::RestError => e
      { success: false, error: e.message, code: e.code }
    rescue => e
      { success: false, error: "Unexpected error: #{e.message}" }
    end
  end

  def generate_twiml(message = nil, voice = 'alice')
    default_message = "Hello! This is an automated call from Autodialer. Thank you for your time."
    message ||= default_message

    twiml = Twilio::TwiML::VoiceResponse.new do |r|
      r.say(message: message, voice: voice)
      r.hangup
    end

    twiml.to_s
  end

  def get_call_details(call_sid)
    begin
      call = @client.calls(call_sid).fetch
      {
        success: true,
        sid: call.sid,
        status: call.status,
        duration: call.duration,
        direction: call.direction,
        from: call.from,
        to: call.to,
        start_time: call.start_time,
        end_time: call.end_time
      }
    rescue => e
      { success: false, error: e.message }
    end
  end
end
