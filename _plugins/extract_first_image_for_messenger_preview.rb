module Jekyll
  class ExtractImages < Jekyll::Generator
    priority :low

    def generate(site)
      # Access the custom collection 'mms-md'
      mms_docs = site.collections['mms-md'].docs

      mms_docs.each do |doc|
        # Skip if images are already defined in front matter
        next unless doc.data['images'].nil? || doc.data['images'].empty?

        # Extract all images from the content
        all_images = doc.content.scan(/!\[.*?\]\((.*?)\)/).flatten

        if all_images.any?
          # Save only the first image, adjusted for relative path
          first_image = "../#{all_images.first}"
          doc.data['images'] = [first_image]
        else
          Jekyll.logger.info "ExtractImages:", "No image found for #{doc.url}"
        end
      end
    end
  end
end
