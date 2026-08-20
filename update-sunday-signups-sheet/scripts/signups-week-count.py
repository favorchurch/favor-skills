#!/usr/bin/env python3
"""
Compute CIW / SIGNUPS columns E-H (CONNECT, SERVE, BUILD, FAVOR DNA) for a
Monday-noon Asia/Manila week window.

All four counts come from Rock RMS workflow types only. Fluro has been
decommissioned as of the 2026-07 cutover completing — no Fluro querying or
dedup/union step is needed anymore.

Env:
  ROCK_API_URL, ROCK_API_KEY   from ~/Git/connect.favor.church/.env.production
                               (this repo was formerly named favor-connect-portal)

Usage:
  # default = live Monday-noon window
  python3 signups-week-count.py
  # explicit window (Sunday inside it is start+? ; window is [start, end) )
  python3 signups-week-count.py --start 2026-07-06T12:00:00 --end 2026-07-13T12:00:00

Notes:
- Rock REST WAF rejects Python-urllib UA (403) and %27-encoded quotes (403):
  we send a curl UA and keep ' : , literal.
"""
import os, sys, json, urllib.parse, urllib.request, datetime as dt

# ---- args / window -----------------------------------------------------------
def arg(name, default=None):
    a = sys.argv
    return a[a.index(name) + 1] if name in a else default

def live_window():
    ph = dt.timezone(dt.timedelta(hours=8))
    now = dt.datetime.now(ph)
    cutoff = (now - dt.timedelta(days=(now.weekday()))).replace(hour=12, minute=0, second=0, microsecond=0)
    if cutoff > now:
        cutoff -= dt.timedelta(days=7)
    start = cutoff - dt.timedelta(days=7)
    fmt = lambda d: d.strftime("%Y-%m-%dT%H:%M:%S")
    return fmt(start), fmt(cutoff)

lw = live_window()
START = arg("--start", lw[0])
END = arg("--end", lw[1])

# ---- Rock REST ---------------------------------------------------------------
BASE = os.environ["ROCK_API_URL"].rstrip("/")
KEY = os.environ["ROCK_API_KEY"]
def rget(path):
    req = urllib.request.Request(BASE + path, headers={"Authorization-Token": KEY, "User-Agent": "curl/8.7.1"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)
_rows_cache = {}
def rock_rows(tid):
    if tid not in _rows_cache:
        f = (f"WorkflowTypeId eq {tid} and CreatedDateTime ge datetime'{START}' "
             f"and CreatedDateTime lt datetime'{END}'")
        q = urllib.parse.quote(f, safe="'" + ":,/")
        _rows_cache[tid] = rget(f"/Workflows/?$filter={q}&$select=Id,Name,Status,CreatedDateTime&$top=1000")
    return _rows_cache[tid]

def rock_valid(tid):
    """Real signups only: drop 'Delivery Failed' rows (CONNECT accrues empty failed
    submissions). NB: BUILD/FDNA rows are legitimately named 'New Form', so do NOT
    filter on Name — only on Status."""
    return [r for r in rock_rows(tid) if r.get("Status") != "Delivery Failed"]

# ---- compute -----------------------------------------------------------------
connect = len(rock_valid(26))
serve   = len(rock_valid(49))
build   = len(rock_valid(34)) + len(rock_valid(71))
fdna    = len(rock_valid(30)) + len(rock_valid(61))

print(json.dumps({
    "window": {"start": START, "end": END},
    "CONNECT_E": connect,
    "SERVE_F":   serve,
    "BUILD_G":   {"type34": len(rock_valid(34)), "type71": len(rock_valid(71)), "total": build},
    "FAVORDNA_H":{"type30": len(rock_valid(30)), "type61": len(rock_valid(61)), "total": fdna},
    "row_values_EH": [connect, serve, build, fdna],
}, indent=2))
