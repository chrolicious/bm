# bm — best-men

A bootleg-Pokémon Game Boy Color "game" to ask two friends to be best men. Two ROMs, one per friend.

## Stack

- **Engine:** GBDK-2020 (C), thin custom visual-novel layer
- **Art source:** sprite/tile rips from [pret/pokecrystal](https://github.com/pret/pokecrystal)
- **Music:** TBD — likely hUGEDriver + hand-written .uge, or MML via mmlgb
- **Target:** real Game Boy Color hardware, flashed to a reflashable cart

## Setup

```sh
bash tools/setup.sh   # pulls GBDK-2020 + pokecrystal asset source
make                  # builds build/bm.gbc
```

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
