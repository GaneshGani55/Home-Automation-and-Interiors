#!/usr/bin/env python3
"""Build a self-contained offline copy of the conduit map.

Inlines app.js and base64-embeds every image in assets/img/ into a single
HTML file (conduit-map-offline.html) that works with no internet — for
AirDrop / WhatsApp to the electrician's phone. PDFs are NOT embedded (they
keep the file small + reliable on mobile); the PDF buttons hide offline.
Run from inside the conduit-map/ folder:  python3 build_offline.py
"""
import base64, json, pathlib

base = pathlib.Path(__file__).resolve().parent
html = (base / "index.html").read_text()
appjs = (base / "app.js").read_text()

assets = {}
for f in sorted((base / "assets" / "img").glob("*.jpg")):
    b64 = base64.b64encode(f.read_bytes()).decode()
    assets[f"assets/img/{f.name}"] = "data:image/jpeg;base64," + b64

inject = ("<script>window.__OFFLINE=true;window.__ASSETS="
          + json.dumps(assets) + ";</script>")
inline = inject + "\n<script>\n" + appjs + "\n</script>"
out = html.replace('<script src="app.js"></script>', inline)

dest = base / "conduit-map-offline.html"
dest.write_text(out)
print(f"wrote {dest.name}: {len(out.encode())/1e6:.2f} MB, {len(assets)} images embedded")
