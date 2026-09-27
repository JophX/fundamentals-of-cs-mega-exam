#!/usr/bin/env python3
"""Build the mega study guide.

Every code example is *executed* at build time, so what ends up in the PDF is
exactly what the tools printed:

  <pre class="hs" data-file="f.hs" [data-block="name"]></pre>
        include (a named block of) guide/haskell/f.hs; every .hs file is
        type-checked with GHC before the build starts.
  <pre class="hs">...</pre>
        inline Haskell, type-checked on its own (add data-nocheck to show
        deliberately broken code).
  <pre class="ghci" data-file="f.hs">expr1
  expr2</pre>
        each line is evaluated with `ghc -e` against f.hs and the real
        result is printed under it (data-file optional).
  <pre class="run" data-cmd="python3 verify/x.py" [data-lang="text"]></pre>
        runs the command in guide/ and shows its output. Non-zero exit fails.
  <pre class="code" data-lang="python">...</pre>
        highlighted only (e.g. pseudo code). Use data-src="verify/x.py" to
        include a file.
  <div class="dot">digraph {...}</div>   Graphviz -> inline SVG
  \( ... \) and \[ ... \]                  KaTeX math
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

GUIDE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(GUIDE, "tools")
HS = os.path.join(GUIDE, "haskell")
BUILD = os.path.join(GUIDE, "build")
ERRORS = []


def fail(msg):
    ERRORS.append(msg)
    print("ERROR:", msg, file=sys.stderr)


def attrs_of(tag):
    return {k: html.unescape(v) for k, v in re.findall(r'([\w-]+)="([^"]*)"', tag)}


def hl(code, lang):
    lexer = get_lexer_by_name(lang)
    out = highlight(code, lexer, HtmlFormatter(nowrap=True))
    return out.rstrip("\n")


# ---------------------------------------------------------------- haskell
def typecheck_all_hs():
    for f in sorted(os.listdir(HS)):
        if f.endswith(".hs"):
            r = subprocess.run(["ghc", "-fno-code", "-v0", "-Wno-all", f], cwd=HS,
                               capture_output=True, text=True)
            if r.returncode != 0:
                fail(f"type error in haskell/{f}:\n{r.stderr}")


def read_block(fname, block):
    src = open(os.path.join(HS, fname)).read()
    if not block:
        # strip block markers and a leading module header comment line if any
        lines = [l for l in src.splitlines() if not re.match(r"\s*-- @(block|end)", l)]
        return "\n".join(lines).strip("\n")
    m = re.search(r"-- @block " + re.escape(block) + r"\n(.*?)\n\s*-- @end", src, re.S)
    if not m:
        fail(f"block {block} not found in {fname}")
        return ""
    return m.group(1)


def check_inline_hs(code):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "Inline.hs")
        open(p, "w").write("module Inline where\n" + code + "\n")
        r = subprocess.run(["ghc", "-fno-code", "-v0", "-Wno-all", p], cwd=d,
                           capture_output=True, text=True)
        if r.returncode != 0:
            fail(f"inline haskell does not type-check:\n{code}\n{r.stderr}")


def ghci(fname, exprs):
    # run each expression separately so outputs map 1:1 to inputs
    outs = []
    for e in exprs:
        a = ["ghc", "-v0", "-e", e] + ([os.path.join(HS, fname)] if fname else [])
        rr = subprocess.run(a, capture_output=True, text=True, timeout=120)
        if rr.returncode != 0:
            fail(f"ghc -e failed: {e}\n{rr.stderr}")
        outs.append(rr.stdout.rstrip("\n"))
    return outs


# ---------------------------------------------------------------- blocks
def process_pre(m):
    tag, body = m.group(1), m.group(2)
    a = attrs_of(tag)
    cls = a.get("class", "")
    body = html.unescape(body).strip("\n")
    title = a.get("data-title")
    cap = f'<div class="codecap">{html.escape(title)}</div>' if title else ""

    if cls == "hs":
        if "data-file" in a:
            code = read_block(a["data-file"], a.get("data-block"))
        else:
            code = body
            if "data-nocheck" not in a:
                check_inline_hs(code)
        extra = " bad" if "data-nocheck" in a else ""
        return f'{cap}<pre class="code hs{extra}">{hl(code, "haskell")}</pre>'

    if cls == "ghci":
        exprs = [l for l in body.splitlines() if l.strip()]
        outs = ghci(a.get("data-file"), exprs)
        parts = []
        for e, o in zip(exprs, outs):
            parts.append('<span class="prompt">ghci&gt; </span>' + hl(e, "haskell"))
            if o:
                parts.append('<span class="result">' + html.escape(o) + "</span>")
        return f'{cap}<pre class="code ghci">' + "\n".join(parts) + "</pre>"

    if cls == "run":
        cmd = a["data-cmd"]
        r = subprocess.run(cmd, shell=True, cwd=GUIDE, capture_output=True, text=True, timeout=600)
        if r.returncode != 0:
            fail(f"command failed: {cmd}\n{r.stdout}\n{r.stderr}")
        out = r.stdout.rstrip("\n")
        shown = a.get("data-show", cmd)
        head = f'<span class="prompt">$ {html.escape(shown)}</span>\n' if "data-hidecmd" not in a else ""
        return f'{cap}<pre class="code run">{head}{html.escape(out)}</pre>'

    if cls == "code":
        lang = a.get("data-lang", "text")
        if "data-src" in a:
            body = open(os.path.join(GUIDE, a["data-src"])).read().strip("\n")
        return f'{cap}<pre class="code {lang}">{hl(body, lang)}</pre>'

    return m.group(0)


def process_dot(m):
    src = html.unescape(m.group(2)).strip()
    a = attrs_of(m.group(1))
    if "data-name" in a:
        src = open(os.path.join(GUIDE, "diagrams", a["data-name"] + ".dot")).read()
    r = subprocess.run(["dot", "-Tsvg"], input=src, capture_output=True, text=True)
    if r.returncode != 0:
        fail("dot failed:\n" + src + "\n" + r.stderr)
        return ""
    svg = r.stdout
    svg = svg[svg.find("<svg"):]
    cap = a.get("data-caption")
    capdiv = f'<div class="figcap">{cap}</div>' if cap else ""
    return f'<div class="figure">{svg}{capdiv}</div>'


# ---------------------------------------------------------------- math
def render_math(text):
    pat = re.compile(r"\\\[(.+?)\\\]|\\\((.+?)\\\)", re.S)
    items, spans = [], []
    for m in pat.finditer(text):
        if m.group(1) is not None:
            items.append({"tex": html.unescape(m.group(1)), "display": True})
        else:
            items.append({"tex": html.unescape(m.group(2)), "display": False})
        spans.append(m.span())
    if not items:
        return text
    r = subprocess.run(["node", os.path.join(TOOLS, "katex_render.js")], input=json.dumps(items),
                       capture_output=True, text=True)
    outs = json.loads(r.stdout)
    res, last = [], 0
    for (s, e), o, it in zip(spans, outs, items):
        res.append(text[last:s])
        if isinstance(o, dict):
            fail(f"KaTeX error: {o['error']} in {o['tex']!r}")
            o = html.escape(it["tex"])
        res.append(o)
        last = e
    res.append(text[last:])
    return "".join(res)


# ---------------------------------------------------------------- toc
def slug(s, used):
    base = re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", s).lower()).strip("-") or "sec"
    k, i = base, 2
    while k in used:
        k, i = f"{base}-{i}", i + 1
    used.add(k)
    return k


def add_toc(body):
    used, toc = set(), []

    def h(m):
        lvl, attrs, inner = m.group(1), m.group(2), m.group(3)
        idm = re.search(r'id="([^"]+)"', attrs)
        hid = idm.group(1) if idm else slug(inner, used)
        if not idm:
            attrs += f' id="{hid}"'
        if "notoc" not in attrs:
            toc.append((int(lvl), hid, re.sub(r"<(?!/?(i|b|em|span)\b)[^>]+>", "", inner)))
        return f"<h{lvl}{attrs}>{inner}</h{lvl}>"

    body = re.sub(r"<h([12])([^>]*)>(.*?)</h\1>", h, body, flags=re.S)
    items = []
    for lvl, hid, text in toc:
        items.append(f'<li class="toc{lvl}"><a href="#{hid}">{text}</a></li>')
    return body.replace("<!--TOC-->", '<ul class="toc">' + "\n".join(items) + "</ul>")


def main():
    typecheck_all_hs()
    args = sys.argv[1:]
    name = "guide"
    chdir = os.path.join(GUIDE, "chapters")
    if args and args[0] == "--pack":
        name, chdir, args = "priority-pack", os.path.join(GUIDE, "pack"), args[1:]
    files = sorted(f for f in os.listdir(chdir) if f.endswith(".html"))
    only = args  # optional: build only chapters matching these prefixes (+ cover)
    if only:
        files = [f for f in files if f.startswith("00") or any(f.startswith(p) for p in only)]
    parts = []
    for f in files:
        t = open(os.path.join(chdir, f)).read()
        t = re.sub(r"<pre((?:[^>\"]|\"[^\"]*\")*)>(.*?)</pre>", process_pre, t, flags=re.S)
        t = re.sub(r'<div (class="dot"[^>]*)>(.*?)</div>', process_dot, t, flags=re.S)
        parts.append(f"<!-- {f} -->\n" + t)
    body = "\n".join(parts)

    # protect <pre>/<svg> from math processing
    protected = []

    def prot(m):
        protected.append(m.group(0))
        return f"\x00{len(protected)-1}\x00"

    body = re.sub(r"<pre.*?</pre>|<svg.*?</svg>", prot, body, flags=re.S)
    body = render_math(body)
    body = re.sub(r"\x00(\d+)\x00", lambda m: protected[int(m.group(1))], body)
    body = add_toc(body)

    css = open(os.path.join(TOOLS, "style.css")).read()
    pyg = HtmlFormatter(style="friendly").get_style_defs(".code")
    katex_css = os.path.join(TOOLS, "node_modules", "katex", "dist", "katex.min.css")
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Mega Study Guide</title>
<link rel="stylesheet" href="file://{katex_css}">
<style>{pyg}\n{css}</style></head><body>{body}</body></html>"""
    os.makedirs(BUILD, exist_ok=True)
    out_html = os.path.join(BUILD, name + ".html")
    open(out_html, "w").write(doc)
    if ERRORS:
        print(f"\n{len(ERRORS)} ERROR(S) — PDF not rendered.", file=sys.stderr)
        sys.exit(1)
    out_pdf = os.path.join(BUILD, name + ".pdf")
    subprocess.run(["node", os.path.join(TOOLS, "render_pdf.js"), out_html, out_pdf], check=True)
    print("OK ->", out_pdf)


if __name__ == "__main__":
    main()
