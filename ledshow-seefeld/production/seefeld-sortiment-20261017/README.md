# Seefeld-Sortiment · 30 Sekunden

Fassung vom 17.10.2026 für das Schaufenster von Unser Kraut in Seefeld in Tirol. Enthält zusätzlich CBD Öle und Vapes. Zwei eigenständige Einladungstafeln, keine zusätzlichen Aufforderungen auf den Produktkarten. Die lange 208-Sekunden-Herbst-Show und die erste 28-Sekunden-Kurzfassung bleiben unverändert erhalten.

## Abspielen

- [LED-MP4: 192 × 128](../../videos/schaufenster-unten-led/UNSER_KRAUT_SEEFELD_SORTIMENT_20261017_192x128.mp4)
- [PC-Vorschau: 768 × 512](../../videos/schaufenster-unten-led/UNSER_KRAUT_SEEFELD_SORTIMENT_20261017_VORSCHAU_768x512.mp4)
- [AVI-Alternative](../../videos/schaufenster-unten-led/UNSER_KRAUT_SEEFELD_SORTIMENT_20261017_192x128_KOMPATIBEL.avi)
- [Vorschauseite](VORSCHAU.html) und [Kontaktbogen des komprimierten LED-Videos](preview/LED_KONTAKTBOGEN.png)

Alle drei Videos: exakt 30 Sekunden, 900 Frames, 30 fps, ohne Audiospur oder Rotation. LED-MP4: H.264 Constrained Baseline, yuv420p. Das bekannte P2.5-LED benötigt die 192 × 128-Datei. Für das Spin-Display fehlen Gerätedaten; dafür wurde keine Ausgabe erzeugt.

## Storyboard

| Zeit | Hauptbotschaft | Fußzeile | Motiv |
| --- | --- | --- | --- |
| 0–4 s | UNSER KRAUT / HANF & CBD | SEEFELD | Markenmedaillon |
| 4–8 s | CBD ÖLE | UNSER KRAUT | Originaletikett auf 3D-Pipettenflasche |
| 8–12 s | BIO HANFTEE | ZUM GENIESSEN | Tee |
| 12–15 s | KOMM / REIN | WIR BERATEN DICH | Hanfblatt |
| 15–19 s | VAPES | 18+ | Original Mesh-Flash-Produktfotografie |
| 19–23 s | CBD PFLEGE | UNSER KRAUT | Pflegeprodukt |
| 23–27 s | GESCHENKE | ZUM MITNEHMEN | CBD-Seife |
| 27–30 s | KOMM / GERNE REIN | UNSER KRAUT | Markenmedaillon |

Jede Tafel funktioniert ohne die vorherige. Fünf Produktgruppen erhalten jeweils vier Sekunden. Die zwei Einladungen stehen zusammen sechs Sekunden, also ein Fünftel der Runde. Keine Laufschrift, keine lange Einleitung; große stehende Hauptschrift. Kurze dunkle Übergänge und ruhige Produktbewegungen. Exakte Schriftgrößen und geprüfte Begrenzungen: [typography_check.json](typography_check.json). Die Gestaltung ist eine redaktionelle Empfehlung für diesen Standort; eine gemessene Steigerung der Ladenbesuche ist damit nicht belegt.

## Standort und Frequenz

[STANDORT-SEEFELD.md](STANDORT-SEEFELD.md) dokumentiert Quellen, Stand und Grenzen der Bahnhofszahlen. Eine historische ÖBB-Angabe von 2018 nennt ungefähr 2.000 Ein- und Ausstiege pro Werktag. Die neueren S6-Zahlen für 2024 betreffen die ganze Strecke Innsbruck–Scharnitz. Keine dieser Zahlen zählt Passanten vor diesem Schaufenster. Die Einladungsdichte wird deshalb am gewünschten freundlichen Auftritt ausgerichtet. Gegenüber der ersten Kurzfassung entfällt die Aufforderung auf jeder Marken-/Produkttafel.

## Quellen und bearbeitbares Projekt

Ausgangspunkt: [vollständige Herbst-Show](../herbst-show-20261016/README.md), Git-Stand `603592164356233482e8d09033601830ff60f853`. Die [erste 28-Sekunden-Variante](../bahnhof-kurz-20261017/README.md) bleibt als eigene Fassung erhalten, Commit `61aea6986c975218d29f4efb50eeb88210d3896e`.

`UNSER_KRAUT_SEEFELD_30S.blend` enthält acht Szenen mit gepackten Texturen. Die sieben übernommenen Szenen stammen aus den ursprünglichen Tafeln 1, 4, 39, 7, 11, 49 und 45. Die Vapes-Szene ist eine unabhängige Kopie der Tee-Umgebung: das Tee-Modell wird durch eine fotografische Ebene mit dem vorhandenen Originalbild `vape-mesh-himbeere.png` ersetzt. Der weiße Hintergrund wird ausschließlich im Blender-Material transparent gesetzt; die Bilddatei bleibt unverändert. `vape_scene.py` dokumentiert den Aufbau. Der Hinweis „18+“ entspricht dem bisherigen Projekt und dem [Vapes-Angebot des Geschäfts](https://www.unser-kraut.at/vapes), geprüft am 17.10.2026. Keine zusätzlichen Wirkungs- oder Legalitätsaussagen eingeblendet.

Alle benötigten Originalbilder, Texturen und das Öletikett liegen zusätzlich unter `assets/`. Herkunft, ursprüngliche Bild-URLs und SHA-256 stehen in `asset_sources.json`. `storyboard.json` nennt die Quelltafeln und den SHA-256 des ursprünglichen Blender-Projekts. `render_provenance.json` dokumentiert die Zuordnung und SHA-256 aller 900 Hintergrundframes.

Für die sieben unveränderten Szenen werden nur bereits vollständig abgeschlossene Originalframes wiederverwendet; PNG-Signatur und IEND werden geprüft, anschließend die Pixel beim Export vollständig decodiert. Die Vapes-Szene wird frisch mit Blender/Eevee gerendert, ihr Original-Cache ist ausdrücklich deaktiviert. Es werden keine laufenden Renderjobs übernommen. Die Auswahl nutzt den ruhigen Bewegungsbereich von etwa 25–86 Prozent der ursprünglichen Szenenzeit und verteilt ihn auf die neuen Standzeiten.

Die großen Anzeigentexte werden erst in `finish_video.py` mit Pillow aufgesetzt; sie sind nicht Teil der Blender-Hintergrundbilder. Die Montage versetzt das Hintergrundbild nach links, um das einzelne Produkt zu zentrieren. Bilder werden nicht gestreckt.

## Bearbeiten und erneut erzeugen

Werkzeuge nach [TOOLCHAIN.md](../../../TOOLCHAIN.md): Blender 4.5.14 LTS/Eevee, Python, Pillow 12.3.0, numpy 2.3.5 und imageio-ffmpeg 0.6.0. Schrift: Arial Bold aus Windows. Im Repository-Hauptordner:

```powershell
$displayTools = Get-Content -LiteralPath .display-tools\toolchain.json -Raw | ConvertFrom-Json
$production = 'ledshow-seefeld/production/seefeld-sortiment-20261017'
& $displayTools.blender --background --threads 5 --python "$production/prepare_project.py"
& $displayTools.blender --background --threads 5 "$production/UNSER_KRAUT_SEEFELD_30S.blend" --python "$production/render_frames.py"
& $displayTools.python "$production/finish_video.py"
```

`prepare_project.py` ist die Quelle für die acht Tafeln und erzeugt `storyboard.json` neu. Direktes Editieren der JSON wird beim erneuten Ausführen des Generators ersetzt. `finish_video.py` enthält Layout und Exportnamen und schützt bestehende fertige Ausgaben vor Überschreiben. Für Änderungen einen neuen Produktionsordner und neue Exportnamen wählen; auch Vorschau und `publication.json` anpassen. Bei geänderten 3D-Szenen frische `build/frames` verwenden und ohne `--source-cache` rendern. Der optionale Original-Cache ist ausschließlich für unveränderte Szenen geeignet; für die Vapes-Szene bleibt er gesperrt.

Die mitgelieferte `.blend` kann direkt bearbeitet werden; `prepare_project.py` nur zum erneuten Ableiten aus den ursprünglichen Quellen starten. Es ersetzt sonst Änderungen an der abgeleiteten Blender-Datei. Frames, Renderjobs und lokale Programme werden nicht veröffentlicht.

## Prüfung und Veröffentlichung

- `export_verification.json`: alle drei Videos vollständig decodiert; 900 Frames, 30 Sekunden, richtige Größen, ohne Audiospur/Rotation.
- `independent_video_check.json`: unabhängige Prüfung der LED-MP4 mit `tools/Test-DisplayVideo.py --seconds 30`.
- Alle acht Tafeln aus der komprimierten LED-Datei sowie je drei Zeitpunkte pro Tafel: `preview/BEWEGUNGSKONTROLLE.png`.
- `qa_validation.json`: acht gepackte Blender-Szenen, frischer Kontroll-Render, Prüfung der Texte und Produktdarstellung.
- `original_preservation.json`: unveränderte lange Video-Exporte, Original-Blender-Projekt und erste 28-Sekunden-Kurzfassung gegenüber den jeweiligen Ausgangs-Commits.
- Wiedergabe, Tageslicht-Lesbarkeit und Helligkeit am echten Schaufenster bleiben vor Ort zu prüfen.

Nach gezieltem Staging, Commit und GitHub-Push die gemeinsame NAS-Projektkopie mit `tools/Sync-DisplayProject.ps1 -Mode Publish` aktualisieren. Pflicht-Geschäftsablage:

```text
\\nas-christoph\Business\christine-geschäft\Videos\Schaufenster-Display\Codex_Fassung_17-10-26_Seefeld_Sortiment_30s
```

```powershell
& .venv\Scripts\python.exe ledshow-seefeld/tools/publish_herbst_archive.py --repo . --show-config ledshow-seefeld/production/seefeld-sortiment-20261017/publication.json --destination '\\nas-christoph\Business\christine-geschäft\Videos\Schaufenster-Display\Codex_Fassung_17-10-26_Seefeld_Sortiment_30s'
```

Der Publisher überträgt nur den sauberen Git-versionierten Projektstand und prüft sämtliche Nutzdateien per SHA-256. `DATEIMANIFEST.json`, `CHECKSUMS.sha256` und `PRUEFPROTOKOLL.json` halten die Herkunft fest. Erst danach die geprüften Einstiegsvorlagen unter `ledshow-seefeld/display/` im Geschäfts-Hauptordner aktualisieren. Alle früheren Fassungen und Originale erhalten.
