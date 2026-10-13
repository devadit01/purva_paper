# Paper Certi Template System

An agency-grade, archival-luxury academic publication proof & digital certificate builder.

## What Has Been Saved

1. **Master HTML Template**:
   - Workspace: [`paper_certi_template.html`](file:///c:/Users/Luci%20M/OneDrive/Desktop/paper_purva/paper_certi_template.html)
   - Global Skill: `C:\Users\Luci M\.gemini\config\skills\paper-certi\template.html`
   - Features: Archival typography (Fraunces + Plus Jakarta Sans + JetBrains Mono), tactile skeuomorphic paper sheet (washi tape, push pin, perforation), live verification top bar, bento grid proof, 4 interactive tabs, golden wax seal, editorial verification modal, 1-click citation copier (APA, BibTeX, Harvard), achievement unlocked card, and print-ready CSS (`@media print`).

2. **Python Automated Builder CLI**:
   - Workspace: [`generate_paper_certi.py`](file:///c:/Users/Luci%20M/OneDrive/Desktop/paper_purva/generate_paper_certi.py)
   - Global Skill: `C:\Users\Luci M\.gemini\config\skills\paper-certi\generate_paper_certi.py`
   - Generates the complete standalone HTML publication proof in under 1 second from any JSON or LaTeX file.

3. **Data Schema & Working Example**:
   - Schema: [`paper_certi_schema.json`](file:///c:/Users/Luci%20M/OneDrive/Desktop/paper_purva/paper_certi_schema.json)
   - Example Data (Purva Chordia): [`purva_paper_data.json`](file:///c:/Users/Luci%20M/OneDrive/Desktop/paper_purva/purva_paper_data.json)

4. **Global Persistent Skill (`paper-certi`)**:
   - Registered at: `C:\Users\Luci M\.gemini\config\skills\paper-certi\SKILL.md`
   - The AI assistant is permanently equipped to automatically build paper certification proof pages whenever you provide any new paper in any folder.

## How To Use Next Time

Whenever you have a new paper (LaTeX `.tex`, BibTeX `.bib`, PDF text, or markdown), you can simply tell the assistant:
> *"Build a paper_certi for this paper"* or *"Create a publication proof for this paper"*

Or run the CLI directly:
```bash
python generate_paper_certi.py --config my_new_paper_data.json --output my_new_paper_proof.html
```
Or extract directly from a `.tex` file:
```bash
python generate_paper_certi.py --tex my_paper.tex --output my_new_paper_proof.html
```
