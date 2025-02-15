require 'nokogiri'

module Jekyll
  module ExcerptFilter
    def extract_first_paragraph(input)
      # Parse HTML content
      doc = Nokogiri::HTML.fragment(input)

      # Find the first meaningful paragraph
      first_paragraph = doc.css('p').find { |p| !p.text.strip.empty? }

      # Extract plain text, removing any remaining HTML
      first_paragraph ? first_paragraph.text.strip : ""
    end
  end
end

Liquid::Template.register_filter(Jekyll::ExcerptFilter)
