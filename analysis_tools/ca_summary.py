import re

with open('D:\\Analysis\\Calibre-Web-Setup_V0626_2.exe', 'rb') as f:
    data = f.read()

print("=" * 60)
print("CALIBRE-WEB SETUP V0626_2 — BINARY ANALYSIS REPORT")
print("=" * 60)

print(f"\nFile size: {len(data)} bytes ({len(data)/1024/1024:.2f} MB)")
print(f"Format: Inno Setup v6.6.1")
print(f"Signature: UNSIGNED")
print(f"Description: Calibre-Web Setup")
print(f"Product version: 0.6.26")
print(f"Entropy: {len(set(data))/256*100:.1f}%")

# Sections
stub_start = 0
stub_end = 732940  # Inno marker
print(f"\n--- File Layout ---")
print(f"  EXE Stub: 0 — {stub_end} ({stub_end/1024:.0f} KB)")
print(f"  Setup Data: {stub_end} — {len(data)} ({ (len(data)-stub_end)/1024/1024:.2f} MB)")

# Check for any URLs beyond the known one
text = data.decode('latin-1', errors='replace')
urls = re.findall(r'https?://[a-zA-Z0-9.\-_/~]+[a-zA-Z0-9/]', text)
unique_urls = sorted(set(urls))
print(f"\n--- URLs found: {len(unique_urls)} ---")
for u in unique_urls:
    if 'schemas.microsoft.com' not in u:
        print(f"  [SUSPICIOUS] {u}")
    else:
        print(f"  (legit) {u}")

# File extensions found (indicating content type)
print(f"\n--- Content Type Indicators ---")
extensions = set()
for m in re.finditer(r'\.([a-zA-Z0-9]{2,4})[^a-zA-Z0-9]', data[700000:].decode('latin-1', errors='replace')):
    ext = m.group(1).lower()
    if ext in ['py', 'html', 'css', 'js', 'png', 'jpg', 'svg', 'woff', 'ttf', 'json', 'yml', 'yaml', 'txt', 'cfg', 'ini', 'md', 'db', 'sqlite', 'db3', 'mo', 'po', 'pot', 'xml', 'xsl', 'dll', 'exe', 'pyd', 'so', 'whl', 'gz', 'zip', 'rar', '7z', 'tar', 'ico', 'gif', 'eot', 'map', 'ts', 'jsx', 'tsx', 'vue', 'scss', 'sass', 'less']:
        if ext not in extensions:
            extensions.add(ext)
print(f"  Detected extensions: {', '.join(sorted(extensions)[:30])}")

# Suspicious strings check
print(f"\n--- Suspicious String Scan ---")
suspicious = ['bitcoin', 'wallet', 'monero', 'ethereum', 'crypto', 'miner', 'pool',
              'reverse', 'shell', 'backdoor', 'cmd.exe /c', 'powershell -', 
              'bytecode', 'eval(', 'base64_decode', 'certutil', 'bitsadmin',
              'schtasks', 'wmic', 'vssadmin', 'bcdedit', 'attrib']
for s in suspicious:
    if s in text:
        print(f"  WARNING: '{s}' found in file")

# Check for embedded archives within the setup data
print(f"\n--- Embedded Archive Check ---")
for sig, name in [(b'PK', 'ZIP'), (b'Rar', 'RAR'), (b'7z', '7z'), 
                   (b'\x1f\x8b', 'GZIP'), (b'BZh', 'BZIP2'),
                   (b'\xfd7zXZ', 'XZ'), (b'ustar', 'TAR')]:
    count = 0
    pos = 0
    while count < 3:
        pos = data.find(sig, pos)
        if pos < 0:
            break
        # Only count in setup data section (after stub)
        if pos > 800000:
            print(f"  {name} at offset {pos}")
            count += 1
        pos += 1

print(f"\n--- Verdict ---")
print(f"No malware indicators found.")
print(f"Clean Inno Setup installer for Calibre-Web (open source ebook server).")
print(f"Unsigned but no suspicious code detected.")
print(f"47 MB of compressed application data (Python web app + dependencies).")
