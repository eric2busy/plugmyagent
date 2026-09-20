#!/usr/bin/env python3
"""Fetch each catalog entry's link-preview image (og:image / twitter:image),
download it, and store a resized hero under build/api/img/<slug>.jpg.

Writes manifest to build/api/img/manifest.json (slug -> relative path).
Resumable: skips slugs already in the manifest with an existing file.
Entries without a usable image simply get no entry (orange fallback).

Usage: fetch_hero_images.py [--limit N]
"""
import io
import json
import os
import re
import sys
import time
import unicodedata
from urllib.parse import urljoin

import requests
from PIL import Image

BASE = os.path.expanduser("~/workspace/plugmyagent-sync/build")
MASTER = os.path.expanduser("~/workspace/api-catalog/master-list.json")
IMG_DIR = os.path.join(BASE, "api", "img")
MANIFEST = os.path.join(IMG_DIR, "manifest.json")

UA = {"User-Agent": "Mozilla/5.0 (compatible; PlugMyAgent/1.0; +https://www.plugmyagent.com/)"}
TIMEOUT = 15
MIN_WIDTH = 600
MAX_WIDTH = 1600

OG_RE = re.compile(
    r'<meta\s+(?:property=["\']og:image["\']|name=["\']twitter:image["\'])\s+content=["\']([^"\']+)["\']',
    re.I)
OG_RE2 = re.compile(
    r'<meta\s+content=["\']([^"\']+)["\']\s+(?:property=["\']og:image["\']|name=["\']twitter:image["\'])',
    re.I)


def slugify(name):
    s = (name or "api").lower()
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"[\u0300-\u036f]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "api"


def find_image_url(page_url):
    try:
        r = requests.get(page_url, headers=UA, timeout=TIMEOUT)
        if r.status_code != 200 or "text/html" not in r.headers.get("Content-Type", ""):
            return None
        html = r.text[:500000]
    except Exception:
        return None
    for rx in (OG_RE, OG_RE2):
        m = rx.search(html)
        if m:
            return urljoin(page_url, m.group(1).strip())
    return None


def fetch_image(img_url):
    try:
        r = requests.get(img_url, headers=UA, timeout=TIMEOUT)
        if r.status_code != 200:
            return None
        ct = r.headers.get("Content-Type", "")
        if "image" not in ct and "octet-stream" not in ct:
            return None
        im = Image.open(io.BytesIO(r.content))
        im.load()
        return im
    except Exception:
        return None


def main():
    limit = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "--limit" else None
    os.makedirs(IMG_DIR, exist_ok=True)
    manifest = {}
    if os.path.exists(MANIFEST):
        manifest = json.load(open(MANIFEST))

    apis = json.load(open(MASTER))
    seen = {}
    jobs = []
    for api in apis:
        base = slugify(api.get("name"))
        slug, n = base, 2
        while slug in seen:
            slug = f"{base}-{n}"
            n += 1
        seen[slug] = api
        url = (api.get("docs_url") or api.get("url") or "").strip()
        if url:
            jobs.append((slug, url))
    if limit:
        jobs = jobs[:limit]

    done, skipped, failed = 0, 0, 0
    for i, (slug, url) in enumerate(jobs):
        out = os.path.join(IMG_DIR, slug + ".jpg")
        if slug in manifest and os.path.exists(out):
            skipped += 1
            continue
        img_url = find_image_url(url)
        if not img_url:
            failed += 1
            continue
        im = fetch_image(img_url)
        if im is None:
            failed += 1
            continue
        try:
            if im.mode in ("RGBA", "LA", "P"):
                bg = Image.new("RGB", im.size, (11, 13, 13))
                bg.paste(im, mask=im.split()[-1] if im.mode in ("RGBA", "LA") else None)
                im = bg
            else:
                im = im.convert("RGB")
            if im.width < MIN_WIDTH:
                failed += 1
                continue
            if im.width > MAX_WIDTH:
                im = im.resize((MAX_WIDTH, int(im.height * MAX_WIDTH / im.width)), Image.LANCZOS)
            im.save(out, "JPEG", quality=80, optimize=True)
            manifest[slug] = f"api/img/{slug}.jpg"
            done += 1
        except Exception:
            failed += 1
        if (i + 1) % 25 == 0:
            json.dump(manifest, open(MANIFEST, "w"), indent=1)
            print(f"[{i+1}/{len(jobs)}] done={done} skipped={skipped} failed={failed}", flush=True)
        time.sleep(0.4)

    json.dump(manifest, open(MANIFEST, "w"), indent=1)
    print(f"FINISHED total={len(jobs)} done={done} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()
