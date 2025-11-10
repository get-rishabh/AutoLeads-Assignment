class Contact
  attr_accessor :phone_number, :name, :status

  def initialize(phone_number, name = nil)
    @phone_number = normalize_phone_number(phone_number)
    @name = name || "Contact #{@phone_number}"
    @status = :pending # :pending, :calling, :completed, :failed
  end

  def normalize_phone_number(number)
    # Remove all non-digit characters
    digits_only = number.gsub(/\D/, '')

    # Add +1 prefix if not present and it's a US number
    if digits_only.length == 10
      "+1#{digits_only}"
    elsif digits_only.length == 11 && digits_only.start_with?('1')
      "+#{digits_only}"
    else
      "+#{digits_only}"
    end
  end

  def valid?
    # Basic validation for US phone numbers
    @phone_number.match?(/^\+1\d{10}$/) ||
    @phone_number.match?(/^\+1\d{3}\d{3}\d{4}$/)
  end

  def test_number?
    # Check if it's a test number (+1800...)
    @phone_number.start_with?('+1800')
  end

  def to_h
    {
      phone_number: @phone_number,
      name: @name,
      status: @status
    }
  end
end
