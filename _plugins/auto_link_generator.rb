module Jekyll
  class AutoLinkGenerator < Generator
    def generate(site)
      site.pages.each do |page|
        page.content = autolink(page.content)
      end

      site.posts.docs.each do |post|
        post.content = autolink(post.content)
      end
    end

    def autolink(input)
      # Regular expression to detect plain URLs
      url_regex = %r{
        (                           # Capture 1: entire matched URL
          (?:
            https?:\/\/             # http or https protocol
            |                       #   or
            www\d{0,3}[.]           # "www.", "www1.", "www2." ... "www999."
            |                       #   or
            [a-z0-9.\-]+[.][a-z]{2,4}\/  # looks like domain name followed by a slash
          )
          (?:                       # One or more:
            [^\s()<>]+              # Run of non-space, non-()<>
            |                       #   or
            \(([^()\s<>]+|(\([^()\s<>]+\)))\)  # balanced parens, up to 2 levels
          )+
          (?:                       # End with:
            \(([^()\s<>]+|(\([^()\s<>]+\)))\)  # balanced parens, up to 2 levels
            |                       #   or
            [^\s`!()\[\]{};:'".,<>?«»“”‘’]        # not a space or one of these punct chars
          )
        )
      }x

      input.gsub(url_regex) do |url|
        # Ensure the URL has a protocol prefix
        link = url.match(%r{^https?://}) ? url : "http://#{url}"
        "<a href=\"#{link}\" target=\"_blank\">#{url}</a>"
      end
    end
  end
end
