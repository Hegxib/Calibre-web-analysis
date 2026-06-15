import struct

with open('D:\\Analysis\\Calibre-Web-Setup_V0626_2.exe', 'rb') as f:
    data = f.read()

# Inno setup internal: after marker, find compress method
marker = b'Inno Setup Setup Data (6.6.1)'
idx = data.find(marker)
print('Marker at:', idx)

# Check for LZMA compressed data after marker
region = data[idx-2000:idx+min(5000, len(data)-idx)]
region_text = region.decode('latin-1', errors='replace')

# Extract null-terminated strings that look like config
print('\n=== Configuration strings ===')
interesting = ['AppName', 'AppVersion', 'DefaultDirName', 'OutputDir', 'Source', 'DestDir', 'Filename', 'RunList', 'Components', 'Tasks', 'Types']
for term in interesting:
    pos = 0
    while True:
        pos = region_text.find(term, pos)
        if pos < 0:
            break
        # Read the null-terminated value after it
        val_start = pos + len(term) + 1
        val_end = val_start
        while val_end < len(region_text) and region_text[val_end] not in ['\x00', '\x01']:
            val_end += 1
        val = region_text[val_start:val_end].strip()
        if val and len(val) < 100:
            print(f'  {term}: {val}')
        pos += 1

# Check for typical Calibre-Web references
print('\n=== Calibre-Web references in setup stub ===')
for ref in ['calibre', 'web', 'ebook', 'library', 'cps', 'kindle', 'kepub', 'mobi', 'epub', 'pdf', 'cbr', 'cbz', 'metadata', 'opds']:
    idx2 = data.find(ref.encode())
    if idx2 >= 0 and idx2 < 800000:
        end_idx = min(len(data), idx2 + 50)
        ctx2 = data[max(0,idx2-5):end_idx].decode('latin-1', errors='replace')
        print(f'  "{ref}" at {idx2}: {ctx2.strip()[:80]}')

# Check for Inno setup version and AppName string
print('\n=== All readable config lines ===')
# Find consecutive null-terminated strings
config_region = data[idx-2000:idx]
config_text = config_region.decode('latin-1', errors='replace')
current = ''
for i, c in enumerate(config_text):
    if c.isprintable() and c not in '\x00\x01\x02':
        current += c
    else:
        if len(current) > 3 and len(current) < 150:
            if any(x in current for x in ['App', 'Setup', 'Dir', 'File', 'Name', 'Version', 'URL', 'Default', 'Output', 'Source', 'Dest', 'Run', 'Icon', 'License', 'Info']):
                print(f'  {current}')
        current = ''
