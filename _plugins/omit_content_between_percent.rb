# _plugins/omit_content_between_percent.rb

Jekyll::Hooks.register [:pages, :documents], :pre_render do |doc|
  # Check if the document's output extension is .html
  if doc.output_ext == ".html"
    # Log to confirm that the hook is running
    #puts "Processing document: #{doc.relative_path}"

    # Replace all content between %%...%% with an empty string
    if doc.content.match(/%%.*?%%/m)
      doc.content = doc.content.gsub(/%%.*?%%/m, '')
      #puts "Modified content: #{doc.content}"
    end
  end
end
