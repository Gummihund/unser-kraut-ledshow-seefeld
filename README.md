# unser-kraut-ledshow-seefeld

Fertige LEDshow fuer den Unser Kraut Schaufenster-LED-Monitor in Seefeld.

## Download auf einem zweiten PC

Voraussetzung: Der PC braucht Zugriff auf das private GitHub-Repo `Gummihund/unser-kraut-ledshow-seefeld`.

```powershell
git clone https://github.com/Gummihund/unser-kraut-ledshow-seefeld.git
cd unser-kraut-ledshow-seefeld
```

Die fertige Offline-Datei fuer LEDshow Suite / LED Max / Onbon liegt hier:

```text
ledshow-seefeld\output\mp4\unser-kraut-seefeld-ledshow-192x128.mp4
```

Diese MP4 ist die Datei, die auf den LED-Controller uebertragen werden soll:

- LED-Software starten.
- Controller/Screen per LAN verbinden.
- Die MP4 in der LED-Software als Video/Programm importieren.
- Ausgabe auf 192 x 128 px lassen.
- Per Send/Upload auf den Controller uebertragen.
- In der Software den Modus verwenden, der das Programm im Controller speichert, nicht nur PC-Live-Playback.

Lokale Browser-Vorschau:

```text
ledshow-seefeld\display\index.html
```

Die Browser-Vorschau dient nur zur Kontrolle am PC. Fuer den echten LED-Monitor die MP4 verwenden.
