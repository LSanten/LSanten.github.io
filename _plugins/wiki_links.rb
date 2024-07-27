module Jekyll
  module WikiLinksFilter
    def wikify_links(input)
      # Convert [[wiki-links]] to standard Markdown links
      input.gsub(/\[\[([^\]]+)\]\]/) do
        title = Regexp.last_match(1)
        "[#{title}](#{title.downcase.gsub(' ', '-')}.html)"
      end
    end

    def wikify_images(input)
      # Convert ![[image]] to standard Markdown image syntax
      input.gsub(/\!\[\[([^\]]+)\]\]/) do
        image_path = Regexp.last_match(1)
        "![#{File.basename(image_path, '.*')}](/#{image_path})"
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::WikiLinksFilter)

