# La Lámpara — project guide

**"Tu palabra es lámpara" — a lifetime study Bible.** Single-file PWA forked from the
**app-shell template (C3)**, own private gist (`lampara.json`), GitHub Pages.
**Status: DESIGN** (plan drafted Jun 25 2026; partial build in `index.html` + `data/`).
Read `LA-LAMPARA-PLAN.md` in full before building anything — the boundaries below are architectural,
not cosmetic, and the plan is the source of truth.

## Identity (NEVER drift from this — these are hard lines)
- **Never gamified.** No streaks, no badges, no "you missed N days" guilt. Grounding: the
  overjustification effect — extrinsic reward mechanics corrode intrinsic motivation, and gamifying
  devotion actively poisons it. The oil-lamp measures **territory covered over a lifetime**, never
  consecutive days.
- **Claude is a rigorous scholar AND a thoughtful interlocutor — never a priest.** It does history,
  Hebrew/Greek, literary structure, the range of scholarly/traditional readings, and *will* connect a
  passage to Leandro's real life — but it **never speaks for God** ("God is telling you…"), never
  pronounces a final verdict on his decisions, never substitutes for his pastor/church. Application is
  offered as grounded, cited, plural possibilities held with humility. This boundary IS his Protestant
  theology (priesthood of all believers).
- **Never lock the user out of their own words.** Offline-first, exportable, gist-owned. A lifetime of
  verse-anchored marginalia is *his* — it must outlive any server, translation, or app version.
- **Never a YouVersion clone.** The point is the accreting personal corpus + the scholar, not social
  verses-of-the-day.

## Translation architecture (the licensing spine — do not bundle copyrighted text)
- **Offline floor (bundled, CC0/PD, always works):** **BSB** (modern English, CC0) ∥ **RV1909**
  (PD Spanish, archaic but legal offline). This is the fallback when there's no network.
- **Live panes (online-only, copyrighted):** preferred **NTV** via Tyndale's free `api.nlt.to`
  (≤500 verses/req, optional free key) — primary Spanish daily read. **TLA** uncertain (no confirmed
  free API) — pursue via API.Bible/UBS in Phase A, **NTV is the fallback; don't block the build on TLA.**
  Optional English live: NLT (Tyndale) / ESV (Crossway key).

## Plumbing & dev loop
Inherits the app-shell engine (gist sync, theme vars, `callClaude`, `cleanStateForSync`,
`looksLikeMyState` — **tighten it for `lampara.json`**). Backport shell fixes by hand from
`~/Projects/app-shell/shell.html`. Single-file, no build.
```bash
python3 -m http.server 8000   # http://localhost:8000/  — never file://, bump the port to dodge stale SW
```
**Visual identity:** decided at build time via the frontend-design skill — distinctive type, cohesive
dominant color; no Inter/Space Grotesk, no AI-slop, content (the Word + marginalia) over chrome.
