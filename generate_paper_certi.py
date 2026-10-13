#!/usr/bin/env python3
"""
generate_paper_certi.py
Universal Publication Proof & Academic Certification Webpage Generator
Part of the Paper Certi Template System
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path

DEFAULT_TEMPLATE_LOCATIONS = [
    Path(__file__).parent / "paper_certi_template.html",
    Path(r"C:\Users\Luci M\.gemini\config\skills\paper-certi\template.html"),
]

def load_template():
    for loc in DEFAULT_TEMPLATE_LOCATIONS:
        if loc.exists():
            with open(loc, "r", encoding="utf-8") as f:
                return f.read()
    raise FileNotFoundError("Could not find paper_certi_template.html in workspace or global skill directory.")

def clean_latex_str(s):
    if not s:
        return ""
    s = re.sub(r'\\textbf\{(.*?)\}', r'<strong>\1</strong>', s)
    s = re.sub(r'\\textit\{(.*?)\}', r'<em>\1</em>', s)
    s = re.sub(r'\\emph\{(.*?)\}', r'<em>\1</em>', s)
    s = re.sub(r'\\textsuperscript\{(.*?)\}', r'<sup>\1</sup>', s)
    s = re.sub(r'\\textsubscript\{(.*?)\}', r'<sub>\1</sub>', s)
    s = re.sub(r'\\%[^\n]*', '', s)
    s = re.sub(r'\\[a-zA-Z]+', '', s)
    s = re.sub(r'[\{\}]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def parse_tex_file(tex_path):
    with open(tex_path, "r", encoding="utf-8") as f:
        content = f.read()

    data = {}
    
    # Extract title
    title_match = re.search(r'\\title\{([^}]+)\}', content, re.DOTALL)
    if not title_match:
        # Check header comments
        for line in content.splitlines()[:20]:
            if "FORMULATION" in line or "Title" in line or line.startswith("%  "):
                title_match = line.strip("% =").strip()
                break
    if title_match:
        raw_title = title_match.group(1) if hasattr(title_match, 'group') else title_match
        data["paper_title"] = clean_latex_str(raw_title)

    # Extract abstract
    abstract_match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', content, re.DOTALL)
    if abstract_match:
        paras = [p.strip() for p in abstract_match.group(1).strip().split('\n\n') if p.strip()]
        data["abstract_html"] = "\n".join([f"<p>{clean_latex_str(p)}</p>" for p in paras])

    # Extract keywords
    kw_match = re.search(r'\\noindent\\textbf\{Keywords:\}\s*(.*?)(?:\n\n|\\section)', content, re.DOTALL)
    if not kw_match:
        kw_match = re.search(r'Keywords:?\s*(.*?)(?:\n\n|\\section)', content)
    if kw_match:
        kws = kw_match.group(1).replace('---', ';').replace('--', ';').split(';')
        data["keywords_html"] = ";<br>\n".join([clean_latex_str(k) for k in kws if k.strip()]) + "."

    return data

def build_citations_object(data):
    apa = data.get("apa_citation", "")
    bib = data.get("bibtex_code", "")
    harvard = data.get("harvard_citation", "")
    
    obj = {
        "apa": apa,
        "bib": bib,
        "harvard": harvard
    }
    return json.dumps(obj, indent=6)

def generate_html(data_dict, template_html=None):
    if template_html is None:
        template_html = load_template()

    # Precompute or fallback values
    d = dict(data_dict)

    # Defaults
    d.setdefault("page_title", f"{d.get('paper_title', 'Research Paper')} — Publication Proof")
    d.setdefault("meta_description", f"Official Publication Proof for {d.get('paper_title', '')} published in {d.get('journal_name', '')}.")
    d.setdefault("live_status_text", f"Verified International Academic Proof • {d.get('journal_short', 'Journal')} Vol. {d.get('volume', '1')} No. {d.get('number', '1')} ({d.get('year', '2026')})")
    d.setdefault("country_name_upper", d.get("country_name", "INTERNATIONAL").upper())
    d.setdefault("country_flag_emoji", "🌐")
    d.setdefault("journal_domain_display", d.get("journal_url", "#").replace("https://", "").replace("http://", "").split("/")[0] + " ↗")
    d.setdefault("journal_emblem_letter", (d.get("journal_name", "J") or "J")[0].upper())
    d.setdefault("journal_name_full", d.get("journal_name", "Academic Journal"))
    d.setdefault("journal_short", "JOURNAL")
    d.setdefault("volume", "1")
    d.setdefault("number", "1")
    d.setdefault("year", "2026")
    d.setdefault("page_range", "1–10")
    d.setdefault("publisher_short", "PRESS")
    d.setdefault("publisher_desc", d.get("publisher_name", "University Press"))
    d.setdefault("hero_badge_category", "International Publication Proof")
    d.setdefault("hero_badge_sub", f"Certified • {d.get('country_name', 'Verified')}")
    d.setdefault("hero_journal_title_html", f"{d.get('journal_name', 'Academic Journal')}")
    d.setdefault("hero_sub_bar_text", f"{d.get('journal_short', 'JOURNAL')} • Vol. {d.get('volume', '1')} • No. {d.get('number', '1')} • {d.get('year', '2026')}")
    d.setdefault("doi_text", d.get("doi_url", d.get("doi", "")))
    d.setdefault("doi_url", d.get("doi_url", "https://doi.org/" + d.get("doi", "")))
    d.setdefault("seal_code", d.get("journal_short", "OFFICIAL"))
    d.setdefault("certificate_id", f"{d.get('journal_short', 'JOURNAL')}-V{d.get('volume', '1')}N{d.get('number', '1')}-{d.get('year', '2026')}-ID")
    d.setdefault("floating_stamp_text", f"&#10003; Published &bull; {d.get('country_name', 'International')}")
    d.setdefault("caption_title", d.get("paper_title", ""))
    d.setdefault("caption_desc", f"Official page proof as it appears in the {d.get('journal_name', '')}, published by {d.get('publisher_name', '')}. Official DOI verified for academic credibility.")
    d.setdefault("sheet_footer_strip_html", f"<span><a href=\"{d.get('journal_url', '#')}\" target=\"_blank\">{d.get('journal_short', '')} &bull; Vol. {d.get('volume', '')} No. {d.get('number', '')} ({d.get('year', '')}) &bull; Page Proof</a></span>\n<a href=\"{d.get('doi_url', '#')}\" target=\"_blank\" class=\"doi-tag\">doi: {d.get('doi', '')} &nearr;</a>")
    
    lead_author = d.get("lead_author_name", "Author")
    d.setdefault("achievement_avatar_letter", lead_author[0].upper())
    d.setdefault("achievement_title", f"Achievement Unlocked &bull; {lead_author}")
    d.setdefault("achievement_tag", "Researcher")
    d.setdefault("achievement_lead_p", f"International Journal Publication in <strong>{d.get('country_name', '')}</strong> &bull; {d.get('journal_name', '')} &bull; {d.get('publisher_name', '')}.")
    d.setdefault("achievement_loc_sub", f"{d.get('publisher_short', 'PRESS')} &bull; {d.get('country_name', '')}")
    d.setdefault("achievement_footer_meta", f"<span>Official proof &bull; For sharing &amp; academic portfolio &bull; Not for commercial reproduction</span>\n<span style=\"font-family:var(--font-mono);\">{d.get('journal_short', '')} {d.get('year', '')} &bull; Verified</span>")

    # Citations JS
    d["js_citations_object"] = build_citations_object(d)

    # Perform token replacement
    rendered = template_html
    for key, val in d.items():
        token = "{{" + key.upper() + "}}"
        rendered = rendered.replace(token, str(val))

    # Also handle lowercase or fallback unmatched tokens cleanly
    leftover = re.findall(r'\{\{([A-Z0-9_]+)\}\}', rendered)
    if leftover:
        print(f"Warning: {len(leftover)} unpopulated tokens remaining: {set(leftover)}")

    return rendered

def main():
    parser = argparse.ArgumentParser(description="Generate Paper Certification & Publication Proof HTML")
    parser.add_argument("--config", "-c", help="Path to paper metadata JSON file")
    parser.add_argument("--tex", "-t", help="Optional LaTeX .tex file to extract metadata from")
    parser.add_argument("--output", "-o", default="paper_proof_generated.html", help="Output HTML file path")
    parser.add_argument("--template", help="Custom template file path")
    args = parser.parse_args()

    data = {}
    if args.config and os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            data = json.load(f)

    if args.tex and os.path.exists(args.tex):
        tex_data = parse_tex_file(args.tex)
        for k, v in tex_data.items():
            if k not in data or not data[k]:
                data[k] = v

    if not data:
        print("No input provided. Using sample Purva data if purva_paper_data.json exists...")
        if os.path.exists("purva_paper_data.json"):
            with open("purva_paper_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            print("Error: Please provide --config <file.json> or --tex <file.tex>")
            sys.exit(1)

    custom_tmpl = None
    if args.template and os.path.exists(args.template):
        with open(args.template, "r", encoding="utf-8") as f:
            custom_tmpl = f.read()

    output_html = generate_html(data, template_html=custom_tmpl)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output_html)

    print(f"Successfully generated publication proof HTML: {args.output} ({len(output_html)} bytes)")

if __name__ == "__main__":
    main()
