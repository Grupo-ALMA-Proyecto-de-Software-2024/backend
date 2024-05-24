import markdown
from django.utils.html import mark_safe


def markdown_to_html(markdown_text: str) -> str:
    return mark_safe(markdown.markdown(markdown_text))
