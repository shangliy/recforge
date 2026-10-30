"""Rewrite arXiv entries of refs.bib to their published versions (published.tsv), keeping the arXiv eprint.

usage: python3 arxiv2bib.py ids.txt manual.bib > refs.bib && python3 published.py refs.bib
The audit coded the arXiv versions; AUDITED entries keep a note saying so.
"""
import re
import sys
from pathlib import Path

AUDITED = {"wang2026selfevolving", "pan2026recevolve"}
JOURNAL = ("Transactions", "Nature", "Journal")
# published author lists or titles that differ from arXiv (checked against Crossref, 2026-10-22)
AUTHORS = {
    "zhao2020autoemb": "Xiangyu Zhao and Haochen Liu and Wenqi Fan and Hui Liu and Jiliang Tang and Chong Wang and "
                       "Ming Chen and Xudong Zheng and Xiaobing Liu and Xiwang Yang",
    "wang2023recagent": "Lei Wang and Jingsen Zhang and Hao Yang and Zhi-Yuan Chen and Jiakai Tang and Zeyu Zhang and "
                        "Xu Chen and Yankai Lin and Hao Sun and Ruihua Song and Wayne Xin Zhao and Jun Xu and "
                        "Zhicheng Dou and Jun Wang and Ji-Rong Wen",
    "peng2025agentsurvey": "Qiyao Peng and Hongtao Liu and Hua Huang and Jian Yang and Qing Yang and Minglai Shao",
}
TITLES = {
    "xu2026harness2": r"Harness$^2$: Recursive Agent Harnessing for an Open World",
    "narasimhan2026taurec": r"$\tau$-Rec: A Verifiable Benchmark for Agentic Recommender Systems",
    "wang2023recagent": "User Behavior Simulation with Large Language Model-based Agents",
    "baumgart2026autoreclab": "AutoRecLab: An Autonomous Recommender Systems Lab",
    # the papers' own titles (arXiv metadata: "Self Evolving", "...Recommender System")
    "mu2026evorec": "EvoRec: Self-Evolving Agentic Recommender Systems",
    "li2026autorecsys": "Auto-RecSys: Harnessing Autonomous Research Agents for Industry-Scale Recommender Systems",
}

path = Path(sys.argv[1])
bib = path.read_text()
pub = {}
for line in open(Path(__file__).with_name("published.tsv")):
    if line.startswith("#") or not line.strip():
        continue
    key, venue, year, volno, pages, doi = line.rstrip("\n").split("\t")
    pub[key] = (venue, year, volno, pages, doi)


def rewrite(m):
    kind, key, body = m.group(1), m.group(2), m.group(3)
    if key not in pub or kind != "misc":
        return m.group(0)
    venue, year, volno, pages, doi = pub[key]
    journal = any(w in venue for w in JOURNAL)
    body = re.sub(r"  howpublished = \{[^}]*\},?\n", "", body)
    body = re.sub(r"  year = \{\d+\}", f"  year = {{{year}}}", body)
    if key in AUTHORS:
        body = re.sub(r"  author = \{.*\},\n", f"  author = {{{AUTHORS[key]}}},\n", body)
    if key in TITLES:
        body = re.sub(r"  title = \{\{.*\}\},\n", f"  title = {{{{{TITLES[key]}}}}},\n", body)
    extra = [f"  {'journal' if journal else 'booktitle'} = {{{venue}}}"]
    if volno != "-":
        vol, _, no = volno.partition("/")
        extra.append(f"  volume = {{{vol}}}")
        if no:
            extra.append(f"  number = {{{no}}}")
    if pages != "-":
        if pages.startswith("article "):
            extra.append(f"  articleno = {{{pages.split()[1]}}}")
        else:
            extra.append(f"  pages = {{{pages}}}")
    if doi.startswith("10.1145/") and not journal:
        extra += ["  publisher = {ACM}", "  address = {New York, NY, USA}"]
    if doi != "-":
        extra.append(f"  doi = {{{doi}}}")
        body = re.sub(r"  url = \{[^}]*\}", f"  url = {{https://doi.org/{doi}}}", body)
    if key in AUDITED:
        extra.append("  note = {The audit coded the arXiv version}")
    body = body.rstrip().rstrip(",") + ",\n" + ",\n".join(extra) + "\n"
    return f"@{'article' if journal else 'inproceedings'}{{{key},{body}}}"


bib = re.sub(r"@(\w+)\{([^,]+),(.*?)\n\}", rewrite, bib, flags=re.S)
for key, title in TITLES.items():  # TeX-safe titles for entries that stay on arXiv as well
    bib = re.sub(r"(@\w+\{" + key + r",\n  title = \{\{).*?(\}\},\n)", lambda m: m.group(1) + title + m.group(2), bib)
path.write_text(bib)
print(f"published versions applied: {sum(1 for k in pub if '@inproceedings{' + k + ',' in bib or '@article{' + k + ',' in bib)}/{len(pub)}")

# TeX-escape accented letters in author fields (ACM TAPS rejects raw UTF-8 in .bbl author names)
import unicodedata

ACC = {"́": "'", "̀": "`", "̂": "^", "̃": "~", "̈": '"', "̧": "c", "̌": "v",
       "̆": "u", "̄": "=", "̋": "H", "̨": "k", "̇": "."}
SPECIAL = {"ı": r"{\i}", "ø": r"{\o}", "Ø": r"{\O}", "ß": r"{\ss}", "ł": r"{\l}", "Ł": r"{\L}", "æ": r"{\ae}"}


def escape(name):
    out = []
    for ch in name:
        if ord(ch) < 128:
            out.append(ch)
        elif ch in SPECIAL:
            out.append(SPECIAL[ch])
        else:
            d = unicodedata.normalize("NFD", ch)
            base, marks = d[0], d[1:]
            if base == "i" and marks:
                base = r"\i"
            for mk in marks:
                cmd = ACC.get(mk)
                if cmd is None:
                    raise SystemExit(f"no TeX escape for {ch!r} in {name!r}")
                base = f"\\{cmd}{{{base}}}" if cmd.isalpha() else f"\\{cmd}{base}"
            out.append("{" + base + "}")
    return "".join(out)


bib = re.sub(r"(  author = \{)(.*)(\},?\n)", lambda m: m.group(1) + escape(m.group(2)) + m.group(3), path.read_text())
path.write_text(bib)

# names the arXiv metadata spells without diacritics, or that BibTeX splits wrongly
NAMES = {"Blaz Skrlj": r"Bla{\v{z}} {\v{S}}krlj", "Huan-ang Gao": "{Huan-ang} Gao"}
bib = path.read_text()
for old, new in NAMES.items():
    bib = bib.replace(old, new)
path.write_text(bib)
