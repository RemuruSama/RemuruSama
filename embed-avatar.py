#!/usr/bin/env python3
"""Embed your GitHub profile photo into the header SVGs.

GitHub blocks remote images inside SVGs, so the photo has to live in the file
itself as a base64 data URI. Run this once from the repo root:

    python3 embed-avatar.py                 # downloads your GitHub avatar
    python3 embed-avatar.py photo.png       # or use a local image / other URL

Re-run any time you change your photo. Safe to run repeatedly. You can delete
this script afterwards.
"""
import base64, os, re, sys, urllib.request

DEFAULT = "https://avatars.githubusercontent.com/u/79688470?v=4&s=256"
TARGETS = ["assets/header-dark.svg", "assets/header-light.svg"]


def load(src):
    if os.path.exists(src):
        return open(src, "rb").read()
    req = urllib.request.Request(src, headers={"User-Agent": "embed-avatar"})
    return urllib.request.urlopen(req, timeout=30).read()


def mime(b):
    if b[:3] == b"\xff\xd8\xff": return "image/jpeg"
    if b[:8] == b"\x89PNG\r\n\x1a\n": return "image/png"
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP": return "image/webp"
    sys.exit("Unrecognised image format (need JPEG, PNG or WebP).")


data = load(sys.argv[1] if len(sys.argv) > 1 else DEFAULT)
uri = f"data:{mime(data)};base64,{base64.b64encode(data).decode()}"
slot = ('<g id="avatar"><image href="%s" x="-53" y="-53" width="106" height="106" '
        'preserveAspectRatio="xMidYMid slice" clip-path="url(#av)"/></g>' % uri)

for path in TARGETS:
    svg = open(path, encoding="utf-8").read()
    new, n = re.subn(r'<g id="avatar">.*?</g>', lambda m: slot, svg, flags=re.S)
    if n != 1:
        sys.exit(f"Could not find the avatar slot in {path}. Run from the repo root.")
    open(path, "w", encoding="utf-8").write(new)
    print(f"embedded photo into {path} ({len(data)//1024} KB)")
