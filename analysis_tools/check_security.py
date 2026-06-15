import re, os

def extract_strings_from_pyc(data):
    text = data.decode('latin-1', errors='replace')
    strings = []
    current = ''
    for c in text:
        if 32 <= ord(c) < 127:
            current += c
        else:
            if len(current) >= 6:
                strings.append(current)
            current = ''
    if len(current) >= 6:
        strings.append(current)
    return strings

def find_interesting(strings, keywords):
    results = []
    for s in strings:
        for kw in keywords:
            if kw.lower() in s.lower():
                results.append(s)
                break
    return results

base = 'D:/Analysis/calibreweb.exe_extracted/PYZ-00.pyz_extracted'

# Also check top-level pyc files
top_files = ['pyiboot01_bootstrap.pyc', 'pyimod01_archive.pyc', 'pyimod02_importers.pyc']
extras = ['cps/main.pyc', 'cps/updater.pyc', 'cps/helper.pyc', 'cps/db.pyc']

suspicious_kws = [
    'http://', 'https://', 'api.', '.com', '.org', '.net',
    'token', 'secret', 'password', 'api_key',
    'telemetry', 'analytics', 'tracking', 'metrics',
    'collect', 'send', 'upload', 'report',
    'exec', 'eval', 'compile', 'subprocess', 'cmd.exe', 'powershell',
    'reverse', 'backdoor', 'exploit', 'dropper',
    'sentry', 'datadog', 'newrelic', 'posthog', 'mixpanel', 'amplitude',
    'miner', 'bitcoin', 'monero', 'ethereum', 'crypto',
    'license', 'license_key', 'activation',
    'base64', 'b64decode',
]

for fname in top_files + extras:
    path = base + '/' + fname
    try:
        with open(path, 'rb') as f:
            data = f.read()
        strings = extract_strings_from_pyc(data)
        interesting = find_interesting(strings, suspicious_kws)
        
        # Extract unique URLs
        text = data.decode('latin-1', errors='replace')
        urls = list(set(re.findall(r'https?://[a-zA-Z0-9.\-_/~]+[a-zA-Z0-9/]', text)))
        
        if interesting or urls:
            print(f'\n=== {fname} ({len(strings)} strings) ===')
            for s in interesting[:15]:
                s_clean = s[:150]
                print(f'  {s_clean}')
            for u in urls:
                print(f'  URL: {u}')
    except Exception as e:
        print(f'\n=== {fname}: ERROR {e} ===')

# Check existing/installed directory structure for licenses
print('\n\n=== Licenses directory ==')
lic_dir = 'D:/Analysis/Calibre-Web_Extracted/_internal/licenses'
if os.path.exists(lic_dir):
    for f in os.listdir(lic_dir):
        fpath = os.path.join(lic_dir, f)
        if os.path.isfile(fpath):
            size = os.path.getsize(fpath)
            print(f'  {f} ({size} bytes)')

# Check requirements
print('\n=== Requirements files ===')
for rfile in ['requirements.txt', 'optional-requirements.txt']:
    rpath = f'D:/Analysis/Calibre-Web_Extracted/_internal/{rfile}'
    if os.path.exists(rpath):
        with open(rpath, 'r') as f:
            content = f.read()
        print(f'\n--- {rfile} ---')
        print(content)
