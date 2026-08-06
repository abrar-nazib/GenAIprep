import re, sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    raw = f.read()

# strip inline XML tags inside <p> elements
raw = re.sub(r"<[^>]+>", "", raw)

all_lines = []
for line in raw.splitlines():
    line = line.strip()
    if not line or line.startswith("<?xml") or line.startswith("<tt") or line.startswith("</tt"):
        continue
    # skip head/body/div open/close lines
    if line in ("<head>", "</head>", "<body region=\"r1\">", "<div>", "</div>", "</body>", "<styling>", "</styling>", "<layout>", "</layout>"):
        continue
    if line.startswith("<style") or line.startswith("<region") or line.startswith("<layout") or line.startswith("<styling"):
        continue
    all_lines.append(line)

# Same rolling-window dedup logic as clean_vtt.py
out = []
last = ""
for line in all_lines:
    if line == last:
        continue
    if line.startswith(last):
        last = line
    elif last.startswith(line):
        continue
    else:
        if last:
            out.append(last)
        last = line
if last:
    out.append(last)

text = " ".join(out)
text = re.sub(r"\s+", " ", text).strip()
print(text)
