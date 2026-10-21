"""Compile locale/*/LC_MESSAGES/django.po into .mo without GNU gettext.

Django's own `compilemessages` needs gettext's msgfmt, which is usually missing on Windows.
Usage: python manage.py compiletranslations
"""
import ast
import struct

from django.conf import settings
from django.core.management.base import BaseCommand


def parse_po(text):
    """Return {msgid: msgstr} for a simple .po file (no plurals or contexts)."""
    entries, msgid, msgstr, current = {}, None, None, None

    def flush():
        if msgid is not None and msgstr is not None:
            entries[msgid] = msgstr

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('msgid '):
            flush()
            msgid, msgstr, current = ast.literal_eval(line[6:]), None, 'id'
        elif line.startswith('msgstr '):
            msgstr, current = ast.literal_eval(line[7:]), 'str'
        elif line.startswith('"'):
            if current == 'id':
                msgid += ast.literal_eval(line)
            else:
                msgstr += ast.literal_eval(line)
    flush()
    return entries


def write_mo(entries, path):
    entries = {k: v for k, v in entries.items() if v}  # untranslated entries fall back to Russian
    keys = sorted(entries)
    ids = strs = b''
    offsets = []
    for k in keys:
        kb, vb = k.encode('utf-8'), entries[k].encode('utf-8')
        offsets.append((len(ids), len(kb), len(strs), len(vb)))
        ids += kb + b'\0'
        strs += vb + b'\0'
    n = len(keys)
    keystart = 7 * 4 + 16 * n
    valuestart = keystart + len(ids)
    koffsets, voffsets = [], []
    for o1, l1, o2, l2 in offsets:
        koffsets += [l1, o1 + keystart]
        voffsets += [l2, o2 + valuestart]
    data = struct.pack('Iiiiiii', 0x950412de, 0, n, 7 * 4, 7 * 4 + n * 8, 0, 0)
    data += struct.pack('%di' % len(koffsets), *koffsets) + struct.pack('%di' % len(voffsets), *voffsets)
    path.write_bytes(data + ids + strs)
    return n


class Command(BaseCommand):
    help = 'Compile .po translation files to .mo (pure Python, no gettext needed).'

    def handle(self, *args, **options):
        for base in settings.LOCALE_PATHS:
            for po in sorted(base.glob('*/LC_MESSAGES/*.po')):
                n = write_mo(parse_po(po.read_text(encoding='utf-8')), po.with_suffix('.mo'))
                self.stdout.write(f'{po.relative_to(base)}: {n} strings')
