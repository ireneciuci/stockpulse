"""Publisher agent: bakes the latest scores into a static site/index.html (deploy to Vercel / Cloudflare Pages)."""
import json
import os

from config import SITE_DATA

SITE = os.path.join(os.path.dirname(__file__), "..", "site")


def run():
    data = json.load(open(SITE_DATA))
    tpl = open(os.path.join(SITE, "template.html")).read()
    html = tpl.replace("/*DATA*/null", json.dumps(data, separators=(",", ":")).replace("</", "<\\/"))
    img = os.path.join(SITE, "assets", "wallstreet.jpg")
    if os.path.exists(img):  # inline the hero engraving so the page is a single file
        import base64
        html = html.replace("/*HERO*/", "data:image/jpeg;base64," + base64.b64encode(open(img, "rb").read()).decode())
    # bare version (for Claude artifact hosting, which adds its own skeleton)
    with open(os.path.join(SITE, "artifact.html"), "w") as f:
        f.write(html)
    # full standalone page (for Vercel / Cloudflare Pages / opening locally)
    with open(os.path.join(SITE, "index.html"), "w") as f:
        f.write('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
                '</head><body style="margin:0">\n' + html + "\n</body></html>")
    print("publisher: site/index.html written")
