#!/usr/bin/env python3
"""Build the anonymized TMLR submission from draft/paper.tex.

    cd submission/tmlr && python3 make_tmlr.py && pdflatex main; bibtex main; pdflatex main; pdflatex main

The ACM draft stays the single source; this script rewrites the preamble,
hides the authors, switches to natbib author-year citations and anonymizes
the authors' own entries; and writes supplement.zip, the anonymised audit data
and evidence to upload as supplementary material on OpenReview.
"""
import re
import subprocess
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SRC = ROOT / "draft" / "paper.tex"

# released files go to reviewers as supplementary material instead of a (de-anonymising) repository link
SUPPLEMENT = ["audit", "review/README.md", "review/sweep-2026-10-22.md", "review/ref-check.md", "review/refcheck-fixlog.md", "review/upgrades.md",
              "review/bibparse.py", "review/check_bib.py", "review/fetch_meta.py", "review/fetch_s2_batch.py",
              "review/fetch_crossref.py", "review/compare_meta.py", "review/upgrades.py", "review/bib_static.json",
              "review/meta.json", "review/meta_report.json"]
IDENTIFYING = ("Shanglin", "Zhan Shi", "shangliy", "kudoysl", "ashi2@")

PREAMBLE = r"""\pdfinfoomitdate=1\pdftrailerid{}
\documentclass[10pt]{article}
\usepackage{tmlr}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=blue!50!black,citecolor=blue!50!black,urlcolor=blue!50!black}
\usepackage{url}
\usepackage{xurl}
\usepackage{rotating}
\usepackage[section]{placeins}
% the ACM text block is wider than TMLR's: figures are scaled to 0.92 and table padding shrunk
\setlength{\tabcolsep}{4pt}
"""


def sub_once(pattern, repl, text, flags=0):
    new, n = re.subn(pattern, lambda m: repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"pattern not found: {pattern}")
    return new


def build_tex():
    tex = SRC.read_text()
    tex = sub_once(r"\\documentclass\[[^\]]*\]\{acmart\}\n", PREAMBLE, tex)
    # authors -> anonymous; tmlr prints the title block from \maketitle
    tex = sub_once(r"\\author\{.*?(?=\\begin\{abstract\})",
                   "\\author{Anonymous authors}\n\n\\begin{document}\n\\maketitle\n\n", tex, re.S)
    tex = sub_once(r"\\begin\{document\}\n", "", tex)  # the original one, before \title
    tex = sub_once(r"\\keywords\{[^\n]*\}\n", "", tex)
    tex = sub_once(r"\n\\maketitle\n(?=\n%=)", "\n", tex)
    # natbib author-year: every citation in the draft is parenthetical
    tex = tex.replace("\\cite{", "\\citep{")
    # the audit-data footnote points at the supplementary material
    tex = sub_once(r"\\footnote\{\\url\{https://github\.com/shangliy/recforge/tree/[^}]*\}\}",
                   "\\footnote{In the supplementary material.}", tex)
    # the authors' own regularisation paper, cited as an excluded example
    tex = sub_once(r" \(such as offline LLM pairwise supervision applied only where a gate on history length,\n"
                   r"item popularity and model uncertainty predicts it is reliable~\\citep\{shi2026selective\}\)", "", tex)
    # the reference implementation is named only in the camera-ready version
    tex = sub_once(r"describes recforge~\\citep\{recforge\}, a\nreference implementation",
                   "describes a\nreference implementation~\\citep{recforge}", tex)
    tex = sub_once(r"The authors are building recforge, the reference implementation", "The authors are building the reference implementation", tex)
    tex = sub_once(r"but recforge enforces", "but it enforces", tex)
    tex = sub_once(r"\\section\{recforge: A Reference Implementation\}", "\\section{A Reference Implementation}", tex)
    tex = sub_once(r"recforge~\\citep\{recforge\} is an open benchmark", "The reference implementation~\\citep{recforge} is an open benchmark", tex)
    if re.search(r"recforge(?![}])", tex.replace("app:recforge", "")):
        raise SystemExit("tool name left in main.tex")
    tex = sub_once(r"\\bibliographystyle\{ACM-Reference-Format\}\n\\bibliography\{\.\./refs\}",
                   "\\bibliographystyle{tmlr}\n\\bibliography{refs-anon}", tex)
    # the 12-column audit and design tables only fit in landscape with author-year citations
    for marker in ("Evaluation audit", "Design of the 27 audited loops"):
        tables = tex.split("\\begin{table*}[t]")
        hits = [i for i, t in enumerate(tables) if i and marker in t.split("\\end{table*}")[0]]
        if len(hits) != 1:
            raise SystemExit(f"table not found: {marker}")
        body, rest = tables[hits[0]].split("\\end{table*}", 1)
        tables[hits[0]] = "\\begin{sidewaystable}" + body + "\\end{sidewaystable}" + rest
        tex = tables[0] + "".join(t if t.startswith("\\begin{sidewaystable}") else "\\begin{table*}[t]" + t
                                  for t in tables[1:])
    tex = tex.replace("\\usetikzlibrary{", "\\tikzset{every picture/.append style={transform shape, scale=0.92}}\n"
                      "\\usetikzlibrary{", 1)
    tex = sub_once(r"\\pdfinfo\{[^\n]*\}\n", "", tex)
    # first-person self-citation -> third person (double-blind)
    # the authors' own unrefereed ideation-harness study cannot be checked by reviewers, so it is dropped as evidence
    tex = sub_once(r", and a pre-registered study of LLM research-ideation harnesses by one\nof us.*?fell~\\cite[pt]?\{yang2026ideationgoodhart\}\.",
                   ".", tex, flags=re.S)
    tex = sub_once(r",yang2026ideationgoodhart\}", "}", tex)
    if "ideationgoodhart" in tex:
        raise SystemExit("ideation-harness citation left in main.tex")
    # the protocol figure names the tool
    fig = (ROOT / "draft/figs/protocol.tex").read_text().replace("Judge (recforge)", "Judge").replace(
        "in recforge.", "in the reference implementation.").replace("recforge", "the reference implementation")
    (HERE / "protocol-anon.tex").write_text(fig)
    tex = sub_once(r"\\input\{figs/protocol\}", "\\input{protocol-anon}", tex)
    tex = sub_once(r" One of us wrote the ideation-harness study cited in\n\\S\\ref\{sec:systems\}, which is outside recommendation and not peer reviewed,"
                   r" and both of us wrote the LLM-guided\nregularisation paper cited in \\S\\ref\{sec:method\} as an excluded example\.",
                   "", tex)
    if re.search(r"[Oo]ne of us|[Bb]oth of us", tex):
        raise SystemExit("first-person self-citation left in main.tex")
    tex = tex.replace("\\input{figs/", "\\input{../../draft/figs/")
    tex = tex.replace("\\input{audit_rows}", "\\input{../../draft/audit_rows}")
    tex = tex.replace("\\input{crosstab}", "\\input{../../draft/crosstab}")
    tex = tex.replace("\\input{pilot}", "\\input{../../draft/pilot}")
    tex = tex.replace("\\input{sensitivity}", "\\input{../../draft/sensitivity}")
    return tex


def build_bib():
    bib = (ROOT / "refs.bib").read_text()
    anon = {
        "yang2026ideationgoodhart": "@misc{yang2026ideationgoodhart,\n  title = {{What Should You Optimize When You Optimize an "
                                    "LLM Research-Ideation Harness?}},\n  author = {Anonymous},\n  year = {2026},\n"
                                    "  note = {Code, pre-registrations and report; anonymised for review}\n}",
        "recforge": "@misc{recforge,\n  title = {{Reference implementation of the reporting checklist}},\n"
                    "  author = {Anonymous},\n  year = {2026},\n  note = {Anonymised for review}\n}",
    }
    for key, entry in anon.items():
        bib, n = re.subn(r"@misc\{" + key + r",.*?\n\}", lambda m: entry, bib, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"bib entry not found: {key}")
    # uncited in the anonymised text; dropped so that no tool can list it
    bib, n = re.subn(r"@inproceedings\{shi2026selective,.*?\n\}\n?", "", bib, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("bib entry not found: shi2026selective")
    bib, n = re.subn(r"@misc\{yang2026ideationgoodhart,.*?\n\}\n?", "", bib, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("bib entry not found: yang2026ideationgoodhart")
    if any(w in bib for w in IDENTIFYING) or "2512.21526" in bib or "3779211.3795736" in bib:
        raise SystemExit("bibliography still identifies the authors")
    return bib


# commit ids could be searched for on a public host; local paths name the user; the tool name is anonymised
COMMITS = set(subprocess.run(["git", "log", "--all", "--format=%H"], capture_output=True, text=True, cwd=ROOT).stdout.split())


def sanitize(data):
    try:
        text = data.decode()
    except UnicodeDecodeError:
        return data
    text = re.sub(r"\b[0-9a-f]{7,40}\b", lambda m: "[commit id withheld for review]" if any(c.startswith(m.group()) for c in COMMITS) else m.group(), text)
    text = re.sub(r"/tmp/claude-[^\s`)]*", "<local path>", text)
    # the self-citation dropped from the anonymised bibliography is also withheld from the review logs
    text = re.sub(r'\n  "yang2026ideationgoodhart": \[[^\]]*\],', "", text)
    text = "\n".join("[line withheld for review]"
                     if "ideationgoodhart" in l or l.startswith("| C-7") else l for l in text.split("\n"))
    text = re.sub(r"papers/self-evolving-recsys-survey/", "", text)
    # a public earlier version is allowed by TMLR but need not be pointed at
    text = text.replace("the public v1 audit table", "the first coding").replace("## Changes in v2 (", "## Changes after internal review (").replace('"Changes in v2"', '"Changes after internal review"').replace("Removed in v2:", "Removed after internal review:").replace("applied in v2 (", "applied after internal review (")
    text = text.replace(" Survey v2 draft:", " Survey draft:").replace(" Survey v2:", " Survey:")
    text = text.replace("the current `draft/paper.tex`", "the current manuscript source (`paper.tex`)").replace("`draft/paper.tex`", "the manuscript source (`paper.tex`)").replace("draft/paper.tex", "paper.tex").replace("draft/audit_rows.tex", "audit_rows.tex")
    return text.replace("recforge", "the reference implementation").encode()


def build_supplement():
    files = []
    for entry in SUPPLEMENT:
        path = ROOT / entry
        files += sorted(p for p in path.rglob("*") if p.is_file()) if path.is_dir() else [path]
    files = [p for p in files if not p.name.endswith((".pre_refcheck", ".pyc"))]
    with zipfile.ZipFile(HERE / "supplement.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            text = sanitize(p.read_bytes())
            if any(w.encode() in text for w in IDENTIFYING + ("recforge", "shawnyang", "/tmp/claude", "ideationgoodhart", "one of us", "own repository")):
                raise SystemExit(f"supplement file identifies the authors: {p}")
            z.writestr(f"supplement/{p.relative_to(ROOT)}", text)
        z.writestr("supplement/README.md", sanitize((HERE / "supplement-README.md").read_bytes()))
    return len(files) + 1


def main():
    (HERE / "main.tex").write_text(build_tex())
    (HERE / "refs-anon.bib").write_text(build_bib())
    n = build_supplement()
    for f in ("tmlr.sty", "tmlr.bst", "fancyhdr.sty"):
        if not (HERE / f).exists():
            raise SystemExit(f"missing {f}: copy it from https://github.com/JmlrOrg/tmlr-style-file")
    main_tex = (HERE / "main.tex").read_text()
    leaks = [w for w in IDENTIFYING + ("Independent Researcher", "Santa Clara", "github.com", "preprints.org", "zenodo") if w in main_tex] + re.findall(r"[\w.+-]+@[\w-]+\.(?:com|edu)", main_tex)
    if leaks:
        raise SystemExit(f"main.tex still identifies the authors: {leaks}")
    print(f"wrote main.tex, refs-anon.bib and supplement.zip ({n} files)")


if __name__ == "__main__":
    main()
