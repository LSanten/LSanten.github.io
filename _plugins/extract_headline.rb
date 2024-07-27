Jekyll::Hooks.register :documents, :pre_render do |document|
  if document.extname == '.md'
    # Store the original filename without the extension
    document.data['file_name'] = File.basename(document.relative_path, File.extname(document.relative_path))
    
    # Extract the first headline as the title
    content = document.content
    if content =~ /^#\s+(.+)$/
      document.data['title'] = $1
    end
  end
end

