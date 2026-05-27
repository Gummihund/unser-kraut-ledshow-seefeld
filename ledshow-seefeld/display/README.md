# Portable LED Display Preview

Diese Preview ist absichtlich statisch gebaut: kein Build-Step, kein npm, keine Installation.

## Auf einem anderen PC verwenden

1. Repository klonen oder als GitHub-Download holen.
2. `ledshow-seefeld/display/index.html` im Browser oeffnen.
3. Optional Produktbilder lokal in `ledshow-seefeld/assets/raw/` legen.

Die Browser-Preview laeuft auch ohne Produktbilder. Dann werden klare Vektor-Packshots angezeigt, die fuer 192 x 128 px optimiert sind.

Wichtig fuer den echten LED-Screen: Lade nicht die HTML-Datei auf den Controller. Fuer den Screen wird eine offline gerenderte Video-Datei aus `output/mp4/` oder `output/avi/` verwendet. Diese Datei enthaelt alle Pixel bereits fest im Video und braucht danach kein Internet.

## Lokale Produktbilder

Wenn echte Produktbilder vorhanden sind, nutzt die Preview automatisch diese Dateinamen:

```text
ledshow-seefeld/assets/raw/cbd-oel-01.png
ledshow-seefeld/assets/raw/hanftee-01.png
ledshow-seefeld/assets/raw/cannabee-honig-01.png
ledshow-seefeld/assets/raw/vape-01.png
ledshow-seefeld/assets/raw/hanfsamen-01.png
ledshow-seefeld/assets/raw/pflege-creme-01.png
ledshow-seefeld/assets/raw/tierprodukt-01.png
```

`assets/raw/`, `assets/prepared/` und `output/` sind per `.gitignore` geschuetzt, damit keine ZIPs, Videos oder Produktbilder versehentlich per PR ins Repo kommen.

## Export-Idee

Die Canvas ist nativ `192 x 128`. Fuer die finale LEDshow gibt es einen Offline-Renderer:

```powershell
python ledshow-seefeld/tools/render_offline_ledshow.py
```

Der Renderer erstellt:

```text
ledshow-seefeld/output/frames/frame_0000.png
ledshow-seefeld/output/preview/unser-kraut-seefeld-ledshow-preview.gif
ledshow-seefeld/output/mp4/unser-kraut-seefeld-ledshow-192x128.mp4
```

Falls lokal kein MP4-Encoder verfuegbar ist, entstehen trotzdem die PNG-Frames und die GIF-Preview. Mit `ffmpeg` kann daraus anschliessend die LEDshow-MP4/AVI aus `render_commands.sh` erzeugt werden.
