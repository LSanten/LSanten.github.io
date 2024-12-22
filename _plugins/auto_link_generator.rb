module Jekyll
  class AutoLinkGenerator < Generator
    def generate(site)
      puts "AutoLinkGenerator is running"
      
      process_files(site.pages)
      process_files(site.posts.docs)
      process_collection_files(site.collections['mms-md'].docs)
    end

    def process_files(files)
      files.each do |file|
        #puts "Processing file: #{file.path}"
        file.content = autolink(file.content)
      end
    end

    def process_collection_files(files)
      files.each do |file|
        #puts "Processing collection file: #{file.path}"
        file.content = autolink(file.content)
      end
    end

    def autolink(input)
      #puts "Processing content"

      # Regular expression to detect plain URLs not within Markdown links or HTML tags
      url_regex = %r{
        (?<!\[)          # Negative lookbehind to ensure the URL is not preceded by '['
        (?<!\]\()        # Negative lookbehind to ensure the URL is not preceded by ']('
        (?<!["'])        # Negative lookbehind to ensure the URL is not inside an HTML attribute value
        \b               # Word boundary
        (https?:\/\/     # Match http or https protocol
          [^\s()<>\[\]]+ # Match non-space characters, excluding parentheses and brackets
          (?:\/[^\s()<>\[\]]*)* # Ensure the trailing characters like / are included
        )\/?             # Ensure trailing slash is included
        (?![^\s]*\])     # Negative lookahead to ensure the URL is not followed by 'anything till a closing bracket'
        (?!["'])         # Negative lookahead to ensure the URL is not followed by ' or "
      }x

      # Process content outside of HTML tags
      input = input.gsub(/(<[^>]+>)/) { |match| "SPLIT#{match}SPLIT" }
      parts = input.split("SPLIT")

      parts.map! do |part|
        if part.match(/<[^>]+>/) # Skip HTML tags
          part
        else
          part.gsub(url_regex) do |url|
            #puts "Found URL: #{url}"
            "<a href=\"#{url}\" target=\"_blank\">#{url}</a>"
          end
        end
      end

      parts.join
    end
  end
end
