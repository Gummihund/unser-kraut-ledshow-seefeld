#!/usr/bin/env bash
set -euo pipefail

# Render-/Exportbefehle fuer Unser Kraut Seefeld LEDshow-Projekt.
# Voraussetzung: Eine fertig gerenderte Frame-Sequenz liegt in output/frames/frame_%04d.png.
# Ziel: LEDshow Suite / Onbon / LED Max, natives P2.5 Display 192 x 128 px.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMES_DIR="$PROJECT_ROOT/output/frames"
MP4_DIR="$PROJECT_ROOT/output/mp4"
AVI_DIR="$PROJECT_ROOT/output/avi"
PREVIEW_DIR="$PROJECT_ROOT/output/preview"

mkdir -p "$MP4_DIR" "$AVI_DIR" "$PREVIEW_DIR"

# 1) Primaerdatei fuer LEDshow Suite: MP4 H.264 Baseline, yuv420p, ohne Audio.
ffmpeg -y \
  -framerate 30 \
  -i "$FRAMES_DIR/frame_%04d.png" \
  -an \
  -vf "scale=192:128:flags=lanczos,setsar=1,unsharp=3:3:0.35:3:3:0.10,format=yuv420p" \
  -r 30 \
  -c:v libx264 \
  -profile:v baseline \
  -level 3.0 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -crf 15 \
  "$MP4_DIR/unser-kraut-seefeld-ledshow-192x128.mp4"

# 2) Kompatibilitaetsversion fuer aeltere LEDshow-/Onbon-Setups: AVI MPEG4.
ffmpeg -y \
  -framerate 30 \
  -i "$FRAMES_DIR/frame_%04d.png" \
  -an \
  -vf "scale=192:128:flags=lanczos,setsar=1,unsharp=3:3:0.35:3:3:0.10,format=yuv420p" \
  -r 30 \
  -c:v mpeg4 \
  -q:v 2 \
  -pix_fmt yuv420p \
  "$AVI_DIR/unser-kraut-seefeld-ledshow-192x128-compat.avi"

# 3) PC-Vorschau ohne Weichzeichnung: nearest-neighbor auf 1920 x 1280.
# Diese Datei sieht am PC pixelig aus, zeigt aber die echte LED-Pixelwirkung fairer als Windows-Medienwiedergabe.
ffmpeg -y \
  -i "$MP4_DIR/unser-kraut-seefeld-ledshow-192x128.mp4" \
  -vf "scale=1920:1280:flags=neighbor" \
  -c:v libx264 \
  -pix_fmt yuv420p \
  -crf 18 \
  "$PREVIEW_DIR/pc-preview-no-blur-unser-kraut-seefeld.mp4"

# 4) Kontaktbogen fuer schnelle Motivkontrolle.
ffmpeg -y \
  -i "$MP4_DIR/unser-kraut-seefeld-ledshow-192x128.mp4" \
  -vf "select='not(mod(n,90))',scale=384:256:flags=neighbor,tile=4x3" \
  -frames:v 1 \
  "$PREVIEW_DIR/contact-sheet-led-pixels.png"

printf '\nExport fertig:\n'
printf 'MP4: %s\n' "$MP4_DIR/unser-kraut-seefeld-ledshow-192x128.mp4"
printf 'AVI: %s\n' "$AVI_DIR/unser-kraut-seefeld-ledshow-192x128-compat.avi"
printf 'Preview: %s\n' "$PREVIEW_DIR/pc-preview-no-blur-unser-kraut-seefeld.mp4"
