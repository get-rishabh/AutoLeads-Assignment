require_relative 'twilio_service'
require_relative '../models/contact'
require_relative '../models/call_log'

class AutodialJob
  def initialize(twilio_service)
    @twilio_service = twilio_service
    @contacts = []
    @call_logs = []
    @is_running = false
  end

  def add_contacts(phone_numbers)
    phone_numbers.each do |number|
      contact = Contact.new(number.strip)
      @contacts << contact if contact.valid?
    end
    @contacts = @contacts.first(100) # Limit to 100 as requested
  end

  def start_calling(base_url)
    return { success: false, error: 'Already running' } if @is_running
    return { success: false, error: 'No contacts to call' } if @contacts.empty?

    @is_running = true

    Thread.new do
      begin
        @contacts.each do |contact|
          next if contact.status != :pending

          contact.status = :calling
          call_result = @twilio_service.make_call(
            contact.phone_number,
            "#{base_url}/twiml",
            "#{base_url}/call_status"
          )

          if call_result[:success]
            call_log = CallLog.new(contact, call_result[:call_sid])
            @call_logs << call_log
          else
            call_log = CallLog.new(contact)
            call_log.update_status(:failed, nil, call_result[:error])
            @call_logs << call_log
          end

          # Wait between calls to avoid overwhelming the API
          sleep(3)
        end
      ensure
        @is_running = false
      end
    end

    { success: true, message: "Started calling #{@contacts.length} contacts" }
  end

  def stop_calling
    @is_running = false
    { success: true, message: 'Stopping calls...' }
  end

  def update_call_status(call_sid, status, duration = nil)
    log_entry = @call_logs.find { |log| log.call_sid == call_sid }
    if log_entry
      log_entry.update_status(status.to_sym, duration)
      log_entry.contact.status = status.to_sym
    end
  end

  def get_stats
    total_contacts = @contacts.length
    initiated = @call_logs.length
    completed = @call_logs.count(&:successful?)
    failed = @call_logs.count(&:failed?)

    {
      total_contacts: total_contacts,
      calls_initiated: initiated,
      calls_completed: completed,
      calls_failed: failed,
      is_running: @is_running
    }
  end

  def get_call_logs
    @call_logs.map(&:to_h)
  end

  def clear_data
    @contacts.clear
    @call_logs.clear
    @is_running = false
  end
end
