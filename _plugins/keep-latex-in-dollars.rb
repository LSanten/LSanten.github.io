module Jekyll
  class KeepLatexConverter < Converter
    safe true
    priority :highest  # Runs before Jekyll's default Markdown conversion

    def matches(ext)
      ext =~ /^\.md$/i
    end

    def output_ext(ext)
      ".md" # Keep file as Markdown
    end

    def convert(content)
      # Preserve `$$ ... $$` in Markdown before Jekyll processes it
      content.gsub(/\$\$(.*?)\$\$/m, 'MATH_BLOCK_START\1MATH_BLOCK_END')
    end
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  if doc.output_ext == ".html" # Ensure it only runs on final HTML files
    doc.output.gsub!("MATH_BLOCK_START", "$$")
    doc.output.gsub!("MATH_BLOCK_END", "$$")
  end
end
