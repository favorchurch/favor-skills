#!/usr/bin/env python3
"""Build the variant -> normalized lookup that powers the CHECK-IN BY CHURCH tab.

The lookup lets the live sheet fold spelling variants into one church. It is generated from the
authoritative normalized list maintained by the `update-unique-churches` skill (that sheet's
"Church Count (Normalized)" tab, columns A=Name, B=City, E=Merged variants).

Usage:
    build_lookup.py CHURCH_COUNT_TABLE.json [out.json]

CHURCH_COUNT_TABLE.json may be either:
  - a raw 2-D array (rows of [Name, City, Status, Count, "variant | variant | ..."]), or
  - a Composio GOOGLESHEETS_VALUES_GET response (inline or storedInFile) for 'Church Count (Normalized)'!A4:E.

Output (default lookup.json): [["nkey","Normalized (Name | City)"], [nkey,label], ...] with a header row,
ready to write to 'CHURCH LOOKUP'!A1 with value_input_option=RAW.

nkey = lowercase then strip every non-alphanumeric char — identical to the sheet's
REGEXREPLACE(LOWER(x),"[^a-z0-9]",""), so exact + punctuation/spacing-insensitive matching lines up.
"""
import json, re, sys


def nk(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


def load_values(path):
    d = json.load(open(path))
    if isinstance(d, list):
        return d
    if isinstance(d, dict) and d.get('storedInFile'):
        d = json.load(open(d['outputFilePath']))
    stack = [d]
    while stack:
        o = stack.pop()
        if isinstance(o, dict):
            if 'values' in o and isinstance(o['values'], list):
                return o['values']
            stack.extend(o.values())
        elif isinstance(o, list):
            stack.extend(o)
    raise SystemExit("no 'values' array found in " + path)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: build_lookup.py CHURCH_COUNT_TABLE.json [out.json]")
    rows = load_values(sys.argv[1])
    out = sys.argv[2] if len(sys.argv) > 2 else 'lookup.json'
    lookup = {}  # nkey -> "Name | City"
    for r in rows:
        name = (r[0] if len(r) > 0 else '').strip()
        if not name:
            continue
        city = (r[1] if len(r) > 1 else '').strip()
        label = f"{name} | {city}" if city and city != '—' else name
        variants = r[4] if len(r) > 4 else ''
        keys = {nk(name)}
        for part in (variants or '').split('|'):
            p = part.strip().strip('…').strip()
            if p:
                keys.add(nk(p))
        for k in keys:
            if k and k not in lookup:   # first write wins (matches the church-count matcher)
                lookup[k] = label
    data = [['nkey', 'Normalized (Name | City)']] + [[k, v] for k, v in lookup.items()]
    json.dump(data, open(out, 'w'), ensure_ascii=False)
    print(f"wrote {out}: {len(data)} rows (incl header), {len(set(lookup.values()))} churches, "
          f"{len(lookup)} variant keys")


if __name__ == '__main__':
    main()
