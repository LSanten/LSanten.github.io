Jekyll::Hooks.register :documents, :post_render do |document|
  if document.output_ext == '.html'
    document.output = document.output.gsub(/<img src="(media\/.*?)"/) do |match|
      path = $1
      # Adjust the path to add '../' before media
      %Q(<img src="#{File.join('..', path)}")
    end
  end
end
