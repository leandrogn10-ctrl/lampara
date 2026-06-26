#!/usr/bin/env python3
"""La Lámpara — offline Bible bundle builder (reproducible).

Sources (both public domain / CC0):
  - BSB (English): https://bereanbible.com/bsb.txt   (publisher TSV, CC0)
  - RV1909 (Spanish): getbible v2 'valera' per-book JSON

Outputs (committed static assets, SW-cached, fetched on demand by the reader):
  - books.json   canonical 66-book table  [{id,en,es,nr,ch}]
  - bsb.json     {bookId: {chap: {verse: text}}}
  - rv1909.json  {bookId: {chap: {verse: text}}}

Everything anchors to canonical bookId (lowercased English, no spaces) + chap + verse,
matching the NTV API's <verse_export bk ch vn> convention so panes align on refs.
Run:  python3 build.py
"""
import json, re, sys, urllib.request

BSB_URL = "https://bereanbible.com/bsb.txt"
GETBIBLE = "https://api.getbible.net/v2/valera/{nr}.json"
UA = {"User-Agent": "Mozilla/5.0 (lampara-build)"}

# Canonical 66 — order/EN names verified against the real BSB file; ES = standard names.
EN = ["Genesis","Exodus","Leviticus","Numbers","Deuteronomy","Joshua","Judges","Ruth",
"1 Samuel","2 Samuel","1 Kings","2 Kings","1 Chronicles","2 Chronicles","Ezra","Nehemiah",
"Esther","Job","Psalm","Proverbs","Ecclesiastes","Song of Solomon","Isaiah","Jeremiah",
"Lamentations","Ezekiel","Daniel","Hosea","Joel","Amos","Obadiah","Jonah","Micah","Nahum",
"Habakkuk","Zephaniah","Haggai","Zechariah","Malachi","Matthew","Mark","Luke","John","Acts",
"Romans","1 Corinthians","2 Corinthians","Galatians","Ephesians","Philippians","Colossians",
"1 Thessalonians","2 Thessalonians","1 Timothy","2 Timothy","Titus","Philemon","Hebrews",
"James","1 Peter","2 Peter","1 John","2 John","3 John","Jude","Revelation"]
ES = ["Génesis","Éxodo","Levítico","Números","Deuteronomio","Josué","Jueces","Rut",
"1 Samuel","2 Samuel","1 Reyes","2 Reyes","1 Crónicas","2 Crónicas","Esdras","Nehemías",
"Ester","Job","Salmos","Proverbios","Eclesiastés","Cantares","Isaías","Jeremías",
"Lamentaciones","Ezequiel","Daniel","Oseas","Joel","Amós","Abdías","Jonás","Miqueas","Nahúm",
"Habacuc","Sofonías","Hageo","Zacarías","Malaquías","Mateo","Marcos","Lucas","Juan","Hechos",
"Romanos","1 Corintios","2 Corintios","Gálatas","Efesios","Filipenses","Colosenses",
"1 Tesalonicenses","2 Tesalonicenses","1 Timoteo","2 Timoteo","Tito","Filemón","Hebreos",
"Santiago","1 Pedro","2 Pedro","1 Juan","2 Juan","3 Juan","Judas","Apocalipsis"]
assert len(EN) == len(ES) == 66

def slug(name):  # "1 Samuel" -> "1samuel", "Song of Solomon" -> "songofsolomon"
    return re.sub(r'[^a-z0-9]', '', name.lower())

ID = [slug(n) for n in EN]
EN2ID = {EN[i]: ID[i] for i in range(66)}
BOOKS = [{"id": ID[i], "en": EN[i], "es": ES[i], "nr": i + 1} for i in range(66)]

def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()

def build_bsb():
    print("• BSB: downloading", BSB_URL)
    txt = fetch(BSB_URL).decode("utf-8-sig")
    out = {}
    n = 0
    for line in txt.splitlines():
        if "\t" not in line:
            continue
        ref, text = line.split("\t", 1)
        m = re.match(r'^(.*?)\s+(\d+):(\d+)$', ref.strip())
        if not m:
            continue  # header rows
        bk, ch, vs = m.group(1), m.group(2), m.group(3)
        bid = EN2ID.get(bk)
        if not bid:
            raise SystemExit(f"BSB: unknown book name {bk!r}")
        out.setdefault(bid, {}).setdefault(ch, {})[vs] = text.strip()
        n += 1
    print(f"  parsed {n} verses, {len(out)} books")
    return out

def build_rv():
    print("• RV1909: downloading 66 books from getbible")
    out = {}
    n = 0
    for i in range(66):
        bid = ID[i]
        d = json.loads(fetch(GETBIBLE.format(nr=i + 1)))
        for ch in d["chapters"]:
            c = str(ch["chapter"])
            for v in ch["verses"]:
                out.setdefault(bid, {})[c] = out.get(bid, {}).get(c, {})
                out[bid][c][str(v["verse"])] = v["text"].strip()
                n += 1
        sys.stdout.write("."); sys.stdout.flush()
    print(f"\n  parsed {n} verses, {len(out)} books")
    return out

def validate(name, data):
    assert len(data) == 66, f"{name}: expected 66 books, got {len(data)}"
    total = sum(len(vs) for b in data.values() for vs in b.values())
    # spot checks
    assert data["genesis"]["1"]["1"], f"{name}: Gen 1:1 missing"
    assert data["john"]["3"]["16"], f"{name}: John 3:16 missing"
    assert data["revelation"]["22"]["21"], f"{name}: Rev 22:21 missing"
    print(f"  ✓ {name}: 66 books, {total} verses, Gen1:1 / John3:16 / Rev22:21 present")
    return total

if __name__ == "__main__":
    bsb = build_bsb()
    rv = build_rv()
    tb = validate("BSB", bsb)
    tr = validate("RV1909", rv)
    # chapter-count per book from BSB (canonical) → into books.json
    for b in BOOKS:
        b["ch"] = len(bsb[b["id"]])
    for fn, obj in [("books.json", BOOKS), ("bsb.json", bsb), ("rv1909.json", rv)]:
        with open(fn, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
        print(f"  wrote {fn}")
    print(f"DONE — BSB {tb} verses, RV1909 {tr} verses")
