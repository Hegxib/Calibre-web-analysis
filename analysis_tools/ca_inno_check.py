import struct

with open('D:\\Analysis\\Calibre-Web-Setup_V0626_2.exe', 'rb') as f:
    data = f.read()

# Find the marker and check version string
idx = data.find(b'Inno Setup Setup Data (6.6.1)')
if idx >= 0:
    print('Inno Setup version: 6.6.1')
    
# Check for any other version indicators in the stub
text = data[:740000].decode('latin-1', errors='replace')
marker = 'SetupLdrAndSetup.'
pos = text.find(marker)
if pos >= 0:
    ctx = text[pos:pos+200]
    print('Setup info:', repr(ctx.replace('\x00', ' ').strip()[:200]))
    
# Check for Inno Setup constants and paths (like default install dir)
appdir = data.find(b'{app}')
if appdir >= 0 and appdir < 732940:
    ctx = data[max(0,appdir-10):min(len(data),appdir+30)]
    print('{app} found at', appdir, ':', repr(ctx.decode('latin-1', errors='replace').strip()))
    
# Check Inno Setup compressed data header structure
cdata = data[idx:]
print()
print('Setup data starts at:', idx)
print('Setup data size:', len(cdata), 'bytes (', len(cdata)/1024/1024, 'MB)')

# Check the setup header area
header = cdata[:512]
print('First 200 hex bytes:')
print(header[:200].hex())

# Look for Inno Setup version string variants
for ver_str in [b'6.6.1', b'6.6', b'6.2', b'6.1', b'6.0']:
    pos = data.find(ver_str)
    count = 0
    while pos >= 0 and count < 5:
        if pos < 740000:
            start = max(0, pos-10)
            end = min(len(data), pos+20)
            ctx = data[start:end]
            readable = ''.join(chr(b) if 32 <= b < 127 else '.' for b in ctx)
            print(f'  "{ver_str.decode()}" at {pos}: {readable}')
        pos = data.find(ver_str, pos+1)
        count += 1

# Try to find the actual descriptor section (before compressed data)
# Inno Setup 6.x has a new format
print()
print('Checking offsets before marker for descriptor info...')
# Look for setup header size indicator
for off in range(732000, 733000):
    if data[off:off+4] == b'\x00\x00\x00\x00':
        continue
# Just check the region before marker
region = data[idx-256:idx+256]
print('Region around marker:', repr(region[:50]))
# Find null-terminated strings
current = ''
for i, b in enumerate(region):
    c = chr(b) if 32 <= b < 127 else ''
    if c:
        current += c
    else:
        if len(current) > 5 and len(current) < 100:
            print(f'  [{i}] {current}')
        current = ''
