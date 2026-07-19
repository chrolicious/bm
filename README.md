# bm — best-men

A bootleg-Pokémon Game Boy Color "game" to ask two friends to be best men. Two ROMs, one per friend.

## Stack

- **Engine:** GBDK-2020 (C), thin custom visual-novel layer
- **Art source:** sprite/tile rips from [pret/pokecrystal](https://github.com/pret/pokecrystal)
- **Music:** TBD — likely hUGEDriver + hand-written .uge, or MML via mmlgb
- **Target:** real Game Boy Color hardware, flashed to a reflashable cart

## Setup

**macOS / Linux (or Windows with Git Bash):**
```sh
bash tools/setup.sh   # auto-detects OS, pulls the right GBDK-2020 + pokecrystal asset source
make                  # builds build/bm.gbc
```

**Windows (PowerShell, no Git Bash):**
```powershell
powershell -ExecutionPolicy Bypass -File tools\setup.ps1   # pulls gbdk-win64 + assets
tools\gbdk\bin\make.exe                                     # or GNU make if on PATH
```

Notes for the Windows machine:
- `setup.sh` and the `Makefile` (`mkdir -p` / `rm -rf`) assume a Unix-ish shell.
  Easiest path is **Git Bash** (ships with Git for Windows) — then the macOS/Linux
  commands above work verbatim.
- The `Makefile` auto-detects `lcc.exe` on Windows; override with `make LCC=...` if needed.
- Neither Windows script is tested on real hardware yet — if a step fails, both just
  (1) unzip GBDK to `tools/gbdk/` and (2) sparse-clone pokecrystal `gfx`+`audio`.
- Toolchain, asset clone, and `build/` are all gitignored — re-run setup after any clone.

## Layout

```
src/        # C source (engine + scenes)
gfx/        # PNG assets ready for png2asset
  raw/      #   curated sprites/tiles staged from pokecrystal-src
  pokecrystal-src/  # vendored, gitignored — full pret/pokecrystal gfx + audio
music/      # .uge / .c music data
scripts/    # markdown scripts per friend, source of truth for dialogue
tools/      # GBDK-2020, scripts
build/      # gitignored ROM output
```
