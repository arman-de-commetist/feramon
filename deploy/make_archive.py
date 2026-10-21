"""Pack the site into mona-site.zip for the server.

    python deploy/make_archive.py              first install: code + database + photos
    python deploy/make_archive.py --code-only  update: code only (the server keeps its own orders and photos)
"""
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'mona-site.zip'
SKIP_DIRS = {'.venv', 'staticfiles', '__pycache__', '.claude', '.git', 'photos'}
SKIP_FILES = {'mona-site.zip', '.env'}
code_only = '--code-only' in sys.argv
if code_only:
    SKIP_DIRS.add('media')
    SKIP_FILES.add('db.sqlite3')

count = 0
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for path in sorted(ROOT.rglob('*')):
        rel = path.relative_to(ROOT)
        if path.is_dir() or set(rel.parts) & SKIP_DIRS or rel.name in SKIP_FILES or rel.suffix == '.pyc':
            continue
        # shell scripts must keep Unix line endings
        if rel.suffix == '.sh':
            z.writestr(rel.as_posix(), path.read_bytes().replace(b'\r\n', b'\n'))
        else:
            z.write(path, rel.as_posix())
        count += 1
print(f'{OUT.name}: {count} files, {OUT.stat().st_size / 1024 / 1024:.1f} MB' + (' (code only)' if code_only else ''))
