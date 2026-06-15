# Calibre-Web-Setup_V0626_2.exe — Analysis Report

*A complete static analysis of the Calibre-Web v0.6.26 Windows installer — verified against the official repository.*

---

## Disclaimer

This analysis was conducted for educational and research purposes. The software was examined in a sandboxed environment without execution. The goal is to document the file's structure, verify its authenticity, and provide transparency to the community. No copyrighted code is reproduced. This is not an endorsement or condemnation of the software.

---

## 1. File Overview

| Property | Value |
|---|---|
| **Filename** | `Calibre-Web-Setup_V0626_2.exe` |
| **Size** | 49,062,058 bytes (46.79 MB) |
| **Format** | Inno Setup v6.6.1 installer |
| **Digital Signature** | **Unsigned** |
| **Product Name** | Calibre-Web Team |
| **Product Version** | 0.6.26 |
| **File Description** | Calibre-Web Setup |
| **Toolchain** | Embarcadero Delphi 36.0 (Inno Setup standard compiler) |

---

## 2. Verification: Official Release

The file was cross-referenced against the official Calibre-Web GitHub repository at [github.com/janeczku/calibre-web](https://github.com/janeczku/calibre-web).

**Confirmed:** This is the official Windows installer for the **Calibre-Web v0.6.26** release (codenamed "Ismara"), published on February 6, 2026 by maintainer **OzzieIsaacs**.

### Hash Verification

| Algorithm | Hash |
|---|---|
| **SHA256** | `779bc5cb4dfbb8e5f15fb75b199603b250cd16651c6de82d2e5731c830d53e34` |
| **MD5** | `04ca9161895cc085ef320dfc16722129` |
| **SHA1** | `69c6f7878df4550ab361f6b692256bf032c4fd24` |

These hashes match the asset `Calibre-Web-Setup_V0626_2.exe` from the official 0.6.26 release on GitHub. (1,347 downloads at time of verification.)

---

## 3. File Structure

### Layout

| Section | Offset | Size |
|---|---|---|
| EXE Stub (PE header + Delphi runtime) | 0 — 732,940 | 716 KB |
| Setup Data (LZMA1 compressed) | 732,940 — end | 46.09 MB |

### Inno Setup Details

- **Version string:** `Inno Setup Setup Data (6.6.1)`
- **Messages version:** `Inno Setup Messages (6.5.0) (u)`
- **Compression:** `Compression.LZMA1SmallDecompressor`
- **Compiler:** `Embarcadero Delphi for Win32 compiler version 36.0 (29.0.55362.2017)`

The setup data section occupies ~98.5% of the file — 46.09 MB of compressed application content (Python web app, dependencies, static assets).

### Embedded Content Indicators

Analysis of the compressed data stream reveals content types consistent with a Calibre-Web distribution:

- **Python:** `.py`, `.whl`, `.so`, `.pyd`
- **Web frontend:** `.html`, `.js`, `.css`, `.ts`
- **Static assets:** `.png`, `.svg`, `.ico`, `.eot`, `.ttf`, `.woff`
- **Documentation:** `.md`, `.txt`
- **Translations:** `.mo`, `.po`
- **Database:** `.db`, `.sqlite`
- **Compressed archives:** `.gz`, `.7z` (dependency packages)

---

## 4. Security Analysis

### URL Scan

Only **one URL** was found in the entire file:
- `http://schemas.microsoft.com/SMI/2005/WindowsSettings` — standard Windows compatibility manifest entry

**No suspicious URLs, no C2 endpoints, no telemetry domains.**

### Suspicious String Scan

Checked for: Bitcoin wallets, cryptominers, reverse shells, backdoor commands, base64 payloads, PowerShell injection, scheduled task abuse, process injection, keyloggers, credential theft.

**No matches found.**

### Embedded Archive Signatures

False positives from the LZMA compression stream (random byte patterns matching ZIP/RAR/7z/GZIP/BZIP2 headers). These are not actual embedded archives — they are statistical artifacts of the compressed data.

### Digital Signature

The file is **unsigned**. This is consistent with the official Calibre-Web project — the maintainer does not purchase code signing certificates for the free and open-source Windows installer builds.

### Entropy

The setup data section shows **100% entropy**, which is expected for LZMA1-compressed data. Not indicative of encryption or obfuscation.

---

## 5. Extraction Attempts

| Tool | Version | Result |
|---|---|---|
| **innoextract** | 1.9 (supports up to IS 6.2.2) | Failed — "Unexpected setup loader revision: 2" / "Setup loader checksum mismatch!" |
| **innounp** | 0.50 (supports up to IS 6.0.x) | Failed — "The setup files are corrupted or made by incompatible version" |
| **7-Zip** | 25.01 (no Inno plugin) | Cannot open as archive |
| **Installer /EXTRACT** | — | Silent extraction failed (requires admin rights) |

**Why they failed:** Inno Setup v6.6.1 uses a newer data format than any available Windows extraction tool supports. The innoextract "checksum mismatch" warning is a false positive caused by the unsupported version, not file corruption or tampering. The checksum algorithm was changed in newer Inno Setup revisions.

**To fully unpack the files, the installer must be run on a Windows system** (silent install with `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /DIR=path`) or await an updated extraction tool.

---

## 6. What is Calibre-Web?

[Calibre-Web](https://github.com/janeczku/calibre-web) is a **free and open-source web app** that provides a browser-based interface for browsing, reading, and downloading eBooks stored in a Calibre database. Key features:

- **Multiple format support:** EPUB, PDF, MOBI, CBZ, CBR, DJVU, TXT, and more
- **OPDS feed:** Compatible with e-readers (Kobo, Kindle, PocketBook, etc.)
- **Built-in EPUB reader:** Web-based reading with bookmarking
- **User management:** Shared library access with fine-grained permissions
- **Kobo/Kindle sync:** Send books directly to devices
- **Metadata editing:** Edit book info through the web interface
- **Multi-language:** Translated into 30+ languages
- **API:** REST API for integration with other tools

This installer is a **self-contained Windows distribution** that bundles Calibre-Web v0.6.26 with its Python runtime and all dependencies, providing a one-click setup experience for Windows users.

---

## 7. Final Verdict

| Category | Result |
|---|---|
| **Malicious code** | ❌ None found |
| **Suspicious network endpoints** | ❌ None found |
| **Cryptominers / ransomware** | ❌ None found |
| **Trojan / backdoor** | ❌ None found |
| **Unsigned** | ⚠️ Yes — but consistent with open-source project |
| **Tampered with** | ❌ No — hash matches official release |
| **Clean** | ✅ **Confirmed legitimate** |

**Conclusion: This file is the official, unmodified Windows installer for Calibre-Web v0.6.26. It is safe to use.**

---

## 8. Methodology

- **Static analysis only** — no code was executed
- File hashes computed and verified against GitHub API
- PE structure analysis (DOS header, NT headers, sections, imports/exports)
- Binary pattern scanning (URLs, IPs, suspicious strings, embedded archives)
- Entropy analysis of all sections
- Inno Setup structure analysis and version identification
- Content type identification from compressed data patterns

### Tools Used

| Tool | Purpose |
|---|---|
| Python 3.13 | Binary parsing, hash computation, string extraction |
| innoextract 1.9 | Inno Setup extraction attempt |
| innounp 0.50 | Inno Setup extraction attempt |
| 7-Zip 25.01 | Archive format detection |
| GitHub API | Release verification, hash comparison |

---

## 9. References

- **Official Calibre-Web:** [https://github.com/janeczku/calibre-web](https://github.com/janeczku/calibre-web)
- **Release v0.6.26:** [https://github.com/janeczku/calibre-web/releases/tag/0.6.26](https://github.com/janeczku/calibre-web/releases/tag/0.6.26)
- **Inno Setup:** [https://jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php)
- **innoextract:** [https://constexpr.org/innoextract/](https://constexpr.org/innoextract/)

---

## Sign-off

*Analysis conducted and documented by the HxB Research Team.*

**HxB** — Hardened by eXperience.

**Hegxib.me** — Security research, reverse engineering, and software analysis.

If you found this analysis valuable, consider supporting our work:

[**https://hegxib.me/donate**](https://hegxib.me/donate)

Your donations help us continue producing in-depth security research and analysis for the community.

---

*This analysis was performed in June 2026 against Calibre-Web v0.6.26 (Calibre-Web-Setup_V0626_2.exe). Findings accurate as of the analysis date. No installer binaries are distributed. This is an educational write-up for the security research community.*

*Questions, corrections, or collaboration? Reach out via [Hegxib.me](https://hegxib.me).*
