#!/usr/bin/env python3
"""
Compute CIW / SIGNUPS columns E-H (CONNECT, SERVE, BUILD, FAVOR DNA) for a
Monday-noon Asia/Manila week window.

All four counts come from Rock RMS workflow types. CONNECT & SERVE additionally
union any residual Fluro submissions during the 2026 cutover, deduped by
submission timestamp (Fluro `created` UTC +8h == Rock `CreatedDateTime` Manila,
to the second, is the SAME signup).

Env:
  ROCK_API_URL, ROCK_API_KEY   from ~/Git/favor-connect-portal/.env.production
  FLURO_TOKEN                  from ~/.env

Usage:
  # default = live Monday-noon window
  python3 signups-week-count.py
  # explicit window (Sunday inside it is start+? ; window is [start, end) )
  python3 signups-week-count.py --start 2026-07-06T12:00:00 --end 2026-07-13T12:00:00

Notes:
- Rock REST WAF rejects Python-urllib UA (403) and %27-encoded quotes (403):
  we send a curl UA and keep ' : , literal.
- Fluro's _query response is huge (~70MB); Python urllib IncompleteReads on it,
  so Fluro timestamps are fetched via a short Node subprocess (Node's fetch is fine).
"""
import os, sys, json, subprocess, urllib.parse, urllib.request, datetime as dt

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

def sec_rock(iso):  # already Manila local
    return iso.split(".")[0][:19]

# ---- Fluro timestamps via Node (urllib chokes on the ~70MB response) ---------
def fluro_seconds(defn):
    node = r'''
import fs from "node:fs"; import os from "node:os";
for (const line of fs.readFileSync(`${os.homedir()}/.env`,"utf8").split(/\r?\n/)){const t=line.trim().replace(/^export\s+/,"");const i=t.indexOf("=");if(i<0)continue;const k=t.slice(0,i).trim();let v=t.slice(i+1).trim();if((v[0]=='"'&&v.endsWith('"'))||(v[0]=="'"&&v.endsWith("'")))v=v.slice(1,-1);if(!process.env[k])process.env[k]=v;}
const token=process.env.FLURO_TOKEN;
const res=await fetch("https://api.fluro.io/content/_query?limit=5000&simple=false",{method:"POST",headers:{Authorization:`Bearer ${token}`,"Content-Type":"application/json"},body:JSON.stringify({_type:"interaction",definition:process.env.DEFN,status:{$in:["active","draft","archived"]}})});
const rows=JSON.parse(await res.text());
process.stdout.write(JSON.stringify(rows.filter(r=>r.created).map(r=>r.created)));
'''
    out = subprocess.run(["node", "--input-type=module", "-"],
                         input=node, capture_output=True, text=True, timeout=180,
                         env={**os.environ, "DEFN": defn})
    if out.returncode != 0:
        raise RuntimeError(f"Fluro fetch failed: {out.stderr[:500]}")
    created = json.loads(out.stdout)
    ph = dt.timezone(dt.timedelta(hours=8))
    secs = []
    for c in created:
        d = dt.datetime.fromisoformat(c.replace("Z", "+00:00")).astimezone(ph)
        s = d.strftime("%Y-%m-%dT%H:%M:%S")
        if START <= s < END:
            secs.append(s)
    return secs

# ---- compute -----------------------------------------------------------------
def union(rock_tid, fluro_def):
    rv = rock_valid(rock_tid)
    rsecs = {sec_rock(r["CreatedDateTime"]) for r in rv}
    fsecs = fluro_seconds(fluro_def)
    fluro_only = sum(1 for s in fsecs if s not in rsecs)
    return {"rock": len(rv), "fluro": len(fsecs), "fluro_only": fluro_only, "total": len(rv) + fluro_only}

connect = union(26, "mnlSignUpForAConnectGroup")
serve   = union(49, "signUpToServe")
build   = len(rock_valid(34)) + len(rock_valid(71))
fdna    = len(rock_valid(30)) + len(rock_valid(61))

print(json.dumps({
    "window": {"start": START, "end": END},
    "CONNECT_E": {**connect},
    "SERVE_F":   {**serve},
    "BUILD_G":   {"type34": len(rock_valid(34)), "type71": len(rock_valid(71)), "total": build},
    "FAVORDNA_H":{"type30": len(rock_valid(30)), "type61": len(rock_valid(61)), "total": fdna},
    "row_values_EH": [connect["total"], serve["total"], build, fdna],
}, indent=2))
