module Jekyll
  module WikiLinksFilter
    def wikify_links(input)
      # Convert [[wiki-links]] to standard Markdown links
      input.gsub(/\[\[([^\]]+)\]\]/) do
        title = Regexp.last_match(1)
        "<a href=\"../#{title}/\">#{title}</a>"
      end
    end

    def wikify_images(input)
      # Convert ![[image]] to standard Markdown image syntax
      input.gsub(/\!\[\[([^\]]+)\]\]/) do
        image_path = Regexp.last_match(1)
        "<img src=\"/#{image_path}\" alt=\"#{File.basename(image_path, '.*')}\">"
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::WikiLinksFilter)
