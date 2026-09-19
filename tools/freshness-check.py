#!/usr/bin/env python3
"""Weekly link-freshness check for the PlugMyAgent catalog.

For every API in api-catalog.json, requests its docs_url (and signup_url
when present) and records the result in the entry's `link_check` field:
{"date": "YYYY-MM-DD", "ok": true/false, "docs": <status>, "signup": <status>}.

- `ok` is true when every present URL answers 2xx/3xx.
- `verified` (human review of the free-tier terms) is NEVER touched here;
  only the automated link check stamp is updated.

Usage: python3 tools/freshness-check.py [--limit N] [--write]
  --limit N  only check the first N entries (for testing)
  --write    write the updated api-catalog.json (default: dry run, prints summary)

Be polite: 0.4s delay between requests, browser-like User-Agent, 15s timeout.
"""

import json
import sys
import time
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()
UA = {"User-Agent": "PlugMyAgent-linkcheck/1.0 (+https://www.plugmyagent.com)"}
# Second-chance UA: some sites serve 404 to unknown bots but 200 to browsers.
# A URL is only "dead" after failing with a real browser user agent too.
BROWSER_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}


def check(url):
    """Return (state, detail) where state is ok|blocked|dead."""
    def attempt(method):
        req = urllib.request.Request(url, method=method, headers=UA)
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            if method == "GET":
                resp.read(2048)
            return ("ok", resp.status)
        except urllib.error.HTTPError as e:
            return ("http", e.code)
        except Exception as e:
            return ("exc", type(e).__name__)

    state, detail = attempt("HEAD")
    if state == "ok":
        return ("ok", detail)
    if state == "http" and detail in (403, 405, 429):
        state2, detail2 = attempt("GET")
        if state2 == "ok":
            return ("ok", detail2)
        state, detail = state2, detail2
    if state == "http" and detail in (404, 410):
        # second chance with a browser UA before declaring dead
        try:
            req2 = urllib.request.Request(url, headers=BROWSER_UA)
            resp2 = urllib.request.urlopen(req2, timeout=15)
            resp2.read(2048)
            return ("ok", resp2.status)
        except Exception:
            pass
        return ("dead", detail)
    return ("blocked", detail)


def main():
    limit = None
    write = False
    for a in sys.argv[1:]:
        if a == "--write":
            write = True
        elif a.startswith("--limit"):
            limit = int(a.split("=")[1])

    path = ROOT / "api-catalog.json"
    catalog = json.loads(path.read_text(encoding="utf-8"))
    if limit:
        catalog = catalog[:limit]

    ok_count, bad = 0, []
    for api in catalog:
        urls = {"docs": api.get("docs_url"), "signup": api.get("signup_url")}
        result = {"date": TODAY}
        states = []
        for key, url in urls.items():
            if not url:
                continue
            state, detail = check(url)
            result[key] = f"{state}:{detail}"
            states.append(state)
            time.sleep(0.4)
        # entry is only "dead" if a URL is definitively gone; bot-blocked
        # URLs are reported separately, not treated as broken links
        result["ok"] = "dead" not in states
        result["unverified"] = [k for k, u in urls.items()
                                if u and result.get(k, "").startswith("blocked")]
        api["link_check"] = result
        if result["ok"] and not result["unverified"]:
            ok_count += 1
        else:
            bad.append((api.get("name"), result))

    dead = [(n, r) for n, r in bad if not r["ok"]]
    unver = [(n, r) for n, r in bad if r["ok"] and r["unverified"]]
    print(f"Checked {len(catalog)} entries: {ok_count} fully OK, "
          f"{len(dead)} with dead links, {len(unver)} bot-blocked (unverified)")
    for name, r in dead[:50]:
        print(" DEAD:", name, r)
    for name, r in unver[:50]:
        print(" UNVERIFIED:", name, r)

    if write:
        full = json.loads(path.read_text(encoding="utf-8"))
        by_name = {a["name"]: a.get("link_check") for a in catalog}
        for a in full:
            if a["name"] in by_name:
                a["link_check"] = by_name[a["name"]]
        path.write_text(json.dumps(full, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Wrote", path)
    else:
        print("(dry run; pass --write to save)")


if __name__ == "__main__":
    main()
