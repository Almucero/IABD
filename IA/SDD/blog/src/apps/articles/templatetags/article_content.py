from django import template
from django.utils.html import format_html, format_html_join

register = template.Library()


@register.filter
def article_content(value):
    """Render plain-text paragraphs and lines prefixed with '## ' as headings."""
    rendered_blocks = []
    for block in str(value).split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if block.startswith("## "):
            rendered_blocks.append(format_html("<h2>{}</h2>", block[3:].strip()))
            continue

        lines = (line.strip() for line in block.splitlines() if line.strip())
        paragraph = format_html_join("<br>", "{}", ((line,) for line in lines))
        rendered_blocks.append(format_html("<p>{}</p>", paragraph))

    return format_html_join("", "{}", ((block,) for block in rendered_blocks))
