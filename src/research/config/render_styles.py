"""CSS templates for rendering research.md into HTML and PDF."""

# Shared rules: long grounding-redirect URLs and code must never overflow
# the page/viewport, since research.md sources routinely contain very long
# unbroken links.
_SHARED_OVERFLOW_RULES = """
  a, code, pre { overflow-wrap: anywhere; }
  pre { white-space: pre-wrap; }
"""

# Standalone HTML for sharing/distribution — screen-first, light/dark aware.
DISTRIBUTION_CSS = f"""
  :root {{ color-scheme: light dark; }}
  body {{
    margin: 0;
    padding: 2.5rem 1.25rem;
    background: #ffffff;
    color: #1a1a1a;
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    line-height: 1.65;
  }}
  article {{ max-width: 46rem; margin: 0 auto; }}
  h1, h2, h3, h4 {{ line-height: 1.3; margin-top: 2em; margin-bottom: 0.6em; }}
  h1 {{ font-size: 2rem; border-bottom: 2px solid #ddd; padding-bottom: 0.4em; }}
  h2 {{ font-size: 1.5rem; border-bottom: 1px solid #eee; padding-bottom: 0.3em; }}
  h3 {{ font-size: 1.2rem; }}
  p, ul, ol {{ margin: 0.9em 0; }}
  li {{ margin: 0.3em 0; }}
  a {{ color: #0b5fff; text-decoration: underline; }}
  strong {{ color: #000; }}
  code {{
    background: #f2f2f2; padding: 0.15em 0.4em; border-radius: 4px;
    font-size: 0.9em; font-family: ui-monospace, "SF Mono", Consolas, monospace;
  }}
  pre {{ background: #f2f2f2; padding: 1em; border-radius: 8px; overflow-x: auto; }}
  pre code {{ background: none; padding: 0; }}
  blockquote {{
    margin: 1em 0; padding: 0.2em 1em; border-left: 4px solid #ddd; color: #555;
  }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 2em 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
  th, td {{ border: 1px solid #ddd; padding: 0.5em 0.75em; text-align: left; }}
  th {{ background: #f7f7f7; }}
  details {{
    background: #f7f8fa; border: 1px solid #e2e4e8; border-radius: 8px;
    padding: 0.75em 1em; margin: 1em 0;
  }}
  summary {{
    font-weight: 600; cursor: pointer; margin: -0.75em -1em; padding: 0.75em 1em;
  }}
  details[open] summary {{ margin-bottom: 0.75em; border-bottom: 1px solid #e2e4e8; }}
  details.toc-wrapper {{
    background: #f7f8fa; border: 1px solid #e2e4e8; border-radius: 8px;
    padding: 0.5em 1.25em; margin: 1.5em 0;
  }}
  details.toc-wrapper ul {{ padding-left: 1.25em; }}
  details.toc-wrapper > summary {{ margin: -0.5em -1.25em; padding: 0.5em 1.25em; }}
  details.toc-wrapper .toc > ul {{ margin: 0; }}
  {_SHARED_OVERFLOW_RULES}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #14161a; color: #e6e6e6; }}
    h1 {{ border-bottom-color: #333; }}
    h2 {{ border-bottom-color: #2a2a2a; }}
    a {{ color: #6ea8ff; }}
    strong {{ color: #fff; }}
    code, pre {{ background: #1e2126; }}
    blockquote {{ border-left-color: #444; color: #aaa; }}
    hr {{ border-top-color: #333; }}
    th, td {{ border-color: #333; }}
    th {{ background: #1e2126; }}
    details, details.toc-wrapper {{ background: #1a1d22; border-color: #2a2d33; }}
    details[open] summary {{ border-bottom-color: #2a2d33; }}
  }}
"""

# PDF for the reMarkable 2 — physical screen is 157.2mm x 209.6mm. Always
# black-on-white (e-ink, no dark mode) with margins and type sized for
# comfortable reading/annotating on the device.
REMARKABLE_PDF_CSS = f"""
  @page {{
    size: 157mm 210mm;
    margin: 14mm 11mm 16mm 11mm;
  }}
  body {{
    background: #ffffff;
    color: #000000;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.5;
    orphans: 3;
    widows: 3;
  }}
  h1, h2, h3, h4 {{
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    line-height: 1.25;
    break-after: avoid-page;
    margin-top: 1.4em;
    margin-bottom: 0.5em;
  }}
  h1 {{ font-size: 20pt; bookmark-level: 1; }}
  h2 {{ font-size: 15pt; bookmark-level: 2; }}
  h3 {{ font-size: 13pt; bookmark-level: 3; }}
  h4 {{ font-size: 11.5pt; bookmark-level: 4; }}
  p, ul, ol {{ margin: 0.7em 0; }}
  li {{ margin: 0.25em 0; }}
  a {{ color: #000000; text-decoration: underline; }}
  code {{
    font-family: "Courier New", monospace; font-size: 0.85em;
    background: #eeeeee;
  }}
  pre {{ background: #eeeeee; padding: 0.6em; break-inside: avoid; }}
  pre code {{ background: none; }}
  blockquote {{ margin: 0.8em 0; padding-left: 0.8em; border-left: 3px solid #999; }}
  hr {{ border: none; border-top: 1px solid #999; margin: 1.5em 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 0.8em 0; break-inside: avoid; }}
  th, td {{ border: 1px solid #999; padding: 0.3em 0.5em; }}
  details {{ border: 1px solid #999; padding: 0.5em 0.75em; margin: 0.8em 0; }}
  summary {{ font-weight: bold; }}
  {_SHARED_OVERFLOW_RULES}
"""
