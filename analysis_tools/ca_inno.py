import re
import struct

with open('D:\\Analysis\\Calibre-Web-Setup_V0626_2.exe', 'rb') as f:
    data = f.read()

# Find Inno Setup signature
idx = data.find(b'Inno Setup Setup Data')
if idx >= 0:
    print(f'Inno Setup marker at offset: {idx}')
    ctx = data[max(0,idx-100):min(len(data),idx+200)].decode('latin-1', errors='replace')
    print(f'Context: {ctx[:200]}')
    
    ver_match = re.search(r'Inno Setup Setup Data \((\d+\.\d+\.\d+)\)', ctx)
    if ver_match:
        print(f'Inno Setup version: {ver_match.group(1)}')
    
    before = data[max(0,idx-500):idx]
    print(f'Bytes before Inno marker: {len(before)}')
else:
    print('Inno Setup marker not found - checking other signatures...')
    # Try looking for setup header
    for sig in [b'Inno', b'setup', b'Setup', b'SetupLdr', b'_ISREG', b'LZMAAuthor']:
        pos = data.find(sig)
        if pos >= 0:
            print(f'Found "{sig.decode()}" at offset {pos}')

# Look for file paths in the binary
print('\n=== Looking for file paths and names ===')
patterns = [b'\\\\[a-zA-Z0-9_]+\.exe', b'\\\\[a-zA-Z0-9_]+\.dll', b'\\\\[a-zA-Z0-9_]+\.msi',
            b'\\\\[a-zA-Z0-9_]+\.py', b'[a-zA-Z]:\\\\[A-Za-z0-9_\\\\]+']
for pat in patterns:
    matches = re.findall(pat, data)
    for m in set(matches[:20]):
        try:
            s = m.decode('latin-1')
            if any(x in s.lower() for x in ['calibre', 'python', 'app', 'setup', 'install', 'web', 'server']):
                print(f'  Path: {s}')
        except:
            pass

# Check for file entries in the setup section
print('\n=== File entries near setup data ===')
# Look for null-terminated strings that look like file paths in the setup section
if idx > 0:
    setup_start = idx
    setup_data = data[setup_start:setup_start+min(500000, len(data)-setup_start)]
    # Find consecutive printable strings that look like filenames
    current_str = ''
    for i, b in enumerate(setup_data):
        if 32 <= b < 127:
            current_str += chr(b)
        else:
            if len(current_str) > 5 and any(c in current_str for c in ['.', '\\', '/']) and not current_str.startswith('http'):
                if len(current_str) < 200:
                    print(f'  {current_str}')
            current_str = ''

# Try to find the Inno Setup embedded setup.exe stub
print('\n=== Looking for setup.e32 or similar Inno structures ===')
for sig in [b'setup.e32', b'setup.ex_', b'setup.0', b'setup.1', b'_setup.dll']:
    pos = data.find(sig)
    if pos >= 0:
        print(f'Found "{sig.decode()}" at offset {pos}')

# Quick file entropy overview  
print(f'\nFile size: {len(data)} bytes')
print(f'Unique bytes: {len(set(data))}')
print(f'Entropy: ~{len(set(data))/256*100:.1f}%')
