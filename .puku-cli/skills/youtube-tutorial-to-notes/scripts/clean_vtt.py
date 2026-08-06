import re, sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    raw = f.read()

raw = re.sub(r"<[^>]+>", "", raw)  # strip inline word-timing tags

all_lines = []
for line in raw.splitlines():
    line = line.strip()
    if not line or line == "WEBVTT" or line.startswith("Kind:") or line.startswith("Language:") or "-->" in line:
        continue
    all_lines.append(line)

# YouTube auto-captions render as a 2-line rolling window: each new cue block
# repeats a fragment of the previous line plus grows the current line by a
# few words. Grouping by cue block and doing prefix-dedup per block produces
# doubled phrases, because the "hold" cue in between only carries the latest
# line, not the full 2-line block. Flattening every physical line into one
# global stream and doing streaming growth-dedup avoids that.
out = []
last = ""
for line in all_lines:
    if line == last:
        continue
    if line.startswith(last):
        last = line          # still growing the same utterance
    elif last.startswith(line):
        continue              # shorter/older duplicate, drop
    else:
        if last:
            out.append(last)  # finalize previous utterance
        last = line
if last:
    out.append(last)

text = " ".join(out)
text = re.sub(r"\s+", " ", text).strip()
print(text)
