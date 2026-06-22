#!/usr/bin/env bash
# tools/setup.sh — one-shot environment bootstrap for the bm project.
# Run from the repo root:  bash tools/setup.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

GBDK_VERSION="4.5.0"
GBDK_ARCHIVE="gbdk-macos-arm64.tar.gz"
GBDK_URL="https://github.com/gbdk-2020/gbdk-2020/releases/download/${GBDK_VERSION}/${GBDK_ARCHIVE}"

if [[ ! -x "tools/gbdk/bin/lcc" ]]; then
  echo "==> Downloading GBDK-2020 ${GBDK_VERSION}"
  curl -L -o "tools/${GBDK_ARCHIVE}" "${GBDK_URL}"
  tar -xzf "tools/${GBDK_ARCHIVE}" -C tools/
  rm -f "tools/${GBDK_ARCHIVE}"
else
  echo "==> GBDK already present at tools/gbdk/"
fi

if [[ ! -d "gfx/pokecrystal-src/.git" ]]; then
  echo "==> Sparse-cloning pret/pokecrystal for asset source"
  git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/pret/pokecrystal.git gfx/pokecrystal-src
  ( cd gfx/pokecrystal-src && git sparse-checkout set gfx audio && git checkout )
else
  echo "==> pokecrystal-src already present"
fi

echo "==> Done. Toolchain: $(tools/gbdk/bin/lcc -v 2>&1 | head -1 || true)"
