---
name: youtube-tutorial-to-notes
description: Turn a YouTube tutorial video link into structured learning material - real transcript, verified GitHub repo, ordered walkthrough, pseudo-code PLUS full working code (Jupyter notebook sources adapted into plain runnable .py, never pasted as raw cells), industry nuances pulled from actual source code flaws. Use when the user pastes a YouTube tutorial/course URL and asks for notes, a summary, a faster way to learn it, or to "extract the transcript" instead of watching it.
---

# YouTube tutorial -> learning material

Goal: user gives one YouTube URL. Output: accurate, ordered notes that let
them navigate the real video faster - not a generic summary of the topic
from general knowledge, and not a scope guess from a related repo.

Hard rule carried through every step: **never fabricate URLs, repo names, or
video content**. Every claim in the final notes must trace back to something
actually fetched (oEmbed JSON, a verified repo file, the cleaned transcript).
If a step's data source is missing or unclear, say so in the output instead
of filling the gap from general knowledge.

Mandatory output shape - both, always, every section: **pseudo-code first,
then the full working code for the same piece**. User works the pseudo-code
themselves first, then compares against the full code - so both must be
present, not one or the other. Pseudo-code is the exercise; full code is the
answer key. Don't skip the full code even if it feels redundant with the
pseudo-code - that comparison step is the entire point of this workflow.

## Step 1 - Resolve video identity (no API key needed)

```
WebFetch: https://www.youtube.com/oembed?url=<video_url>&format=json
```
Gives real `title` and `author_name` (channel). A direct WebFetch on the
`watch?v=` URL itself usually returns only the JS-shell (nav/footer junk) -
oEmbed is the reliable path for title/channel.

## Step 2 - Find the related GitHub repo, then verify it

```
WebSearch: "<channel/author>" "<exact video title>" github
```
The search tool's own summary sometimes **invents a plausible-looking repo
URL** that isn't literally in the returned links list - treat any repo name
it surfaces as a hypothesis, not a fact. Confirm with a direct fetch:

```
WebFetch: https://github.com/<owner>/<repo>
```
Only proceed once this independently confirms the repo exists and its
description/file list plausibly matches the video's topic.

If the user's prompt already contains the video description or a repo link,
use that directly and skip the search - don't re-derive what's already given.

## Step 3 - Pull real source files, don't summarize from the repo listing

```
WebFetch: https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<file>
```
Fetch the actual files relevant to the video's topic (ask for "full raw file
content exactly as-is" in the prompt - summarizers otherwise paraphrase code,
which loses exact API names/parameters). Read enough files to see the real
patterns used: exact imports, function signatures, prebuilt helpers used
instead of hand-rolled ones, error handling (or lack of it), hardcoded values.

These files are also where **industry nuances** come from later (Step 6) -
don't invent generic best-practice advice, cite what the real source actually
does or omits.

**If the source file is a `.ipynb`:** the user works in plain `.py` files, not
notebooks. Don't paste raw cells into the notes - adapt them into what a `.py`
file actually needs:
- Merge duplicate/repeated imports across cells into one top-of-file import
  block (notebooks often re-import the same thing in a later cell).
- A bare trailing expression in a cell (e.g. `workflow.get_state(config1)`)
  relies on Jupyter's implicit last-expression display - it prints nothing in
  a `.py` script. Wrap these in `print(...)` in the adapted code.
- Note any cell that depends on Jupyter/Colab-only behavior (e.g. manual
  kernel interrupt, `%magic` commands, rich display of images/dataframes) -
  call this out explicitly rather than silently translating it, since the
  `.py` equivalent may need a different mechanism entirely (e.g.
  `KeyboardInterrupt` timing is unreliable outside a notebook kernel - flag
  it, don't paper over it).
- Preserve the notebook's original cell order as the section order in the
  notes - only the packaging changes, not the sequence.

## Step 4 - Get the transcript

Check what's available first:
```
which yt-dlp uvx
python3 -c "import youtube_transcript_api"
```
If `uvx` isn't on PATH, it's often still installed at `~/.local/bin/uvx` (uv's
default install location) - check there before assuming it's missing:
```
ls ~/.local/bin/uvx
```
If neither `yt-dlp` nor `uvx` exists anywhere, install `yt-dlp` via an
isolated runner - do not `pip install --user` system-wide (hits PEP 668
externally-managed-environment errors on most distros) and do not add it to
the project's own `pyproject.toml`/venv (it's a one-off tool, not a project
dependency):
```
uvx yt-dlp --version   # (or the ~/.local/bin/uvx full path) installs into an ephemeral uv-managed env on first use
```
Fetch captions only, never the video:
```
uvx yt-dlp --write-auto-sub --sub-lang "<lang>,en" --skip-download \
  --sub-format vtt -o "<name>.%(ext)s" "<video_url>"
```
Run this from the project's scratchpad/temp directory, not the repo.
Ask the user (or infer from context, e.g. channel language) which `<lang>`
to request. A 429 on a second language after the first succeeds is fine -
don't retry-loop on it, one working transcript is enough.

## Step 5 - Clean the VTT into plain text

YouTube auto-caption VTT is **not** simple sequential cues - it's a 2-line
rolling window per cue block (previous line repeated + new line growing word
by word), plus short "hold" cues in between that only repeat the latest
single line, not the full block. Naively joining lines per cue block and
prefix-deduping *between blocks* produces doubled phrases, because the hold
cue's content doesn't match the full previous block.

The fix that actually works: flatten every physical text line in the whole
file into one ordered stream (ignore cue/timestamp boundaries entirely), then
do streaming growth-dedup on that flat stream - use
`scripts/clean_vtt.py` as-is:
```
python3 scripts/clean_vtt.py <name>.<lang>.vtt > transcript_clean.txt
```
Sanity check before trusting it: `wc -w` should land in a plausible range for
the video's length, and `head -c 1000` should read as continuous prose with
no back-to-back repeated phrases. If you still see doubling, the dedup logic
regressed - don't hand-patch it ad hoc, re ­diff against the reference script.

## Step 6 - Read the transcript, then build the notes from what it actually says

Read the full cleaned transcript before writing anything. This is the step
most likely to get skipped in favor of guessing from the repo's file
structure - resist that. A repo can contain files from *other* episodes of
the same series (e.g. a "with-HITL" and "without-HITL" variant sitting side
by side when the video in hand only covers the "without" one). Scope, order,
and depth of the notes must come from what the transcript actually walks
through, not from what files happen to exist in the repo.

Structure the output:
1. **Video/repo identification** - title, channel, verified repo link, which
   specific files were read.
2. **Scope note** - what this video actually covers vs. what's mentioned as
   "future video" material. State this explicitly so the user isn't misled
   into thinking a whole playlist's worth of concepts is in one video.
3. **Ordered walkthrough** matching the transcript's real sequence - one
   section per concept/step as the video introduces it, each with a short
   pseudo-code sketch followed immediately by the full working code for that
   same piece (per the mandatory-output-shape rule above - both, every time).
4. **Industry nuances** - pulled from Step 3's real source files: flag actual
   flaws spotted (hardcoded secrets, missing timeouts, unpinned model
   versions, deprecated vs. current API patterns) rather than generic advice.
5. **Reading order** - primary docs to confirm against, not just the video,
   especially for anything that evolves fast (agent/tool-calling APIs,
   memory/persistence mechanisms).
6. **Suggested exercise** - if the video demonstrates a bug-then-fix pattern
   (common in tutorials), tell the user to reproduce the bug themselves
   first, matching the source video's own pedagogy, before jumping to the
   fix.

## Step 7 - Own mistakes directly if caught

If the user points out a shortcut was taken (e.g. "the GitHub link was right
there in the description, why did you search for it?"), say so plainly and
explain what was actually done instead - don't get defensive, don't backfill
a justification. If new information surfaces that changes earlier notes
(e.g. the transcript reveals the true scope was narrower than assumed),
correct the notes and say what changed and why, don't quietly patch over it.
