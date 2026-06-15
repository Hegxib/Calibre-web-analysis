import struct, re

def extract_strings_from_pyc(path):
    """Extract all readable strings from a .pyc binary file."""
    with open(path, 'rb') as f:
        data = f.read()
    
    # Extract null-terminated printable strings
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

# Check a few key files
key_files = [
    'root.pyc',
    'cps/__init__.pyc',
    'cps/web.pyc',
    'cps/server.pyc',
    'cps/config_sql.pyc',
    'cps/kobo.pyc',
    'cps/updater.pyc',
    'cps/oauth.pyc',
    'cps/admin.pyc',
    'cps/main.pyc',
]

base = 'D:/Analysis/calibreweb.exe_extracted/PYZ-00.pyz_extracted'

suspicious_kws = [
    'http://', 'https://', 'api.', '.com', '.org', '.net',
    'token', 'secret', 'password', 'api_key', 'api-', 
    'telemetry', 'analytics', 'tracking', 'metrics',
    'collect', 'send', 'upload', 'report',
    'exec', 'eval', 'compile', 'subprocess',
    'cmd', 'powershell', 'shell', 'b64decode',
    'reverse', 'backdoor', 'exploit',
    'license', 'license_key', 'activation',
    'sentry', 'datadog', 'newrelic', 'posthog',
]

for fname in key_files:
    path = base + '/' + fname
    try:
        strings = extract_strings_from_pyc(path)
        interesting = find_interesting(strings, suspicious_kws)
        if interesting:
            print(f'\n=== {fname} ({len(strings)} strings) ===')
            for s in interesting[:20]:
                print(f'  {s[:150]}')
    except Exception as e:
        print(f'\n=== {fname}: ERROR {e} ===')
