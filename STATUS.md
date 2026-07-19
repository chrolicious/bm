# bm — project status / handoff

Last updated: 2026-06-25 (end of a macOS working session, before swapping to Windows PC).

## What this is

A bootleg-Pokémon Game Boy Color "game" to ask two friends to be best men.
**Two separate ROMs**, one per friend. Built in GBDK-2020 (C) as a thin
visual-novel engine. Art ripped/palette-swapped from pret/pokecrystal.

- Friend 1 = **Tobi** (WoW handle Ozora) — script finalized.
- Friend 2 = **BramS** (WoW handle Freak0r) — script not started.
- Deadline: ~2026-06-30 (about a week out as of the last session).

## Repo layout

```
src/        C source (engine + scenes). Currently just main.c.
scripts/    Markdown scripts, source of truth for dialogue.
            friend1.md = Tobi (DONE). friend2.md = BramS (TODO).
gfx/        pokecrystal-src/ is gitignored; re-fetch via setup.
music/      empty — 4 tracks TODO (see below).
tools/      setup.sh (mac/linux/git-bash), setup.ps1 (windows), gbdk/ (gitignored).
build/      gitignored ROM output.
```

## Done

- [x] GBDK-2020 4.5.0 toolchain + build chain (`make` → build/bm.gbc, 32K, MBC5, CGB-only)
- [x] pret/pokecrystal assets pulled (sprites, tilesets, fonts, audio source)
- [x] Cross-platform setup (mac/linux/windows) — see README
- [x] **Tobi script finalized** — all 7 scenes, polished (scripts/friend1.md)
- [x] Engine pass 1: Scene 1 (Classroom) dialogue plays via GBDK built-in font,
      A-to-advance. **Not yet visually verified** (no emulator installed last session).

## Tobi script — 7 scenes (chronological)

1. Classroom (cold open, age 16) — Tobi mocks front-row dress-shirt Michel. "spasti."
2. Schoolyard — Friets/BramT/Tobi hype WoW; ends on "...what is deadmines" + "20 years... and counting."
3. BramT's living room — Michel plays Porcupine Tree "Trains" on guitar. Quiet beat. **Music centerpiece.**
4. La Cubanita, Spain (age 18) — ANOTHER ROUND? loop, 4 rounds, options degrade to gibberish; dad yells "TOBIAS. MAUEL. WAS. ZUM. FICK."; ends on Tobi's *sigh*.
5. Blackwing Lair raid — anti-puzzle: "DON'T WALK LEFT OR RIGHT", player does, 40-man wipe, real demotion. Guild "Bound by Blood", vent chat in WoW handles.
6. Aachen club stairs (CLIMAX) — follow Tobi out, camera pan up stairs, silent telling ("..."), hug, user's narrator coda, idiots snapped down with "Halt's Maul du Spasti", closes on "...Spastis."
7. Garden BBQ (the ask) — BramS says "Yo Mich"; "this whole game was a question"; storyteller narrator block (20+ years, deeper/stronger); "will you be my best man?" > Yes / Heil Yes; BEST MAN BADGE; "spasti. of course."; title card "BESTMEN / Ozora".

Full dialogue + intentions + asset notes live in scripts/friend1.md.

## Music (TODO — 4 GBC chiptune tracks)

- **Trains main motif** (Porcupine Tree) — Scene 3 centerpiece, reprises in Scene 7 under the ask + title card.
- **WoW Classic Tavern theme** — Scene 2 BGM.
- **La Cucaracha** — Scene 4 BGM (cheesy tourist-bar).
- **Aachen Beat** — Scene 6, generic club four-on-the-floor; muffles when the door closes, plays through everything.

Approach: hUGEDriver runtime + .uge authoring, or MML via mmlgb. Not decided.

## Next actions (in priority order)

1. Install an emulator (SameBoy recommended: https://github.com/LIJI32/SameBoy/releases)
   and verify Scene 1 renders: `open -a SameBoy build/bm.gbc` (mac) / open the .gbc in SameBoy (win).
2. Extend engine: bottom text-box on window layer, tilemap backgrounds, NPC sprites,
   choice prompts (Sc4 loop, Sc5 pull, Sc7 Yes/Heil Yes), scene transitions. Then wire all 7 Tobi scenes.
3. Write BramS (Friend 2) script — same 7-scene shape where memories overlap.
4. Compose the 4 music tracks.
5. Art: palette swaps + custom Tobi/BramS overworld sprites + cartridge covers.
6. Build both ROMs, flash to real carts, test on hardware. Keep a buffer day.

## Gotchas

- Windows: use Git Bash so `make` (mkdir -p / rm -rf) works. See README.
- git auth: SSH key missing on the mac; used `gh auth setup-git` + HTTPS remote.
  On Windows, `gh auth login` then HTTPS remote should just work.
- RTK proxy wraps shell commands on the mac; not relevant on Windows.
