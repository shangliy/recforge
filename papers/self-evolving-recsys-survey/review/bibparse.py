"""Minimal BibTeX parser (brace-aware) shared by the review scripts."""
import re


def parse_bib(text):
    entries = []
    i = 0
    while True:
        m = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,").search(text, i)
        if not m:
            break
        etype, key = m.group(1).lower(), m.group(2)
        j = m.end()
        depth = 1
        k = j
        while k < len(text) and depth:
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
            k += 1
        body = text[j:k - 1]
        start_line = text.count("\n", 0, m.start()) + 1
        entries.append({"type": etype, "key": key, "fields": parse_fields(body), "raw": text[m.start():k],
                        "line": start_line})
        i = k
    return entries


def parse_fields(body):
    fields = {}
    i = 0
    n = len(body)
    while i < n:
        m = re.compile(r"\s*(\w+)\s*=\s*").match(body, i)
        if not m:
            i += 1
            continue
        name = m.group(1).lower()
        i = m.end()
        if i < n and body[i] == "{":
            depth = 1
            k = i + 1
            while k < n and depth:
                if body[k] == "{":
                    depth += 1
                elif body[k] == "}":
                    depth -= 1
                k += 1
            val = body[i + 1:k - 1]
            i = k
        elif i < n and body[i] == '"':
            k = body.index('"', i + 1)
            val = body[i + 1:k]
            i = k + 1
        else:
            m2 = re.compile(r"[^,]*").match(body, i)
            val = m2.group(0).strip()
            i = m2.end()
        fields[name] = val
        while i < n and body[i] in " \t\n,":
            i += 1
    return fields


def norm(s):
    """Normalise a title/name for comparison: drop TeX escapes/braces/punctuation, lowercase."""
    s = s.replace("\\&", "&").replace("\\%", "%").replace("\\_", "_").replace("\\#", "#")
    s = re.sub(r"\\[a-zA-Z]+\s*", "", s)
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"[^0-9a-zA-Z&%#_]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()
