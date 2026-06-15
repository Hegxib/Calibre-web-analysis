import struct, os

exe = r'D:\Analysis\Calibre-Web_Extracted\calibreweb.exe'
with open(exe, 'rb') as f:
    data = f.read()

print(f'File size: {len(data)} bytes ({len(data)/1024/1024:.2f} MB)')

# Check for PyInstaller magic
idx = data.find(b'PYINSTALLER')
if idx >= 0:
    print(f'\nPyInstaller detected at offset {idx}')
    ctx = data[idx:idx+200]
    print('Context:', repr(ctx[:100]))
    
# Check for MEI (PyInstaller temp dir)
mei = data.find(b'MEI')
if mei >= 0 and mei < 500000:
    print(f'MEI reference at {mei}')

# Check for embedded zip files
pks = []
pos = 0
while pos < len(data):
    pos = data.find(b'PK\x03\x04', pos)
    if pos < 0:
        break
    pks.append(pos)
    pos += 1
print(f'\nTotal embedded ZIP headers: {len(pks)}')
print(f'First ZIP at: {pks[0] if pks else "N/A"}')

# Check for .pyc files in the exe  
pyc_count = data.count(b'.pyc')
print(f'References to .pyc: {pyc_count}')

# Look for the actual cps module files inside the exe
for module in [b'cps/__init__.py', b'cps/web.py', b'cps/admin.py', b'cps/books.py']:
    pos = data.find(module)
    if pos >= 0:
        end = min(len(data), pos + 60)
        ctx = data[pos:end].decode('latin-1', errors='replace')
        print(f'\nFound: {module.decode()} at {pos}')
        print(f'  Context: {repr(ctx[:80])}')

print('\n--- Python module references in exe ---')
for ref in [b'cps.', b'flask', b'sqlalchemy', b'werkzeug', b'jinja2']:
    count = data.count(ref)
    if count > 0:
        print(f'  {ref.decode()}: {count} occurrences')

# Check for __init__.pyc in extracted dir
import glob
cps_dir = r'D:\Analysis\Calibre-Web_Extracted\_internal\cps'
pyc_files = glob.glob(cps_dir + '/**/__init__*', recursive=True)
print(f'\n__init__ files found: {len(pyc_files)}')
for f in pyc_files:
    size = os.path.getsize(f)
    print(f'  {f} ({size} bytes)')
