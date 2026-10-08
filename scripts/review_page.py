"""Render POST.md as a standalone review page for an outside reader, with its images beside it.

Usage: review_page.py posts/<slug>/POST.md docs/review/index.html
The page is marked noindex because it is an unpublished draft.
"""
import re, sys, html

src = open(sys.argv[1], encoding='utf-8').read()
fm, body = src.split('---\n', 2)[1:]
meta = dict(l.split(':', 1) for l in fm.strip().splitlines() if ':' in l)
title, subtitle = meta['title'].strip(), meta['subtitle'].strip()


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', t)


out, blocks = [], [b.strip() for b in re.split(r'\n\s*\n', body) if b.strip()]
for b in blocks:
    lines = b.split('\n')
    if b.startswith('# '):
        continue
    if b.startswith('## '):
        out.append(f'<h2>{inline(b[3:])}</h2>')
    elif b.startswith('!['):
        m = re.match(r'!\[(.*?)\]\((.*?)\)', lines[0])
        cap = lines[1].strip().strip('*') if len(lines) > 1 else ''
        out.append(f'<figure><img src="{m.group(2)}" alt="{html.escape(m.group(1))}"><figcaption>{inline(cap)}</figcaption></figure>')
    elif b.startswith('<iframe'):
        out.append(f'<figure class="embed">{b}</figure>')
    elif b.startswith('::: spacer'):
        continue
    elif b.startswith('::: divider'):
        out.append('<hr>')
    elif b.startswith('- '):
        out.append('<ul>' + ''.join(f'<li>{inline(l[2:])}</li>' for l in lines) + '</ul>')
    else:
        out.append(f'<p>{inline(" ".join(lines))}</p>')

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>{html.escape(title)} (draft for review)</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=IBM+Plex+Sans:wght@400;600&display=swap">
<style>
/* Layout: one reading column, 66 characters wide; charts break out a little wider on large screens. */
:root {{
  --bg: #fbfaf6; --fg: #1c1d1a; --dim: #5d5f58; --rule: #dcdad0; --note-bg: #f0eedf; --accent: #8a6100;
  --read: "Newsreader", Georgia, "Times New Roman", serif;
  --label: "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg: #181a1b; --fg: #e8e8e4; --dim: #a3a59d; --rule: #33362f; --note-bg: #23251f; --accent: #d9a02a; color-scheme: dark }} }}
:root[data-theme="dark"] {{ --bg: #181a1b; --fg: #e8e8e4; --dim: #a3a59d; --rule: #33362f; --note-bg: #23251f; --accent: #d9a02a; color-scheme: dark }}
body {{ background: var(--bg); color: var(--fg); font-family: var(--read); font-size: 1.19rem; line-height: 1.62; padding-inline: 20px; padding-block: 28px 80px; }}
main {{ max-width: 66ch; margin-inline: auto; display: flex; flex-direction: column; gap: 1.05em; }}
main > * {{ margin: 0; min-width: 0; }}
.note {{ font-family: var(--label); font-size: .82rem; line-height: 1.5; color: var(--dim); background: var(--note-bg); border-radius: 6px; padding: 10px 14px; }}
.note strong {{ color: var(--accent); letter-spacing: .04em; text-transform: uppercase; font-size: .76rem; }}
h1 {{ font-size: clamp(2rem, 6vw, 2.9rem); line-height: 1.1; font-weight: 600; text-wrap: balance; margin-top: .5em; }}
.sub {{ font-size: 1.22rem; line-height: 1.45; color: var(--dim); font-style: italic; }}
.by {{ font-family: var(--label); font-size: .85rem; color: var(--dim); padding-bottom: 1em; border-bottom: 1px solid var(--rule); }}
h2 {{ font-size: 1.55rem; line-height: 1.2; font-weight: 600; text-wrap: balance; margin-top: 1.1em; }}
figure {{ margin-block: .6em; }}
figure img {{ display: block; width: 100%; max-width: 100%; height: auto; border-radius: 6px; }}
figure.embed iframe {{ display: block; width: 100%; border-radius: 6px; background: #fcfcfb; }}
figcaption {{ font-family: var(--label); font-size: .82rem; line-height: 1.45; color: var(--dim); margin-top: 8px; }}
@media (min-width: 900px) {{ figure {{ margin-inline: -70px; }} figcaption {{ margin-inline: 70px; }} }}
a {{ color: var(--accent); }} a:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
hr {{ border: 0; border-top: 1px solid var(--rule); margin-block: 1.2em; width: 100%; }}
ul {{ padding-left: 1.2em; display: flex; flex-direction: column; gap: .6em; font-size: 1.05rem; }}
body {{ margin: 0; }} img {{ max-width: 100%; }}
</style>
</head>
<body>
<main>
<p class="note"><strong>Draft for review</strong><br>Not yet published. Charts and figures are current as of October 8, 2026.</p>
<h1>{html.escape(title)}</h1>
<p class="sub">{html.escape(subtitle)}</p>
<p class="by">By Eric Pachman · Data 4 The People</p>
{chr(10).join(out)}
</main>
</body>
</html>
'''
import shutil, pathlib
dst = pathlib.Path(sys.argv[2]); dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(page, encoding='utf-8')
shutil.copytree(pathlib.Path(sys.argv[1]).parent / 'images', dst.parent / 'images', dirs_exist_ok=True)
print('blocks', len(out), 'figures', sum(o.startswith('<figure') for o in out))
