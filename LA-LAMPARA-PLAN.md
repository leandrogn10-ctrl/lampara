# La Lámpara — "Tu palabra es lámpara" (Faith app)

Plan drafted Jun 25 2026. Status: **DESIGN — not yet scheduled. Awaiting Leandro's feature sign-off.**
Lives at `~/Projects/lampara` → GitHub Pages PWA, own private gist (`lampara.json`), forked from
`~/Projects/app-shell` (C3). Wires back to the city later (Setup gist field + `read_lampara` chat
tool + Bible-habit bridge, mirroring La Forja → Gym).

## One-sentence spec
A lifetime study Bible: a **bilingual parallel canon** you read offline, **annotate in the margins
forever** (verse-anchored notes that accrete across years), with **Claude as a rigorous scholar**
(history, original languages, cross-references — never a pastor), and an **oil-lamp** that measures how
much of the Word you've walked through — **no streaks, no guilt, no gamification.**

## What it must NEVER be
- **Never gamified.** No streaks, no badges, no "you missed 3 days" guilt. This is architectural, not
  cosmetic. Grounding: the **overjustification effect** (well-documented in motivation psychology —
  Deci, Lepper) — extrinsic reward mechanics reliably *corrode* intrinsic motivation. Gamifying
  devotion is not neutral; it actively poisons the thing. The lamp measures *territory covered over a
  lifetime*, never *consecutive days*.
- **Never a devotional-pablum machine, never plays priest.** Claude is a **scholar AND a thoughtful
  interlocutor** (Leandro's call, Jun 25): it does history, Hebrew/Greek, literary structure, the range
  of scholarly/traditional readings, AND it *will* connect a passage to his actual life (19, the Bain
  track, Georgetown, ambition/vocation), answer his questions, and explore how different traditions
  *apply* it. The line it does NOT cross: it never claims to **speak for God** ("God is telling you…"),
  never pronounces a final verdict on his decisions, never poses as a substitute for his pastor or
  church. It informs, provokes, asks — *Leandro* (with the Spirit and his community) discerns. This
  boundary IS his own Protestant theology (priesthood of all believers); application is offered as
  grounded possibilities and good questions, held with humility, plural and cited.
- **Never lock you out of your own words.** Offline-first, exportable, gist-owned. A lifetime of
  marginalia is *yours* — it must outlive any server, any translation, any version of this app.
- **Never a YouVersion clone.** The point is the *accreting personal corpus* + the *scholar*, not
  social verses-of-the-day.

## THE TRANSLATION ARCHITECTURE (Leandro's preferred = NTV / TLA — both copyrighted, so online-first)
Leandro reads **NTV** (Nueva Traducción Viviente) and **TLA** (Traducción en Lenguaje Actual). Neither
can be bundled offline (both copyrighted, 500-verse ceiling). But both can be *served live*:
- **NTV — confirmed, clean.** Tyndale's own free API `api.nlt.to` serves NTV + NLT, non-commercial,
  ≤500 verses/request, optional free key. → **NTV is the primary live daily-read Spanish pane.**
- **TLA — uncertain.** © Sociedades Bíblicas Unidas 2002/2004; no confirmed free API (YouVersion has no
  public API). Path: request via API.Bible / UBS licensing — **pursue in Phase A, NTV is the fallback
  if it doesn't land.** Don't block the build on TLA.
- **English live pane:** NLT (Tyndale API, English twin of NTV) and/or ESV (Crossway key) — optional.

**The offline floor (bundled, CC0/PD, always works, no network):** **BSB** (modern English, CC0) ∥
**RV1909** (PD Spanish — archaic, but it's the legal offline Spanish). This is the fallback when there's
no network, never the forced daily driver.

**The reconciliation (online-first, never locked out):**
- Reading is **online-first** in NTV/TLA; a **rolling ≤500-verse cache** of recently-read chapters
  keeps the *real* translation available offline *within the legal storage limit* (evicted FIFO past
  500). So a plane ride still has your last several chapters of actual NTV.
- **His data — marginalia, plans, memory, xrefs — is 100% offline, always**, in the gist. Only the
  copyrighted TEXT needs a network. The PD bundle guarantees he can always open *a* Bible.
- **Everything anchors to verse references** (`book.chap.verse`, BSB versification), which are
  translation-independent and public — so a note written in NTV today survives a switch to TLA, ESV,
  RV1909, or the app's death. Refs are the bedrock; translations are interchangeable lenses over them.

Source files / endpoints to pin in Phase A: NTV via `api.nlt.to` (get a key); TLA via API.Bible
request (or shelve); BSB JSON (bsb.freely.giving / bereanbible.com tables) + RV1909 JSON (getbible v2 /
seven1m/open-bibles) for the offline bundle; Strong's (PD) + Berean Interlinear (free) for word studies.

## Data model (gist `lampara.json`, los-state union-merge like the other apps)
- **`notes[]`** — the spine. `{id, ref:'john.3.16', refEnd?, kind:'note|highlight|question|prayer|xref',
  body, color?, lang?, created, updated, tags[]}`. `ref` is canonical (BSB versification). A range note
  carries `refEnd`.
- **`memory[]`** — verses marked to memorize → exported as F2 recall cards. `{ref, lang:'es|en|both',
  added, lastReviewed?}`.
- **`xrefs[]`** — personal cross-reference edges `{from:'rom.5.8', to:'john.3.16', note?}` → the
  personal web (constellation pattern).
- **`plans[]`** — reading paths `{id, name, kind:'mcheyne|chrono|book|topical|custom', refs:[...ranges],
  position, paused?}`. Position is a pointer, not a streak; pausing carries no penalty.
- **`progress`** — `{readRefs: bitset/run-length of every verse ever opened}` → drives the lamp +
  the canon map. Lifetime cumulative, monotonic (it only ever fills).
- **`settings`** — parallel layout, default langs, ESV/RVR1960 keys (optional), font scale.
- Bible TEXT itself is NOT in the gist (it's the bundled static PD asset) — the gist holds only HIS
  layer. Keeps the gist small and the text immutable.

## Feature list — VETO ANYTHING (Leandro: "tell me what features you want to add")
**Tier 1 — the spine (MVP, Phase A–B):**
1. **Bilingual parallel reader** — BSB ∥ RV1909, verse-aligned, tap a verse to focus. Smooth chapter
   nav, book grid, search across the bundled text.
2. **Verse-anchored lifetime marginalia** — select verse(s) → note / highlight / question / prayer /
   cross-ref. Anchored to refs, accreting forever. An annotated verse glows faintly (the lamp lights
   verses you've touched). The margin becomes a personal study Bible you build over years.
3. **The Lamp (progress, not streaks)** — an oil lamp whose light grows as cumulative canon-territory
   covered grows; a faint **canon map** (66 books) lights up book-by-book as you read. "How much of the
   Word have you walked through" — lifetime cartography, zero daily pressure, no break to "lose."

**Tier 2 — the scholar (Phase C):**
4. **Claude as Scholar + Interlocutor** — select a passage → historical/cultural context, **Hebrew/Greek
   word study** (PD Strong's + interlinear), literary structure, **the plural range of scholarly &
   traditional readings** (Catholic / Orthodox / Reformed / critical, side by side, cited — Leandro is
   Protestant but wants the fuller room), **AND lived application** to his situation + free-form Q&A.
   Guardrail (above): explores/provokes/asks, never speaks-for-God / pronounces / replaces a pastor;
   says "I don't know" over inventing. Sub-mode aware (Max plan via helper, like the city) so it's ~free.
5. **Memory verses → F2 recall** — mark a verse to memorize → becomes a recall card (bilingual),
   feeding the August recall deck. Verse-anchored, survives translation switches.

**Tier 3 — the lifetime corpus (Phase D):**
6. **Marginalia search & synthesis** — query *your own* years of notes ("what have I written about
   suffering / la gracia?"). Claude synthesizes HIS corpus (distinct from interpreting Scripture — this
   is reading *him*, with consent). A personal theology you can actually retrieve.
7. **Personal cross-reference web** — verses you've linked form a navigable graph (the Bitácora
   constellation, applied to Scripture). Walk from Romans 5 to John 3 along edges you drew.
8. **Reading paths** — M'Cheyne / chronological / book-study / topical, plus **Claude-generated custom
   plans** ("understand Pauline theology in 6 weeks"). Pause/resume guilt-free; a path, not a chain.

**Tier 4 — city integration (later, city-side):**
9. **Bible-habit bridge** — reading activity auto-marks `streak.bible` (idempotent union-merge, like
   La Forja → Gym). **Log the activity into `los.stats` even though content stays out of Wrapped/digests
   by default** — recording ≠ surfacing; preserves the no-gamification stance while keeping a future
   gentle "a steady week in the Word" *opt-in* possible (don't throw the signal away).
10. **`read_lampara` city tool** — the city chat's Claude can see (with consent) recent reading +
    memory verses for "prep me for tomorrow" synthesis across organs.
11. **Quiet ambient echo (optional, deferred)** — at most a single gentle nod in the city (a lamp lit
    on a roof at night), NEVER a gamified reward. Pitch later; easy to cut.

## Identity / aesthetic (distinct from the city + other apps)
Oil-lamp warmth: deep ink ground, **amber/flame accent** (not the city's gold-on-navy — warmer, more
candlelit), a **single serif with real character** for the text (a humanist or transitional serif —
NOT Inter/Roboto/system; candidate: a Garamond-class or **Cormorant/Spectral**-class face for the
Scripture, a quiet mono for chrome). Psalm 119:105 as the seed. Layered, low, contemplative motion —
a flame's flicker, not the city's staggered reveals. Self-hosted fonts (no FOUT).

## Build phases
- **Phase A — spine + data:** fork app-shell → lampara; pin + bundle BSB + RV1909 JSON; versification
  map; offline reader (parallel, nav, search); gist sync (`looksLikeMyState` guard); lamp identity. No
  Claude yet. Ships as a usable offline bilingual Bible.
- **Phase B — marginalia:** verse-anchored notes/highlights/memory; the glow; the lamp + canon map;
  export. The spine feature — this is the soul; get it right before anything clever.
- **Phase C — the scholar:** Claude study panel (context / word study / plural readings), guardrailed +
  sub-mode aware; memory-verse → recall-card export.
- **Phase D — the corpus:** marginalia search/synthesis, cross-ref web, reading paths (+ custom).
- **Phase E — city wiring:** Bible-habit bridge + `read_lampara` tool + the log-don't-surface ledger
  emission; (optional) ambient echo.

## Settled with Leandro (Jun 25)
- **Translations:** primary = **NTV** live (Tyndale API), **TLA** live if obtainable (else NTV only);
  PD offline floor = BSB ∥ RV1909; rolling ≤500-verse cache for partial-offline of the real text.
- **Claude = scholar + interlocutor** (applies to life + answers questions), with the never-plays-priest
  boundary; **plural traditions by default**, Protestant home base.

## Settled — round 2 (Jun 26) → DESIGN LOCKED
- **Online-first is fine.** Don't over-engineer offline. Reading is live NTV; the rolling ≤500-verse
  cache covers the plane case; PD bundle is the never-locked-out floor; his data is always offline.
- **Defer TLA.** Ship on NTV (Tyndale API, confirmed). Add TLA later only if API.Bible/UBS access lands;
  never block the build on it.
- **Keep #7 (cross-ref web), build it LAST.** Stays in Phase D, after the marginalia + scholar core
  prove out. Cut without grief if it's not pulling weight.

**→ Plan is LOCKED. Phase A is the next build session.**

## Phase A kickoff checklist (the next session's first moves)
1. **Leandro:** request a free **NTV/NLT API key** at `api.nlt.to` (only he can sign up). Anonymous use
   works for a spike; the key lifts limits.
2. Fork `~/Projects/app-shell` → `~/Projects/lampara` (lamp identity: amber/flame, Cormorant/Spectral-class
   serif, Psalm 119:105 seed). `git init`, own private gist `lampara.json`.
3. Pin + vendor the offline bundle: **BSB JSON** (bsb.freely.giving / bereanbible.com) + **RV1909 JSON**
   (getbible v2 / seven1m/open-bibles); normalize to one ref schema (`book.chap.verse`, BSB versification).
4. Build the parallel offline reader (BSB ∥ RV1909) + book/chapter nav + bundled-text search; wire NTV
   live pane via `api.nlt.to` with the rolling ≤500-verse session cache. No marginalia/Claude yet.
5. Gist sync from the shell (`looksLikeMyState` guard). Ship a usable bilingual reader; THEN Phase B
   (marginalia — the soul).
