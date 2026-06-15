import re
with open('D:\\Analysis\\Calibre-Web-Setup_V0626_2.exe', 'rb') as f:
    data = f.read()

idx = data.find(b'Inno Setup Setup Data')
print('Inno Setup marker at offset:', idx)
ctx = data[idx:idx+80].decode('latin-1', errors='replace')
print('Version:', ctx.strip())
print('File size:', len(data), 'bytes')
print('Setup data at', round(100*idx/len(data), 1), '% of file')

# Find readable strings in first 740KB (stub)
print()
print('=== Stub strings ===')
stub = data[:idx]
stub_text = stub.decode('latin-1', errors='replace')
current = ''
results = []
for i, c in enumerate(stub_text):
    if 32 <= ord(c) < 127:
        current += c
    else:
        if len(current) > 8:
            keywords = ['calibre', 'python', 'web', 'app', 'http', 'setup', 'install', 'server', '.exe', '.dll', '.py', 'version', 'license', 'copyright', 'github', 'docker', 'config', 'database', 'sqlite', 'flask', 'pip', 'requirements']
            if any(x in current.lower() for x in keywords):
                offset = i - len(current)
                print(f'  @{offset}: {current[:120]}')
        current = ''
