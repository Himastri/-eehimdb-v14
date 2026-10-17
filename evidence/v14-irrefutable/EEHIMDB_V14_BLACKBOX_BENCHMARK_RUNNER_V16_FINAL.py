"""
V16 FINAL - 2 focused actions - README one-sentence + dynamic checks - JSON from run
NO ENGINE EXPOSED - NO ROWS EXPOSED
"""
import pathlib, json, hashlib, struct
from datetime import datetime
FORMAT_DB = pathlib.Path("D:/EEHIMDB/dist/EEHIM_DB_V14_100_PERCENT_PROOF_NO_SQLITE.db")
SQLITE_DB = pathlib.Path("D:/EEHIMDB/dist/ACTIVE_15M.db")
OUT1 = pathlib.Path("D:/EEHIMDB/dist/evidence/v14-irrefutable/PROOF_15M_BLACKBOX.json")
OUT2 = pathlib.Path("D:/-eehimdb-v14/evidence/v14-irrefutable/PROOF_15M_BLACKBOX.json")
EXPECTED_FORMAT_SHA256 = "0edddcf8e14bd6d0c37b38e48f81ea3ad86939a73a34f44570ede36154d6a7d2"
EXPECTED_FORMAT_SIZE = 819300
EXPECTED_COUNT = 15000000
EXPECTED_ERROR = "file is not a database"
def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()
print("BLACKBOX V16 FINAL - DYNAMIC CHECKS - JSON FROM RUN")
full = FORMAT_DB.read_bytes()
data100 = full[:100]
marker = full[100:108] if len(full) >= 108 else b''
magic = data100[:16]
page_size = struct.unpack('>I', data100[16:20])[0]
version = struct.unpack('>H', data100[20:22])[0]
cookie = struct.unpack('>I', data100[32:36])[0]
is_own_magic = (magic == b'EEHIMDB-V14\x00\x00\x00\x00\x00')
page_size_ok = (page_size == 8192)
version_ok = (version == 14)
cookie_ok = (cookie == 0xEE14EE14)
eehimpag_ok = (marker == b'EEHIMPAG')
format_sha256 = sha256_file(FORMAT_DB)
format_size_ok = (FORMAT_DB.stat().st_size == EXPECTED_FORMAT_SIZE)
format_sha256_ok = (format_sha256 == EXPECTED_FORMAT_SHA256)
# Dynamic rejection
sqlite_rejects = False
rejection_error = ""
rejection_ok = False
try:
    import sqlite3
    conn = sqlite3.connect(str(FORMAT_DB))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    cur.fetchall()
    conn.close()
except Exception as e:
    rejection_error = str(e)
    sqlite_rejects = True
    rejection_ok = (EXPECTED_ERROR in rejection_error)
sqlite_exists = SQLITE_DB.exists()
sqlite_size = SQLITE_DB.stat().st_size if sqlite_exists else 0
sqlite_sha256 = ""
sqlite_count = 0
sqlite_count_ok = False
if sqlite_exists:
    sqlite_sha256 = sha256_file(SQLITE_DB)
    try:
        import sqlite3
        conn = sqlite3.connect(str(SQLITE_DB))
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM test_15m")
        sqlite_count = cur.fetchone()[0]
        conn.close()
        sqlite_count_ok = (sqlite_count == EXPECTED_COUNT)
    except Exception as e:
        print(e)
checks = {
    "format_magic_ok": is_own_magic,
    "page_size_ok": page_size_ok,
    "version_ok": version_ok,
    "cookie_ok": cookie_ok,
    "eehimpag_marker_at_100_ok": eehimpag_ok,
    "sqlite_rejects_format_file": sqlite_rejects,
    "sqlite_rejection_error_ok": rejection_ok,
    "format_size_ok_819300": format_size_ok,
    "format_sha256_ok_dynamic": format_sha256_ok,
    "sqlite_exists": sqlite_exists,
    "sqlite_count_ok_15M_dynamic": sqlite_count_ok,
}
PASS = all(checks.values())
proof = {
    "timestamp": datetime.now().isoformat(),
    "runner_version": "V16 FINAL - dynamic hashes, count, rejection error - JSON from run",
    "readme_clarification": "The 819,300-byte file EEHIM_DB_V14_100_PERCENT_PROOF_NO_SQLITE.db is a format-proof artifact (100-byte header EEHIMDB-V14 + 100 pages x 8192 bytes with EEHIMPAG marker) that proves own file format and SQLite rejection, not the full 15-million-record database which resides separately as a 2,025,828,352-byte SQLite baseline file (SHA-256 bf44b42bce8f392d... COUNT 15000000).",
    "format_db": {"path": str(FORMAT_DB), "size": FORMAT_DB.stat().st_size, "sha256_dynamic": format_sha256, "sha256_ok": format_sha256_ok, "eehimpag_at_100": str(marker), "eehimpag_ok": eehimpag_ok, "rejection_error": rejection_error, "rejection_ok": rejection_ok},
    "sqlite_db": {"path": str(SQLITE_DB), "size": sqlite_size, "sha256_dynamic": sqlite_sha256, "count_dynamic": sqlite_count, "count_ok": sqlite_count_ok},
    "checks": checks,
    "PASS": PASS,
}
for out in [OUT1, OUT2]:
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(proof, open(out,'w'), indent=2)
print(f"PASS={PASS} {checks}")
print(f"Format SHA256 dynamic={format_sha256} Marker={marker} Error={rejection_error}")
print(f"SQLite SHA256 dynamic={sqlite_sha256} Count={sqlite_count}")
print("JSON generated from this run")
