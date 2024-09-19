
require 'kramdown'
require 'nokogiri'

module Jekyll
  class CustomMarkdownWithRenderer < Converter
    safe true
    priority :low

    def matches(ext)
      ext =~ /^\.md$/i
    end

    def output_ext(ext)
      '.html'
    end

    def convert(content)
      doc = Kramdown::Document.new(content, input: 'GFM')
      html = doc.to_html
      adjust_links(html)
    end

    private

    def adjust_links(html)
      doc = Nokogiri::HTML::DocumentFragment.parse(html)
      doc.css('a').each do |link|
        href = link['href']
        if href =~ /^http/
          link.set_attribute('target', '_blank')
        elsif href =~ /\.md$/
          # Adjust internal markdown link to folder format
          folder_name = href.sub('.md', '').split('/').last
          link.set_attribute('href', "../#{folder_name}/")
        end
      end
      doc.to_html
    end
  end
end