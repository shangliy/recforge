#!/usr/bin/env python3
"""Build the anonymized TMLR submission from draft/paper.tex.

    cd submission/tmlr && python3 make_tmlr.py && pdflatex main; bibtex main; pdflatex main; pdflatex main

The ACM draft stays the single source; this script rewrites the preamble,
hides the authors, switches to natbib author-year citations and anonymizes
the two bibliography entries that point at the authors' GitHub account.
"""
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SRC = ROOT / "draft" / "paper.tex"

# Replace with real anonymous.4open.science links before submitting.
ANON = {
    "https://github.com/shangliy/recforge": "https://anonymous.4open.science/r/recforge-ANON",
    "https://github.com/shangliy/ideation-goodhart": "https://anonymous.4open.science/r/ideation-goodhart-ANON",
}

PREAMBLE = r"""\documentclass[10pt]{article}
\usepackage{tmlr}
% For the de-anonymized preprint: \usepackage[preprint]{tmlr}
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
    # links to the authors' repositories in the text (the audit-data footnote)
    for real, anon in ANON.items():
        tex = tex.replace(real, anon)
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
    tex = tex.replace("\\input{figs/", "\\input{../../draft/figs/")
    tex = tex.replace("\\input{audit_rows}", "\\input{../../draft/audit_rows}")
    return tex


def build_bib():
    bib = (ROOT / "refs.bib").read_text()
    for real, anon in ANON.items():
        bib = bib.replace(real, anon)
    bib = re.sub(r"(@misc\{yang2026ideationgoodhart,.*?author = )\{[^}]*\}",
                 r"\1{Anonymous}", bib, count=1, flags=re.S)
    if "shangliy" in bib or "Shanglin" in bib:
        raise SystemExit("bibliography still identifies the authors")
    return bib


def main():
    (HERE / "main.tex").write_text(build_tex())
    (HERE / "refs-anon.bib").write_text(build_bib())
    for f in ("tmlr.sty", "tmlr.bst", "fancyhdr.sty"):
        if not (HERE / f).exists():
            raise SystemExit(f"missing {f}: copy it from https://github.com/JmlrOrg/tmlr-style-file")
    main_tex = (HERE / "main.tex").read_text()
    leaks = [w for w in ("Shanglin", "Zhan Shi", "shangliy", "Independent Researcher", "Santa Clara")
             if w in main_tex] + re.findall(r"[\w.+-]+@[\w-]+\.(?:com|edu)", main_tex)
    if leaks:
        raise SystemExit(f"main.tex still identifies the authors: {leaks}")
    print("wrote main.tex and refs-anon.bib")


if __name__ == "__main__":
    main()
