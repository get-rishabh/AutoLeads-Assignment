class Article
  attr_accessor :id, :title, :content, :created_at, :slug

  def initialize(title, content)
    @id = generate_id
    @title = title
    @content = content
    @created_at = Time.now
    @slug = title.downcase.gsub(/[^a-z0-9\s]/, '').gsub(/\s+/, '-')
  end

  def to_h
    {
      id: @id,
      title: @title,
      content: @content,
      created_at: @created_at.iso8601,
      slug: @slug
    }
  end

  private

  def generate_id
    Time.now.to_i.to_s + rand(1000).to_s
  end
end
