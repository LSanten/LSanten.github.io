module Jekyll
  class AutoTitleSubtitleGenerator < Generator
    def generate(site)
      site.pages.each do |page|
        next unless page.extname == '.md' # Only process markdown files

        content = page.content
        lines = content.lines.map(&:strip) # Split content into lines and strip whitespace

        # Initialize title and subtitle
        title = nil
        subtitle = nil

        lines.each_with_index do |line, index|
          # Check for the first # heading
          if line.start_with?('# ') && title.nil?
            title = line.sub(/^# /, '').strip
            # Check if the next line is a ## heading for the subtitle
            next_line = lines[index + 1] || ''
            if next_line.start_with?('## ')
              subtitle = next_line.sub(/^## /, '').strip
            end
            break # Stop after finding the first title and subtitle pair
          end
        end

        # Update the page's data
        page.data['title'] = title if title
        page.data['subtitle'] = subtitle if subtitle
      end
    end
  end
end
