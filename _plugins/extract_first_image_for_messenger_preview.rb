require 'json'

module Jekyll
  class UpdateFrontmatterWithImage < Jekyll::Generator
    priority :low

    def generate(site)
      # Load the JSON file
      json_file_path = File.join(site.source, 'marble-thumbnails', 'image_mapping.json')
      image_mapping = JSON.parse(File.read(json_file_path))

      # Access the custom collection 'mms-md'
      mms_docs = site.collections['mms-md'].docs

      mms_docs.each do |doc|
        # Skip if images are already defined in front matter
        next unless doc.data['images'].nil? || doc.data['images'].empty?

        # Get the Markdown filename without extension
        markdown_filename = File.basename(doc.basename, '.md')

        # Assign the image link from the JSON mapping
        if image_mapping.key?(markdown_filename)
          doc.data['images'] = [image_mapping[markdown_filename]]
        else
          doc.data['images'] = [] # Leave empty if no mapping exists
        end
      end
    end
  end
end
