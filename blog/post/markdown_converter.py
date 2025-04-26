import re
import markdown

class ObsidianMarkdownConverter:
    def __init__(self):
        pass

    def convert(self, md_text):
        # 1. Handle Embedded Images with optional width and height
        # Format: ![[image.png|100x200]] or ![[image.png|width=100]] or ![[image.png|height=200]]
        md_text = re.sub(
            r'!\[\[([^\]|]+)(?:\|([^\]]+))?\]\]',
            lambda match: self._convert_image(match.group(1), match.group(2)),
            md_text
        )

        # 2. Handle Internal Links [[Page Name]]
        md_text = re.sub(
            r'\[\[([^\]]+)\]\]',
            lambda match: self._convert_wikilink(match.group(1)),
            md_text
        )

        # 3. Handle Highlighted text ==highlight==
        md_text = re.sub(
            r'==(.+?)==',
            r'<mark>\1</mark>',
            md_text
        )
        
        # 4. Handle standard markdown links for internal pages [text](page)
        md_text = re.sub(
            r'\[([^\]]+)\]\(([^http://|https://|#][^)]*)\)',
            lambda match: self._convert_standard_link(match.group(1), match.group(2)),
            md_text
        )

        # 5. Convert the rest of Markdown into HTML
        html = markdown.markdown(md_text, extensions=['extra'])

        return html

    def _convert_image(self, image_path, size_info=None):
        """Converts Obsidian image syntax with optional size parameters."""
        style = ""
        
        if size_info:
            # Handle different size formats
            if 'x' in size_info:  # Format: 100x200
                width, height = size_info.split('x')
                style = f' style="width:{width}px; height:{height}px;"'
            elif 'width=' in size_info:  # Format: width=100
                width = size_info.replace('width=', '')
                style = f' style="width:{width}px;"'
            elif 'height=' in size_info:  # Format: height=200
                height = size_info.replace('height=', '')
                style = f' style="height:{height}px;"'
            elif size_info.isdigit():  # Format: 300 (just width)
                style = f' style="width:{size_info}px;"'
        
        return f'<img src="/media/{image_path}" alt="{image_path}"{style}>'

    def _convert_wikilink(self, link_text):
        """Converts Obsidian wikilink text into HTML <a> tag."""
        page_slug = link_text.strip().replace(' ', '-').lower()
        return f'<a href="/{page_slug}/">{link_text}</a>'
        
    def _convert_standard_link(self, text, link):
        """Converts standard markdown links to internal pages."""
        page_slug = link.strip().replace(' ', '-').lower()
        if not page_slug.startswith('/'):
            page_slug = f'/{page_slug}'
        return f'<a href="{page_slug}/">{text}</a>'