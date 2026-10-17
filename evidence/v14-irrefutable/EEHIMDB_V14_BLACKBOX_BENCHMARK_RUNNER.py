"""
EEHIMDB-V14 BLACKBOX BENCHMARK RUNNER V15 - CLOSES 3 GAPS - NO ENGINE EXPOSED - NO ROWS EXPOSED
- Checks EEHIMPAG at offset 100
- Includes sqlite_count == 15M in PASS
- Records SHA256 for BOTH format file and SQLite file
- Per-check results, overall PASS only if all required checks succeed
- Documents that SQLite file must be present locally to reproduce count
Privacy: ONLY hashes, counts, sizes, markers - NO private engine, NO data rows
"""
import pathlib, json, hashlib, struct
from datetime import datetime

# --- CANDIDATES - format proof file 819300 bytes ---
FORMAT_CANDIDATES = [
    pathlib.Path("D:[STRIPPED 80 bytes].db"),
    pathlib.Path("D:/EEHIMDB/dist/EEHIM_DB_V14_100_PERCENT_PROOF_NO_SQLITE.db"),
    pathlib.Path("D:[STRIPPED 93 bytes].db"),
    pathlib.Path("D:[STRIPPED 67 bytes].db"),
]
SQLITE_DB = pathlib.Path("D:/EEHIMDB/dist/ACTIVE_15M.db")
OUT_JSON_DIST = pathlib.Path("D:/EEHIMDB/dist/evidence/v14-irrefutable/PROOF_15M_BLACKBOX.json")
OUT_JSON_GITHUB = pathlib.Path("D:/-eehimdb-v14/evidence/v14-irrefutable/PROOF_15M_BLACKBOX.json")

EXPECTED_FORMAT_SHA256 = "0edddcf8e14bd6d0c37b38e48f81ea3ad86939a73a34f44570ede36154d6a7d2"
EXPECTED_FORMAT_SIZE = 819300
EXPECTED_SQLITE_COUNT = 15000000

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

print("BLACKBOX V15 FINAL - CLOSES 3 GAPS - NO ENGINE EXPOSED - NO ROWS EXPOSED")
print("This runner expects local files. External reviewer cannot reproduce SQLite count without access to that DB.")
FORMAT_DB = None
for cand in FORMAT_CANDIDATES:
    if cand.exists():
        FORMAT_DB = cand
        print(f"FOUND FORMAT: {cand} Size={cand.stat().st_size}")
        break
    else:
        print(f"NOT FOUND FORMAT: {cand}")

if FORMAT_DB is None:
    print("FAILED: No format DB found")
    exit(1)

# --- Read header + marker ---
full = FORMAT_DB.read_bytes()
data100 = full[:100]
marker = full[100:108] if len(full) >= 108 else b''

magic = data100[:16]
page_size = struct.unpack('>I', data100[16:20])[0] if len(data100) >= 20 else 0
version = struct.unpack('>H', data100[20:22])[0] if len(data100) >= 22 else 0
cookie = struct.unpack('>I', data100[32:36])[0] if len(data100) >= 36 else 0

# --- Per-check ---
is_sqlite_magic = (magic == b'SQLite format 3\x00')
is_own_magic = (magic == b'EEHIMDB-V14\x00\x00\x00\x00\x00')
page_size_ok = (page_size == 8192)
version_ok = (version == 14)
cookie_ok = (cookie == 0xEE14EE14)
is_own = (is_own_magic and page_size_ok and version_ok and cookie_ok)
not_sqlite_magic = (not is_sqlite_magic)
eehimpag_marker_ok = (marker == b'EEHIMPAG')

format_sha256 = sha256_file(FORMAT_DB)
format_size_ok = (FORMAT_DB.stat().st_size == EXPECTED_FORMAT_SIZE)
format_sha256_ok = (format_sha256 == EXPECTED_FORMAT_SHA256)

# --- SQLite rejection test ---
try:
    import sqlite3
    conn = sqlite3.connect(str(FORMAT_DB))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    cur.fetchall()
    sqlite_rejects = False
    conn.close()
    print("sqlite3 SELECT sqlite_master succeeded - unexpected for EEHIM")
except Exception as e:
    sqlite_rejects = True
    print(f"sqlite3 SELECT sqlite_master FAILED as expected: {e}")

# --- SQLite 15M file ---
sqlite_exists = SQLITE_DB.exists()
sqlite_size = SQLITE_DB.stat().st_size if sqlite_exists else 0
sqlite_sha256 = ""
sqlite_count = 0
sqlite_count_ok = False
if sqlite_exists:
    print(f"Hashing SQLite DB {SQLITE_DB} Size={sqlite_size} - may take 30-60s for 2GB...")
    sqlite_sha256 = sha256_file(SQLITE_DB)
    print(f"SQLite SHA256={sqlite_sha256[:16]}... Size={sqlite_size}")
    try:
        import sqlite3
        conn = sqlite3.connect(str(SQLITE_DB))
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM test_15m")
        sqlite_count = cur.fetchone()[0]
        conn.close()
        sqlite_count_ok = (sqlite_count == EXPECTED_SQLITE_COUNT)
        print(f"SQLITE COUNT={sqlite_count} Expected={EXPECTED_SQLITE_COUNT} OK={sqlite_count_ok}")
    except Exception as e:
        print(f"SQLITE COUNT FAILED: {e}")
        sqlite_count_ok = False

# --- Overall PASS: ALL required checks must succeed ---
checks = {
    "format_magic_ok": is_own_magic,
    "page_size_ok": page_size_ok,
    "version_ok": version_ok,
    "cookie_ok": cookie_ok,
    "is_own": is_own,
    "not_sqlite_magic": not_sqlite_magic,
    "eehimpag_marker_at_100_ok": eehimpag_marker_ok,
    "sqlite_rejects_format_file": sqlite_rejects,
    "format_size_ok_819300": format_size_ok,
    "format_sha256_ok": format_sha256_ok,
    "sqlite_exists": sqlite_exists,
    "sqlite_count_ok_15M": sqlite_count_ok,
}
PASS = all(checks.values())

print("\n--- PER-CHECK RESULTS ---")
for k,v in checks.items():
    print(f"{k}: {v}")
print(f"\nOVERALL PASS={PASS} - requires ALL checks True")
print(f"Magic={magic} Marker@100={marker} Page={page_size} Ver={version} Cookie={hex(cookie)}")
print(f"Format SHA256={format_sha256} Size={FORMAT_DB.stat().st_size}")
print(f"SQLite SHA256={sqlite_sha256} Size={sqlite_size} Count={sqlite_count}")

proof = {
    "timestamp": datetime.now().isoformat(),
    "runner_version": "V15 - closes 3 gaps - EEHIMPAG@100, count in PASS, sqlite SHA256",
    "documentation": "Runner expects local files. External reviewer cannot reproduce SQLite count/hash without access to that DB or a verifiable test environment. No private engine imported. No data rows exposed. Only hashes, sizes, markers, counts.",
    "what_this_proves": {
        "format_signature_exists": "Supported if format_magic_ok True",
        "format_size_819300": "Recorded, bound to SHA256",
        "sqlite_rejects_proof_file": "Supported if sqlite_rejects_format_file True",
        "sqlite_15M_count": "Recorded, bound to SHA256 and size, requires local DB to reproduce",
        "private_engine_not_exposed": "Yes - runner does not import private engine",
        "limitations": "Does NOT by itself prove full engine SQLite-independent, nor that 819300-byte file physically stores 15M records. Proves published artifacts and measured checks."
    },
    "format_db": {
        "path": str(FORMAT_DB),
        "exists": True,
        "size": FORMAT_DB.stat().st_size,
        "size_ok": format_size_ok,
        "sha256": format_sha256,
        "sha256_ok": format_sha256_ok,
        "expected_sha256": EXPECTED_FORMAT_SHA256,
        "magic": str(magic),
        "magic_ok": is_own_magic,
        "page_size": page_size,
        "page_size_ok": page_size_ok,
        "version": version,
        "version_ok": version_ok,
        "cookie": hex(cookie),
        "cookie_ok": cookie_ok,
        "is_own": is_own,
        "not_sqlite_magic": not_sqlite_magic,
        "eehimpag_marker_at_100": str(marker),
        "eehimpag_marker_at_100_ok": eehimpag_marker_ok,
        "sqlite_rejects": sqlite_rejects,
        "hex_0_100": data100[:100].hex()[:160],
    },
    "sqlite_db": {
        "path": str(SQLITE_DB),
        "exists": sqlite_exists,
        "size": sqlite_size,
        "sha256": sqlite_sha256,
        "count": sqlite_count,
        "count_ok": sqlite_count_ok,
        "expected_count": EXPECTED_SQLITE_COUNT,
        "note": "SHA256 binds count to immutable file. External reviewer needs this file to reproduce."
    },
    "checks": checks,
    "PASS": PASS,
    "verdict": "PASS only if ALL checks True - FORMAT 819300 EEHIMDB-V14 8192 EEHIMPAG@100 0xEE14EE14 SHA256 0edddcf8 - SQLITE 15M bound to SHA256 COUNT 15000000 - NO ENGINE EXPOSED - NO ROWS EXPOSED"
}

for out in [OUT_JSON_DIST, OUT_JSON_GITHUB]:
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(proof, open(out,'w'), indent=2)
    print(f"Saved {out}")

print(f"\nVERDICT: PASS={PASS} - V15 FINAL - EEHIMPAG@100, COUNT in PASS, SQLITE SHA256 - NO ENGINE EXPOSED")
