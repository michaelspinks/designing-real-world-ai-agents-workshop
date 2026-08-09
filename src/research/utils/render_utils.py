"""Render research.md into a distribution-ready HTML file or a reMarkable-sized PDF."""

import html
import logging
import re

import markdown as md
from weasyprint import HTML as WeasyHTML

from research.config.render_styles import DISTRIBUTION_CSS, REMARKABLE_PDF_CSS

logger = logging.getLogger(__name__)

# `extra` covers tables/fenced code/footnotes; `md_in_html` lets markdown
# render *inside* the <details>/<summary> blocks that research.md uses for
# collapsible sections (see markdown_utils.markdown_collapsible); `toc`
# assigns heading ids and exposes a nav tree; `sane_lists` avoids merging
# differently-marked adjacent lists.
_MARKDOWN_EXTENSIONS = ["extra", "md_in_html", "toc", "sane_lists"]

_LEADING_RESEARCH_HEADING = re.compile(r"^#\s+Research\s*\n")


def slug_to_title(slug: str) -> str:
    """Turn an outputs/ slug (e.g. 'llm-agent-patterns') into a display title."""

    return slug.replace("-", " ").replace("_", " ").strip().title()


def _prepare_markdown(markdown_text: str, title: str) -> str:
    """Swap the generic '# Research' heading for the real title, force every
    collapsible <details> section open (a distributed report should read as
    a complete document, not a click-to-reveal one), and opt those sections
    into markdown parsing — the md_in_html extension otherwise treats HTML
    block content as opaque and leaves nested **bold**/links unrendered."""

    text = markdown_text.replace("<details>", '<details open markdown="1">')
    if _LEADING_RESEARCH_HEADING.match(text):
        text = _LEADING_RESEARCH_HEADING.sub(f"# {title}\n", text, count=1)
    return text


def _convert_to_html(markdown_text: str, title: str) -> tuple[str, str]:
    """Convert research.md content to an HTML body fragment and a TOC fragment."""

    converter = md.Markdown(extensions=_MARKDOWN_EXTENSIONS, output_format="html5")
    body_html = converter.convert(_prepare_markdown(markdown_text, title))
    toc_html = getattr(converter, "toc", "")
    return body_html, toc_html


def render_distribution_html(markdown_text: str, title: str) -> str:
    """Wrap research.md content into a standalone, self-styled HTML document."""

    body_html, toc_html = _convert_to_html(markdown_text, title)
    toc_block = (
        f'<details class="toc-wrapper" open><summary>Contents</summary>{toc_html}</details>'
        if toc_html
        else ""
    )
    escaped_title = html.escape(title)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escaped_title}</title>
<style>{DISTRIBUTION_CSS}</style>
</head>
<body>
<article>
{toc_block}
{body_html}
</article>
</body>
</html>
"""


def render_remarkable_pdf(markdown_text: str, title: str) -> bytes:
    """Render research.md content into a PDF sized for the reMarkable 2 screen."""

    body_html, _ = _convert_to_html(markdown_text, title)
    escaped_title = html.escape(title)

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{escaped_title}</title>
<style>{REMARKABLE_PDF_CSS}</style>
</head>
<body>
<article>
{body_html}
</article>
</body>
</html>
"""
    # weasyprint/fontTools log routine rendering/font-subsetting steps at
    # INFO regardless of this module's own logger levels; logging.disable()
    # is the one reliable way to silence them. CSS is parsed as early as
    # HTML(...) construction, so disable before that, not just around
    # write_pdf().
    logging.disable(logging.INFO)
    try:
        return WeasyHTML(string=document).write_pdf()
    finally:
        logging.disable(logging.NOTSET)
