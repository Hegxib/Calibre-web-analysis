import sys

with open('D:\\Analysis\\Calibre-Web-Setup_V0626_2.exe', 'rb') as f:
    data = f.read()

print('File size:', len(data), 'bytes')
print()

# Find embedded MZ headers
mz_positions = []
pos = 0
while pos < len(data) - 1000:
    pos = data.find(b'MZ', pos)
    if pos < 0:
        break
    if pos > 4:  # skip main exe
        if pos + 0x40 < len(data):
            pe_off = int.from_bytes(data[pos+0x3C:pos+0x40], 'little')
            if pe_off > 0 and pe_off < 5000 and pos + pe_off + 6 < len(data):
                pe_sig = data[pos+pe_off:pos+pe_off+4]
                machine = int.from_bytes(data[pos+pe_off+4:pos+pe_off+6], 'little')
                mach_str = {0x14c: 'x86', 0x8664: 'x64', 0x200: 'IA64'}.get(machine, str(hex(machine)))
                
                # Find approximate size to next MZ
                next_mz = data.find(b'MZ', pos + 64)
                end = next_mz if next_mz > 0 else len(data)
                est_size = end - pos
                
                # Check content type
                sample = data[pos:min(pos+2000, len(data))].decode('latin-1')
                content_hints = []
                for h in ['python', 'Python', 'PyInstaller', 'github', 'calibre', 'web', 'docker', 'pip', 'package', 'node', 'npm', '.dll', '.exe', '.pyd', '.zip', 'gzip']:
                    if h.lower() in sample.lower():
                        content_hints.append(h)
                
                print(f'  MZ at {pos:+>10}: PE={pe_sig.decode()}, arch={mach_str:>4}, size={est_size//1024:>5}KB, hints={content_hints}')
                mz_positions.append(pos)
    pos += 2

print(f'\nTotal embedded MZ files: {len(mz_positions)}')
print(f'File unique byte ratio: {len(set(data))}/256 = {len(set(data))/256*100:.1f}%')

# Check for AutoIt script marker
aut_idx = data.find(b'!AUTOIT')
print(f'\nFirst \"!AUTOIT\" at offset: {aut_idx}')
if aut_idx >= 0:
    print(f'Context hex: {data[aut_idx-16:aut_idx+32].hex()}')

# Look for AutoIt-specific patterns
for sig in [b'>AUTOIT', b'AUTOIT', b'AU3', b'!AUTOIT', b'UEH', b'AUT']:
    idx = data.find(sig)
    if idx >= 0:
        print(f'Found "{sig.decode()}" at offset {idx}')
        if idx + 64 < len(data):
            print(f'  Hex: {data[idx:idx+32].hex()}')

# Check the last portion of the file (where AutoIt script data typically lives)
print(f'\n=== Last 20% of file (possible script data) ===')
tail_start = len(data) * 4 // 5
tail = data[tail_start:].decode('latin-1', errors='replace')
# Show printable ASCII runs
current = ''
for i, c in enumerate(tail):
    if 32 <= ord(c) < 127:
        current += c
    else:
        if len(current) > 15:
            offset = tail_start + i - len(current)
            print(f'  String at {offset}: {current[:120]}')
        current = ''
if current and len(current) > 15:
    print(f'  String at end: {current[:120]}')

# Check for URL patterns
import re
urls = re.findall(r'https?://[a-zA-Z0-9.\-_/]+', data.decode('latin-1', errors='replace'))
print(f'\n=== URLs found: {len(urls)} ===')
for u in sorted(set(urls)):
    print(f'  {u}')

# Check for IP addresses
ips = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', data.decode('latin-1', errors='replace'))
print(f'\n=== IPs found: {len(ips)} ===')
for ip in sorted(set(ips)):
    print(f'  {ip}')
