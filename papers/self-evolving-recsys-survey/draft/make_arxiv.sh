#!/usr/bin/env bash
# Build the arXiv upload: paper.tex + figs + paper.bbl (arXiv does not run bibtex on .bib files we omit).
set -euo pipefail
cd "$(dirname "$0")"
pdflatex -interaction=nonstopmode paper.tex >/dev/null
bibtex paper >/dev/null
pdflatex -interaction=nonstopmode paper.tex >/dev/null
pdflatex -interaction=nonstopmode paper.tex >/dev/null
out=arxiv-upload.tar.gz
tar czf "$out" paper.tex paper.bbl figs/*.tex
echo "wrote $out ($(du -h "$out" | cut -f1)); upload it at https://arxiv.org/submit (primary cs.IR, cross-list cs.LG, cs.AI)"
