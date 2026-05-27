# Portable LED Display Preview

Diese Preview ist absichtlich statisch gebaut: kein Build-Step, kein npm, keine Installation.

## Auf einem anderen PC verwenden

1. Repository klonen oder als GitHub-Download holen.
2. `ledshow-seefeld/display/index.html` im Browser oeffnen.
3. Optional Produktbilder lokal in `ledshow-seefeld/assets/raw/` legen.

Die Show laeuft auch ohne Produktbilder. Dann werden klare Vektor-Packshots angezeigt, die fuer 192 x 128 px optimiert sind.

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

Die Canvas ist nativ `192 x 128`. Fuer die finale LEDshow kannst du spaeter daraus Frames aufnehmen oder die bestehende `render_commands.sh` nutzen, sobald eine Frame-Sequenz unter `output/frames/frame_%04d.png` liegt.
