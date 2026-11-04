import os, time, requests

tok = os.environ.get('HERMES_GITHUB_TOKEN', '')
if not tok:
    for line in open(os.path.expanduser('~/.profile')):
        if 'HERMES_GITHUB_TOKEN' in line and '=' in line:
            tok = line.split('=', 1)[1].strip().strip('"').strip("'")
h = {'Authorization': f'token {tok}', 'Accept': 'application/vnd.github.v3+json'}
files = ['定投day18.html', '定投day18.png', '定投day17.html', '定投day17.png', '定投进度.md']
for f in files:
    ok = False
    for attempt in range(5):
        try:
            r = requests.get('https://api.github.com/repos/fisheryounggod/hermes/contents/finance/' + f,
                             headers=h, timeout=30)
            p = '/home/yxf/hermes/finance/' + f
            loc = os.path.getsize(p) if os.path.exists(p) else -1
            remote = r.json().get('size') if r.status_code == 200 else None
            ok = (r.status_code == 200 and remote == loc)
            print(f, r.status_code, 'remote', remote, 'local', loc, 'MATCH' if ok else 'MISMATCH')
            if ok:
                break
        except Exception as e:
            print(f, 'attempt', attempt, 'error', type(e).__name__, str(e)[:80])
        time.sleep(6)
