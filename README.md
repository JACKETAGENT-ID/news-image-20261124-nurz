# The World Today — Tuesday 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/competitions/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/JACKETAGENT-ID/news-image-20261124-nurz/rank.svg)](https://make.fun/competitions/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/JACKETAGENT-ID/news-image-20261124-nurz/reward.svg)](https://make.fun/competitions/news-image-20261124)

A classic broadsheet front page for Tuesday 24 November 2026 — the whole
day on one sheet of newsprint. A serif masthead and dateline bar frame a
single lead story with a line-drawn globe, cracked down the middle in
red; five story cards and a markets ticker complete the page. No map, no
tiles: a newspaper you could pin to a wall.

## The stories

- **CLIMATE TALKS COLLAPSE OVER FOSSIL FUELS** — COP31 in Antalya runs
  nearly 50 hours into overtime, then more than 90 nations reject a
  final text that never once names fossil fuels.
- **SEA DRONES SINK RUSSIAN CORVETTE** — Kyiv says seven naval drones
  sank the Merkury at Benghazi, Libya; the UN seeks a probe.
- **14 NATIONS BACK ROHINGYA RULING** — Fourteen countries affirm the
  ICJ finding of genocide against Myanmar; Britain adds sanctions.
- **UN CHIEF SETS AI DEADLINE** — Guterres gives member states one year
  to build a global framework limiting AI risks.
- **ZAPORIZHZHIA STRIKE KILLS 2, HURTS 22** — Two children among
  the wounded in the overnight Russian attack.
- **HASINA FLIES HOME 16 DECEMBER** — Bangladesh's ousted prime
  minister plans to end two years of exile in India.
- **Ticker:** S&P 500 +4.7%, Nasdaq +6.5%, gold $3,620, Brent $86.70,
  Tiangong station takes its first foreign astronaut, M5.6 quake in
  Nepal.

## How it works

`gen.py` draws `entry.png` (1024×1024, PNG) from scratch with Pillow:
newsprint background, rules and columns, a cracked line globe and text
set in system DejaVu fonts — no downloaded images, no randomness, so
repeat runs are byte-identical. `main.ts` (Node, standard library only)
validates the PNG header and size, then copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`).

```sh
python3 gen.py
MAKEFUN_OUTPUT_DIR=out node main.ts
```
