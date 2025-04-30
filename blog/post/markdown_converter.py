import re
import markdown

class ObsidianMarkdownConverter:
    def __init__(self, base_url="/", media_url="/media/"):
        """
        Initializes the converter.
        :param base_url:  The base URL for internal links (e.g., "/notes/").
        :param media_url: The URL where media files are served (e.g., "/media/").
        """
        self.base_url = base_url
        self.media_url = media_url
        self.code_blocks = []  # Store extracted code blocks

    def convert(self, md_text):
        """
        Converts Obsidian Markdown to HTML.
        """

        # 0. Extract code blocks first to prevent interference
        md_text = self._extract_code_blocks(md_text)

        # 1. Handle Embedded Images with optional width and height
        md_text = re.sub(
            r'!\[\[([^\]|]+)(?:\|([^\]]+))?\]\]',
            lambda match: self._convert_embed(match.group(1), match.group(2), is_image=True),
            md_text
        )

        # 2. Handle Embedded Files (including PDFs, etc.)
        md_text = re.sub(
            r'!\[\[([^\]|]+)(?:\|([^\]]+))?\]\]',  # Reuse the pattern, handle in _convert_embed
            lambda match: self._convert_embed(match.group(1), match.group(2), is_image=False),
            md_text
        )

        # 3. Handle Internal Links [[Page Name]] or [[Page Name|Alias]]
        md_text = re.sub(
            r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]',
            lambda match: self._convert_wikilink(match.group(1), match.group(2)),
            md_text
        )

        # 4. Handle Highlighted text ==highlight==
        md_text = re.sub(
            r'==(.+?)==',
            r'<mark>\1</mark>',
            md_text
        )

        # 5. Handle standard markdown links for internal pages [text](page)
        md_text = re.sub(
            r'\[([^\]]+)\]\(([^http://|https://|#][^)]*)\)',
            lambda match: self._convert_standard_link(match.group(1), match.group(2)),
            md_text
        )

        # 6. Handle Callouts > [!TYPE]
        md_text = re.sub(
            r'> +\[!([A-Z]+)\] +',
            lambda match: self._convert_callout(match.group(1)),
            md_text,
        )

        # 7. Handle Tags  #tag or #tag/subtag
        md_text = re.sub(
            r'(#[\w\/]+)',
            lambda match: self._convert_tag(match.group(1)),
            md_text
        )

        # 8. Handle Math formulas (inline)
        md_text = re.sub(
            r'\$([^\$]+)\$',
            r'<span class="math">\1</span>',  # Use a class for styling
            md_text
        )

        # 9. Handle Math formulas (block)
        md_text = re.sub(
            r'\$\$([^\$]+)\$\$',
            r'<div class="math-block">\1</div>', # Use a class for styling
            md_text
        )

       # 10. Handle Checkboxes - [ ] and - [x]
        md_text = re.sub(
            r'- +\[( |x|X)\] +',
            lambda match: self._convert_checkbox(match.group(1)),
            md_text
        )
        # 12. Convert the rest of Markdown into HTML
        html = markdown.markdown(md_text, extensions=['extra'])

        # 13.  Replace placeholders with the extracted code blocks
        html = self._replace_code_placeholders(html)
        return html

    def _extract_code_blocks(self, md_text):
        """
        Extracts code blocks from the Markdown text and replaces them with placeholders.
        This prevents markdown from misinterpreting the code block content.
        """
        self.code_blocks = []

        def _replace_code(match):
            language = match.group(1) or ''
            code = match.group(2)
            placeholder = f'__CODEBLOCK_{len(self.code_blocks)}__'
            self.code_blocks.append({'language': language.strip(), 'code': code.strip()})  # Remove extra spaces
            return placeholder

        md_text = re.sub(r'```(\w+)?\n([\s\S]*?)\n```', _replace_code, md_text, flags=re.MULTILINE)
        return md_text

    def _replace_code_placeholders(self, html):
        """
        Replaces the placeholders in the HTML with the actual code blocks.
        """
        for i, code_block in enumerate(self.code_blocks):
            placeholder = f'__CODEBLOCK_{i}__'
            html = html.replace(placeholder, self._convert_code_block(code_block['language'], code_block['code']))
        return html


    def _convert_embed(self, file_path, size_info, is_image):
        """
        Handles embedded files (images, PDFs, etc.) with optional size parameters.
        """
        style = ""
        if size_info:
            if 'x' in size_info:
                width, height = size_info.split('x')
                style = f' style="width:{width}px; height:{height}px;"'
            elif 'width=' in size_info:
                width = size_info.replace('width=', '')
                style = f' style="width:{width}px;"'
            elif 'height=' in size_info:
                height = size_info.replace('height=', '')
                style = f' style="height:{height}px;"'
            elif size_info.isdigit():
                style = f' style="width:{size_info}px;"'

        if is_image:
            return f'<img src="{self.media_url}{file_path}" alt="{file_path}"{style}>'
        else:
            return f'<a href="{self.media_url}{file_path}">{file_path}</a>'  # Or use an appropriate viewer

    def _convert_wikilink(self, link_text, alias=None):
        """
        Converts Obsidian wikilink text into HTML <a> tag.
        Handles aliases.
        """
        display_text = alias if alias else link_text
        page_slug = link_text.strip().replace(' ', '-').lower()
        return f'<a href="{self.base_url}{page_slug}/">{display_text}</a>'

    def _convert_standard_link(self, text, link):
        """
        Converts standard markdown links to internal pages.
        """
        page_slug = link.strip().replace(' ', '-').lower()
        if not page_slug.startswith('/'):
            page_slug = f'{self.base_url}{page_slug}'
        return f'<a href="{page_slug}/">{text}</a>'

    def _convert_callout(self, callout_type):
        """
        Converts Obsidian callouts to HTML.  You can expand this to handle different types.
        """
        #  You'll likely want to map Obsidian's type names to CSS classes.
        callout_classes = {
            "INFO": "callout-info",
            "WARNING": "callout-warning",
            "NOTE": "callout-note",
            # Add more as needed
        }
        css_class = callout_classes.get(callout_type, "callout")  # Default class
        return f'<div class="{css_class}">'  #  Close this <div> in another regex, or in post-processing

    def _convert_tag(self, tag):
        """
        Converts Obsidian tags to HTML.
        """
        return f'<span class="tag">{tag}</span>' #  Use a class for styling

    def _convert_checkbox(self, checked):
        """
        Converts Obsidian checkboxes to HTML input elements.
        """
        checked_attr = 'checked' if checked.lower() == 'x' else ''
        return f'<input type="checkbox" {checked_attr} disabled>' # disabled so they are not interactive

    def _convert_code_block(self, language, code):
        """
        Converts Obsidian code blocks to HTML, including language class.
        """
        if language:
            return f'<pre><code class="language-{language}">{code.strip()}</code></pre>'
        else:
            return f'<pre><code>{code.strip()}</code></pre>'
