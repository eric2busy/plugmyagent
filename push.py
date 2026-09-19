#!/usr/bin/env python3
"""Push the generated API pages + index.html change to eric2busy/plugmyagent in one commit."""
import sys, os, json, urllib.request, urllib.error

sys.path.insert(0, '/opt/hatch/skills/skill-creator/bin')
from dynamic_credentials import add_surrogate_to_request, read_json_response, read_response_body

REPO = 'eric2busy/plugmyagent'
ROOT = '/tmp/pma-push'

def api(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request('https://api.github.com' + path, data=data, method=method)
    r.add_header('Accept', 'application/vnd.github+json')
    r.add_header('Content-Type', 'application/json')
    add_surrogate_to_request(r, 'custom.github', allowed_hosts=['api.github.com'])
    try:
        resp = urllib.request.urlopen(r, timeout=120)
        return resp.status, read_json_response(resp)
    except urllib.error.HTTPError as e:
        print('HTTP', e.code, 'on', method, path)
        print(read_response_body(e)[:500])
        raise SystemExit(1)

# collect files
entries = []
for dirpath, _, filenames in os.walk(ROOT):
    for fn in filenames:
        if fn.startswith('check') and fn.endswith('.js'):
            continue
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, ROOT)
        if rel in ('api-catalog.json',):
            continue
        with open(full, encoding='utf-8') as f:
            entries.append({'path': rel, 'mode': '100644', 'type': 'blob', 'content': f.read()})
print('files to push:', len(entries))

status, ref = api('GET', f'/repos/{REPO}/git/ref/heads/main')
main_sha = ref['object']['sha']
status, commit = api('GET', f'/repos/{REPO}/git/commits/{main_sha}')
base_tree = commit['tree']['sha']
print('base:', main_sha[:8], base_tree[:8])

status, tree = api('POST', f'/repos/{REPO}/git/trees',
                   {'base_tree': base_tree, 'tree': entries})
print('new tree:', tree['sha'][:8])

msg = ("Add per-API static pages for SEO and link unfurls\n\n"
       "421 generated pages at /api/<slug>/ (SEO meta + Open Graph +\n"
       "JSON-LD), sitemap.xml, robots.txt. Share button now copies the\n"
       "per-API page URL so links unfurl with that API's name and\n"
       "description. Generator: tools/generate-api-pages.py")
status, new_commit = api('POST', f'/repos/{REPO}/git/commits',
                         {'message': msg, 'tree': tree['sha'], 'parents': [main_sha]})
print('new commit:', new_commit['sha'])

status, _ = api('PATCH', f'/repos/{REPO}/git/ref/heads/main', {'sha': new_commit['sha']})
print('main updated OK')
