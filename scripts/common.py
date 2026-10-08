"""Shared paths and helpers for the Sulfur pipeline.

Every script imports from here so no path is written twice. Run scripts from
anywhere; paths resolve from this file.
"""
import os, sys, time, json, datetime as dt, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
PROCESSED = ROOT / 'data' / 'processed'
SRC = ROOT / 'src'
DIST = ROOT / 'dist'

WAR_START = '2026-02-28'   # first strikes; Hormuz closed to dry bulk the same day


def keys():
    """Load the central D4TP keys. Never print a key."""
    sys.path.insert(0, os.path.expanduser('~/.claude/d4tp-process'))
    from d4tp_env import load_env, get_key
    load_env()
    return get_key


def _contact():
    # Contact address for the User-Agent: read at run time, never hardcoded in the repo.
    keys()
    return os.environ.get('D4TP_CONTACT_EMAIL', '')


UA = {'User-Agent': f'Data4ThePeople research {_contact()}'}


def get(url, tries=4, timeout=90, headers=UA):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout).read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def stamp(folder):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'pulled.txt').write_text(dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC') + '\n')


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, separators=(',', ':')))
