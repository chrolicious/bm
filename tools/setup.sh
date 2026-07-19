#!/usr/bin/env bash
# tools/setup.sh — one-shot environment bootstrap for the bm project.
# Run from the repo root:  bash tools/setup.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

GBDK_VERSION="4.5.0"

# Pick the right GBDK build for this OS/arch. Works under macOS, Linux,
# and Git Bash / MSYS on Windows. (Windows users without Git Bash can
# run tools/setup.ps1 in PowerShell instead.)
case "$(uname -s)" in
  Darwin)
    if [[ "$(uname -m)" == "arm64" ]]; then GBDK_ARCHIVE="gbdk-macos-arm64.tar.gz"; else GBDK_ARCHIVE="gbdk-macos.tar.gz"; fi ;;
  Linux)
    if [[ "$(uname -m)" == "aarch64" ]]; then GBDK_ARCHIVE="gbdk-linux-arm64.tar.gz"; else GBDK_ARCHIVE="gbdk-linux64.tar.gz"; fi ;;
  MINGW*|MSYS*|CYGWIN*)
    GBDK_ARCHIVE="gbdk-win64.zip" ;;
  *)
    echo "Unknown OS $(uname -s); edit GBDK_ARCHIVE by hand." >&2; exit 1 ;;
esac
GBDK_URL="https://github.com/gbdk-2020/gbdk-2020/releases/download/${GBDK_VERSION}/${GBDK_ARCHIVE}"

if [[ ! -x "tools/gbdk/bin/lcc" && ! -x "tools/gbdk/bin/lcc.exe" ]]; then
  echo "==> Downloading GBDK-2020 ${GBDK_VERSION} (${GBDK_ARCHIVE})"
  curl -L -o "tools/${GBDK_ARCHIVE}" "${GBDK_URL}"
  case "${GBDK_ARCHIVE}" in
    *.zip)    ( cd tools && unzip -q "${GBDK_ARCHIVE}" ) ;;
    *.tar.gz) tar -xzf "tools/${GBDK_ARCHIVE}" -C tools/ ;;
  esac
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

LCC_BIN="tools/gbdk/bin/lcc"; [[ -x "${LCC_BIN}.exe" ]] && LCC_BIN="${LCC_BIN}.exe"
echo "==> Done. Toolchain: $("${LCC_BIN}" -v 2>&1 | head -1 || true)"
