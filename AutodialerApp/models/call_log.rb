class CallLog
  attr_accessor :id, :contact, :call_sid, :status, :duration, :error_message, :created_at, :updated_at

  STATUSES = [:initiated, :ringing, :in_progress, :completed, :failed, :busy, :no_answer, :canceled]

  def initialize(contact, call_sid = nil)
    @id = SecureRandom.uuid
    @contact = contact
    @call_sid = call_sid
    @status = :initiated
    @duration = 0
    @error_message = nil
    @created_at = Time.now
    @updated_at = Time.now
  end

  def update_status(new_status, duration = nil, error = nil)
    return unless STATUSES.include?(new_status.to_sym)

    @status = new_status.to_sym
    @duration = duration if duration
    @error_message = error if error
    @updated_at = Time.now
  end

  def successful?
    [:completed, :in_progress].include?(@status)
  end

  def failed?
    [:failed, :busy, :no_answer, :canceled].include?(@status)
  end

  def to_h
    {
      id: @id,
      phone_number: @contact.phone_number,
      call_sid: @call_sid,
      status: @status.to_s,
      duration: @duration,
      error_message: @error_message,
      created_at: @created_at.iso8601,
      updated_at: @updated_at.iso8601
    }
  end
end
