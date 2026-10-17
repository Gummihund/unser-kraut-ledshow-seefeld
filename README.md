# unser-kraut-ledshow-seefeld

Aktuell für Laufkundschaft am Bahnhof: [28-Sekunden-LED-MP4](ledshow-seefeld/videos/schaufenster-unten-led/UNSER_KRAUT_BAHNHOF_KURZ_20261017_192x128.mp4), erstellt am 17.10.2026 aus der langen Herbst-Show. Sechs eigenständige Tafeln, große stehende Schrift, Einladung auf jeder Tafel und zwei große Einladungstafeln. [Vorschau](ledshow-seefeld/production/bahnhof-kurz-20261017/VORSCHAU.html) · [Storyboard, Blender und Quellen](ledshow-seefeld/production/bahnhof-kurz-20261017/README.md).

Geschäftsablage der Kurzfassung mit vollständigem Projektstand: `Codex_Fassung_17-10-26_Bahnhof_28s` im bekannten NAS-Videoordner. `00_START_HIER.html` führt zur aktuellen Fassung. Die lange Herbst-Show und alle bisherigen Fassungen bleiben erhalten.

[Start für Christine / eigenen Codex](START-HIER.md) · [Gleiche Herstellungswerkzeuge einrichten](TOOLCHAIN.md) · [Bewertung der letzten Show für Bahnhof-Laufkundschaft](ledshow-seefeld/production/herbst-show-20261016/BAHNHOF-PRUEFUNG.md)

Der vollständige Stand für die gemeinsame Bearbeitung wird im Geschäfts-Videoordner zusätzlich unter `Codex_Fassung_16-10-26_Gemeinsame_Bearbeitung` abgelegt. Der Haupt-Einstieg `00_START_HIER.html` und `01_MIT_CODEX_BEARBEITEN.html` führen dorthin. Die bisherige Herbst-Fassung bleibt erhalten.

Geschäftsablage mit Videos und vollständiger Projektdokumentation: `\\nas-christoph\Business\christine-geschäft\Videos\Schaufenster-Display\00_START_HIER.html`. Die Fassung vom 16.10.2026 liegt dort unter `Codex_Fassung_16-10-26_Herbst_3D`, mit Startseite, Git-Commit, Dateimanifest und SHA-256-Prüfprotokoll. [Ablageplan und Veröffentlichungsablauf](ledshow-seefeld/NAS-ABLAGE.md).

Vollständige Herbst-Show vom 16.10.2026: [LED-MP4, 192 × 128, 3:28 Minuten](ledshow-seefeld/videos/schaufenster-unten-led/UNSER_KRAUT_HERBST_20261016_192x128.mp4). Übernimmt alle 54 Tafeln der gelieferten Show mit neuen Blender-Szenen. [Original-/Neu-Vergleich, Blender-Projekt und Anleitung](ledshow-seefeld/production/herbst-show-20261016/README.md).

Neue Blender-3D-Show vom 14.10.2026: [LED-MP4, 192 × 128, 30 Sekunden](ledshow-seefeld/videos/schaufenster-unten-led/UNSER_KRAUT_3D_BLENDER_20261014_192x128.mp4). [Blender-Projekt, Vorschau und Anleitung](ledshow-seefeld/production/blender-show-20261014/README.md).

Fertige LEDshow fuer den Unser Kraut Schaufenster-LED-Monitor in Seefeld.

Seit 14.10.2026 gemeinsame NAS-Kopie fuer Geschaeft und Daheim:
`\\nas-christoph\Business\Codex-Projekte\unser-kraut-ledshow-seefeld`.
Sie enthaelt Projektdateien und fertige Videos. [PC-uebergreifender Ablauf, NAS-Abgleich und Codex Cloud](PC-UEBERGREIFEND.md).

## Download auf einem zweiten PC

Voraussetzung: Git und Zugriff auf `Gummihund/unser-kraut-ledshow-seefeld` (am 14.10.2026 als oeffentlich geprueft). Zum Pushen ist die eigene GitHub-Anmeldung erforderlich.

```powershell
git clone https://github.com/Gummihund/unser-kraut-ledshow-seefeld.git
cd unser-kraut-ledshow-seefeld
```

Die aktuelle Kurzfassung fuer LEDshow Suite / LED Max / Onbon liegt hier:

```text
ledshow-seefeld\videos\schaufenster-unten-led\UNSER_KRAUT_BAHNHOF_KURZ_20261017_192x128.mp4
```

Ein aktuelles Register fuer die beiden Display-Standorte und die versionierten Videos liegt hier:

```text
ledshow-seefeld\display-register.md
```

Neue fertige Videos werden pro Geraet getrennt abgelegt:

```text
ledshow-seefeld\videos\schaufenster-unten-led\
ledshow-seefeld\videos\spin-display-1-stock\
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
