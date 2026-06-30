#!/usr/bin/env python3
"""
church_recount.py — mechanical engine for the `update-unique-churches` skill.

Operates purely on local JSON (fetch via Composio GOOGLESHEETS_VALUES_GET, or any
other client). The AGENT supplies judgment via curation.json + transforms.json;
this script does the deterministic extraction, matching, recount, and payload build.

Columns in the MASTERLIST are detected by HEADER TEXT, not fixed letters, because
the upstream export has drifted before (Order Status moved AW->BA; church fields
are N/S/T/AH/AI). Header-matching survives that drift.

Subcommands
-----------
  analyze  ML.json TABLE.json
      -> stated.json, matched.json, unmatched.json, zerorows.json  (+ printed summary)
  build    TABLE.json curation.json [transforms.json]
      -> new_table.json, summary.json  (reads matched.json from analyze)

File shapes
-----------
  ML.json / TABLE.json : the raw `values` 2-D arrays returned by VALUES_GET
    (ML must include the header row 1; TABLE is the Normalized tab from A1).
  curation.json : { "<exact raw string>": {"action":"existing","name":..,"city":..}
                                          | {"action":"new","name":..,"city":..,"status":..}
                                          | {"action":"drop"} }
  transforms.json (all optional):
    { "strip_parens": true,
      "apostrophe_fixes": {"Christ Commission Fellowship":"Christ’s Commission Fellowship"},
      "renames": [{"match":"Old Name|City","name":"New Name","city":"City","status":"Verified"}],
      "merges":  [{"into":"Name|City","absorb":["Other|City","Frag|—"]}],
      "prune_zeros": "all" }      # "all" | "fragments" | "none" (default "fragments")
"""
import json, re, sys

def norm_key(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())

def load_values(path):
    return json.load(open(path))

# ---------- MASTERLIST column detection (header-based) ----------
def detect_cols(header):
    idx = {}
    for i, h in enumerate(header):
        hl = (h or '').strip().lower()
        if hl == 'ticket' and 'ticket' not in idx:               idx['ticket'] = i
        if 'order status' in hl:                                  idx['status'] = i
        if 'which favor location' in hl:                          idx['favor'] = i
        if "church/ministry organization" in hl:                  idx['ch_org'] = i
        if hl.startswith('which church are you from') and 'church1' not in idx:
            idx['church1'] = i
        elif hl.startswith('which church are you from'):          idx['church2'] = i
        if 'which church do you come from' in hl:                 idx['church3'] = i
        if hl.startswith('if others'):                            idx['others'] = i
        if 'city where your church is located' in hl:             idx['ch_city'] = i
    # church-name fields in priority order (first non-blank wins)
    idx['church_fields'] = [idx[k] for k in
        ('ch_org','church1','church2','church3','others') if k in idx]
    return idx

BLANK = {'na','none','','wala','n','x','nq','none.'}
def is_blank(x):
    return norm_key(x) in BLANK
def is_favor(x):
    return (x or '').lower().startswith('favor') or 'favor church' in (x or '').lower()

def extract_stated(ml):
    header = ml[0]
    c = detect_cols(header)
    need = ('ticket','status')
    missing = [k for k in need if k not in c]
    if missing or not c.get('church_fields'):
        sys.exit(f"Header detection failed (missing {missing or 'church_fields'}). "
                 f"Inspect MASTERLIST headers; update detect_cols().")
    def g(row, i):
        return (row[i].strip() if i is not None and i < len(row) and row[i] else '')
    stated, favor, drop = [], 0, 0
    for row in ml[1:]:
        if g(row, c['status']).lower() != 'completed':   continue
        if g(row, c['ticket']) == 'Kids':                continue
        church = ''
        for fi in c['church_fields']:
            v = g(row, fi)
            if v and not is_blank(v) and not is_favor(v):
                church = v; break
        if church:
            stated.append({'church': church, 'city': g(row, c.get('ch_city'))})
        elif (not is_blank(g(row, c.get('favor')))) or any(is_favor(g(row, fi)) for fi in c['church_fields']):
            favor += 1
        else:
            drop += 1
    return stated, {'favor': favor, 'noChurch': drop, 'cols': {k: v for k, v in c.items() if k != 'church_fields'}}

# ---------- table parsing ----------
def parse_table(tbl):
    """Return list of dicts for data rows (idx = 0-based offset from row 4)."""
    rows = []
    for off, row in enumerate(tbl[3:]):           # data starts at sheet row 4
        if not row or not (row[0] or '').strip():  continue
        rows.append({
            'row': 4 + off,
            'name': row[0].strip(),
            'city': (row[1].strip() if len(row) > 1 else ''),
            'status': (row[2].strip() if len(row) > 2 else ''),
            'variants': [v.strip() for v in (row[4].split('|') if len(row) > 4 and row[4] else []) if v.strip()],
        })
    return rows

def build_variant_index(rows):
    v2i = {}
    for i, r in enumerate(rows):
        for s in r['variants'] + [r['name']]:
            v2i.setdefault(norm_key(s), i)
    return v2i

# ---------- analyze ----------
def cmd_analyze(ml_path, table_path):
    ml = load_values(ml_path); tbl = load_values(table_path)
    stated, meta = extract_stated(ml)
    rows = parse_table(tbl)
    v2i = build_variant_index(rows)
    matched = {}; unmatched = {}
    for rec in stated:
        k = norm_key(rec['church'])
        if k in v2i:
            matched[v2i[k]] = matched.get(v2i[k], 0) + 1
        else:
            unmatched[rec['church']] = unmatched.get(rec['church'], 0) + 1
    # zero rows after exact match, classify fragment-dup vs standalone
    def base(n): return norm_key(re.sub(r'\(.*?\)', '', n))
    nonzero_base = {base(rows[i]['name']) for i in matched if matched[i] > 0}
    zerorows = []
    for i, r in enumerate(rows):
        if matched.get(i, 0) == 0:
            kind = 'fragment-dup' if base(r['name']) in nonzero_base else 'standalone-0'
            zerorows.append({'row': r['row'], 'name': r['name'], 'city': r['city'],
                             'status': r['status'], 'kind': kind})
    json.dump(stated, open('stated.json', 'w'), ensure_ascii=False)
    json.dump({str(i): matched[i] for i in matched}, open('matched.json', 'w'))
    json.dump(sorted(unmatched.items(), key=lambda x: -x[1]), open('unmatched.json', 'w'), ensure_ascii=False)
    json.dump(zerorows, open('zerorows.json', 'w'), ensure_ascii=False)
    print(f"MASTERLIST: {len(ml)-1} rows | detected cols: {meta['cols']}")
    print(f"Stated a non-Favor church: {len(stated)} | Favor members: {meta['favor']} | no-church/junk: {meta['noChurch']}")
    print(f"Matched to existing rows: {sum(matched.values())} | UNCAPTURED people: {sum(unmatched.values())} ({len(unmatched)} distinct strings)")
    print(f"Existing rows that recompute to 0: {len(zerorows)} "
          f"({sum(1 for z in zerorows if z['kind']=='fragment-dup')} fragment-dup, "
          f"{sum(1 for z in zerorows if z['kind']=='standalone-0')} standalone)")
    print("\n--> Classify every string in unmatched.json into curation.json (existing/new/drop).")
    print("--> Review zerorows.json; decide prune policy in transforms.json.")
    print("\nUncaptured strings:")
    for s, n in sorted(unmatched.items(), key=lambda x: -x[1]):
        print(f"  {n:3d}  {s!r}")

# ---------- build ----------
def cmd_build(table_path, curation_path, transforms_path=None):
    tbl = load_values(table_path)
    rows = parse_table(tbl)
    matched = {int(k): v for k, v in json.load(open('matched.json')).items()}
    people = {s: n for s, n in json.load(open('unmatched.json'))}  # per-string head-count
    curation = json.load(open(curation_path))
    tr = json.load(open(transforms_path)) if transforms_path else {}

    for i, r in enumerate(rows):
        r['count'] = matched.get(i, 0)
        r['added'] = []
    by_namecity = {}
    for r in rows:
        by_namecity[(norm_key(r['name']), norm_key(r['city']))] = r
    def find_row(spec):  # "Name|City"
        nm, _, ci = spec.partition('|')
        return by_namecity.get((norm_key(nm), norm_key(ci)))

    new_rows = {}; unmapped = []
    for raw, c in curation.items():
        act = c.get('action')
        if act == 'drop':
            continue
        if act == 'existing':
            tgt = find_row(f"{c['name']}|{c.get('city','')}")
            if not tgt:
                cand = [r for r in rows if norm_key(r['name']) == norm_key(c['name'])]
                tgt = cand[0] if len(cand) == 1 else None
            if not tgt:
                unmapped.append(raw); continue
            tgt['count'] += people.get(raw, 1)
            if norm_key(raw) not in {norm_key(v) for v in tgt['variants'] + tgt['added']}:
                tgt['added'].append(raw)
        elif act == 'new':
            key = (norm_key(c['name']), norm_key(c.get('city', '')))
            nr = new_rows.setdefault(key, {'name': c['name'], 'city': c.get('city', '—'),
                                           'status': c.get('status', 'Unverified'), 'count': 0,
                                           'variants': [], 'added': [], 'is_new': True})
            nr['count'] += people.get(raw, 1)
            if norm_key(raw) not in {norm_key(v) for v in nr['variants']}:
                nr['variants'].append(raw)
        else:
            unmapped.append(raw)
    if unmapped:
        print("UNMAPPED (add to curation.json and re-run):")
        for s in unmapped: print("  ", repr(s))
        sys.exit(1)

    # assemble working rows (existing + new), fold 'added' into variants
    work = []
    for r in rows:
        r['variants'] = r['variants'] + [a for a in r['added'] if norm_key(a) not in {norm_key(v) for v in r['variants']}]
        work.append(r)
    for nr in new_rows.values():
        work.append(nr)

    # transforms: renames
    for rn in tr.get('renames', []):
        t = None
        nm, _, ci = rn['match'].partition('|')
        for r in work:
            if norm_key(r['name']) == norm_key(nm) and norm_key(r['city']) == norm_key(ci):
                t = r; break
        if t:
            if 'name' in rn: t['name'] = rn['name']
            if 'city' in rn: t['city'] = rn['city']
            if 'status' in rn: t['status'] = rn['status']
    # apostrophe / text fixes on names
    for a, b in tr.get('apostrophe_fixes', {}).items():
        for r in work:
            r['name'] = r['name'].replace(a, b)
    # strip trailing campus parenthetical — ONLY on pre-existing rows. New rows are
    # already named in final form by the agent (so a deliberate acronym like
    # "International Churches of Christ (ICOC)" on a new row is preserved).
    if tr.get('strip_parens'):
        for r in work:
            if r.get('is_new'):
                continue
            stripped = re.sub(r'\s*\([^)]*\)\s*$', '', r['name']).strip()
            r['name'] = stripped or r['name']
    # explicit merges
    def lookup(spec, pool):
        nm, _, ci = spec.partition('|')
        for r in pool:
            if norm_key(r['name']) == norm_key(nm) and norm_key(r['city']) == norm_key(ci):
                return r
        return None
    for mg in tr.get('merges', []):
        into = lookup(mg['into'], work)
        if not into: continue
        for spec in mg.get('absorb', []):
            src = lookup(spec, work)
            if not src or src is into: continue
            into['count'] += src['count']
            for v in src['variants']:
                if norm_key(v) not in {norm_key(x) for x in into['variants']}:
                    into['variants'].append(v)
            work.remove(src)

    # collision merge (same name+city after strip) + prune
    policy = tr.get('prune_zeros', 'fragments')
    def base(n): return norm_key(re.sub(r'\(.*?\)', '', n))
    merged = {}; collapsed = []
    for r in work:
        k = (norm_key(r['name']), norm_key(r['city']))
        if k in merged:
            m = merged[k]; m['count'] += r['count']
            for v in r['variants']:
                if norm_key(v) not in {norm_key(x) for x in m['variants']}:
                    m['variants'].append(v)
            if 'verified' == r['status'].lower() and m['status'].lower() == 'unverified':
                m['status'] = r['status']
        else:
            merged[k] = dict(r); collapsed.append(merged[k])
    nonzero_base = {base(r['name']) for r in collapsed if r['count'] > 0}
    final, pruned = [], []
    for r in collapsed:
        if r['count'] == 0:
            kind = 'fragment-dup' if base(r['name']) in nonzero_base else 'standalone-0'
            if policy == 'all' or (policy == 'fragments' and kind == 'fragment-dup'):
                pruned.append({'name': r['name'], 'city': r['city'], 'kind': kind}); continue
        if r['status'].lower().startswith('not a church'):
            pruned.append({'name': r['name'], 'city': r['city'], 'kind': 'non-church'}); continue
        final.append(r)

    final.sort(key=lambda r: (-r['count'], r['name'].lower()))
    matrix = [[r['name'], r['city'], r['status'], r['count'], ' | '.join(r['variants'])] for r in final]
    n = len(final)
    ver = sum(1 for r in final if r['status'] in ('Verified', 'Manually Verified'))
    unv = sum(1 for r in final if r['status'].lower() == 'unverified')
    total = sum(r['count'] for r in final)
    last = 3 + n
    summary = {'unique': n, 'verified': ver, 'unverified': unv, 'placed': total,
               'data_range': f"A4:E{last}", 'new_rows': len(new_rows),
               'pruned': pruned, 'dropped_actions': sum(1 for c in curation.values() if c.get('action') == 'drop'),
               'banner': f"OPEN ACCESS — UNIQUE CHURCHES (NORMALIZED): {n}   •   "
                         f"Verified: {ver}   ·   Unverified: {unv}",
               'plus30': [[r['name'], r['city'], r['count']] for r in final if r['count'] >= 30]}
    json.dump(matrix, open('new_table.json', 'w'), ensure_ascii=False)
    json.dump(summary, open('summary.json', 'w'), ensure_ascii=False)
    print(f"unique={n} verified={ver} unverified={unv} placed={total} new={len(new_rows)} pruned={len(pruned)}")
    print(f"data_range={summary['data_range']}  (clear A{last+1}:E<oldlast> if the table shrank)")
    print(f"30+ churches: {len(summary['plus30'])}")
    print("Wrote new_table.json + summary.json")

if __name__ == '__main__':
    a = sys.argv
    if len(a) >= 4 and a[1] == 'analyze':
        cmd_analyze(a[2], a[3])
    elif len(a) >= 4 and a[1] == 'build':
        cmd_build(a[2], a[3], a[4] if len(a) > 4 else None)
    else:
        print(__doc__); sys.exit(1)
