"""Render a research.md file into a distribution HTML file and/or a
reMarkable-2-sized PDF.

Usage:
    uv run python scripts/render_research.py --slug llm-agent-patterns
    uv run python scripts/render_research.py --slug llm-agent-patterns --format pdf
    uv run python scripts/render_research.py --input path/to/research.md --format html
"""

import logging
import sys
from pathlib import Path

import click

from research.utils.file_utils import read_file, write_file
from research.utils.render_utils import (
    render_distribution_html,
    render_remarkable_pdf,
    slug_to_title,
)

logger = logging.getLogger(__name__)

OUTPUTS_DIR = Path(__file__).parent.parent / "outputs"


@click.command()
@click.option(
    "--slug",
    help="Folder name under outputs/ containing research.md "
    "(reads outputs/<slug>/research.md, writes alongside it).",
)
@click.option(
    "--input",
    "input_path",
    type=click.Path(exists=True, dir_okay=False),
    help="Explicit path to a research.md file (alternative to --slug).",
)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False),
    help="Directory to write the rendered file(s) into (default: alongside the input).",
)
@click.option(
    "--title",
    help="Document title (default: derived from --slug, or 'Research' for --input).",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["html", "pdf", "both"]),
    default="both",
    help="Which output(s) to render (default: both).",
)
def main(
    slug: str | None,
    input_path: str | None,
    output_dir: str | None,
    title: str | None,
    output_format: str,
) -> None:
    """Render research.md into distribution HTML and/or a reMarkable PDF."""

    if not slug and not input_path:
        print("ERROR: pass either --slug or --input.")
        sys.exit(1)

    if slug:
        source_path = OUTPUTS_DIR / slug / "research.md"
        default_title = slug_to_title(slug)
    else:
        source_path = Path(input_path)
        default_title = "Research"

    if not source_path.exists():
        print(f"ERROR: {source_path} not found.")
        sys.exit(1)

    markdown_text = read_file(source_path)
    if not markdown_text.strip():
        print(f"ERROR: {source_path} is empty.")
        sys.exit(1)

    doc_title = title or default_title
    dest_dir = Path(output_dir) if output_dir else source_path.parent

    if output_format in ("html", "both"):
        html_doc = render_distribution_html(markdown_text, doc_title)
        html_path = dest_dir / "research.html"
        write_file(html_path, html_doc)
        print(f"Wrote HTML: {html_path.resolve()}")

    if output_format in ("pdf", "both"):
        pdf_bytes = render_remarkable_pdf(markdown_text, doc_title)
        pdf_path = dest_dir / "research.pdf"
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_bytes(pdf_bytes)
        print(f"Wrote PDF ({len(pdf_bytes):,} bytes): {pdf_path.resolve()}")


if __name__ == "__main__":
    main()
