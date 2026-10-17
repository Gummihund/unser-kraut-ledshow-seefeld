# Bahnhof-Kurzfassung · 28 Sekunden

Erstellt am 17.10.2026 aus der vollständigen Herbst-Show vom 16.10.2026. Eigene Variante für Laufkundschaft am Bahnhof. Die lange Show, ihr Blender-Projekt und ihre Exporte bleiben unverändert erhalten.

## Abspielen

- [LED-MP4: 192 × 128](../../videos/schaufenster-unten-led/UNSER_KRAUT_BAHNHOF_KURZ_20261017_192x128.mp4)
- [PC-Vorschau: 768 × 512](../../videos/schaufenster-unten-led/UNSER_KRAUT_BAHNHOF_KURZ_20261017_VORSCHAU_768x512.mp4)
- [AVI-Alternative](../../videos/schaufenster-unten-led/UNSER_KRAUT_BAHNHOF_KURZ_20261017_192x128_KOMPATIBEL.avi)
- [Vorschauseite](VORSCHAU.html) und [Kontaktbogen der komprimierten LED-Datei](preview/LED_KONTAKTBOGEN.png)

Alle drei Videos: exakt 28 Sekunden, 840 Frames, 30 fps, ohne Audiospur oder Rotation. LED-MP4: H.264 Constrained Baseline, yuv420p. Das bekannte P2.5-LED benötigt die 192 × 128-Datei. Für das Spin-Display fehlen weiterhin Gerätedaten; dafür wurde keine Ausgabe erzeugt.

## Storyboard

| Zeit | Hauptbotschaft | Zusätzliche Einladung | Motiv aus der langen Show |
| --- | --- | --- | --- |
| 0–5 s | UNSER KRAUT / HANF & CBD | KOMM REIN | Tafel 1, Markenmedaillon |
| 5–9 s | KOMM / REIN | WIR BERATEN DICH | Tafel 7, Hanfblatt |
| 9–14 s | BIO HANFTEE | KOMM REIN | Tafel 39, Tee |
| 14–19 s | CBD PFLEGE | KOMM REIN | Tafel 11, Pflegeprodukt |
| 19–24 s | GESCHENKE | KOMM REIN | Tafel 49, CBD-Seife |
| 24–28 s | KOMM / GERNE REIN | UNSER KRAUT | Tafel 45, Markenmedaillon |

Jede Tafel funktioniert ohne die vorherige. Die Einladung ist bereits am Anfang, auf allen Produkttafeln und nochmals groß vor dem Loop-Ende sichtbar. Zwei reine Einladungstafeln stehen insgesamt acht Sekunden. Keine Laufschrift, keine Aufzählungen über mehrere Folgetafeln und keine lange Einleitung. Die Schrift bleibt stehen; nur kurze dunkle Übergänge und ruhige Produktbewegungen.

Die Hauptschrift beträgt je nach Zeile 24,5–46 native Pixel. Der wiederkehrende Hinweis „KOMM REIN“ hat 21 Pixel, der sekundäre Beratungshinweis 17 Pixel. Genaue Größen und geprüfte Begrenzungen: [typography_check.json](typography_check.json). Die tatsächliche Lesbarkeit durch das Schaufensterglas bei Tageslicht muss vor Ort kontrolliert werden.

## Herkunft und vollständige Quellen

Ausgangsprojekt: [UNSER_KRAUT_HERBST_3D.blend](../herbst-show-20261016/UNSER_KRAUT_HERBST_3D.blend), Projektstand `603592164356233482e8d09033601830ff60f853`. `storyboard.json` nennt zusätzlich den SHA-256 der ursprünglichen Blender-Datei und alle verwendeten Quelltafeln/Bildbereiche.

`UNSER_KRAUT_BAHNHOF_28S.blend` enthält die sechs benötigten Szenen mit gepackten Texturen. Unveränderte Produktbilder und Texturen liegen zusätzlich unter `assets/`; Herkunft, ursprüngliche Bild-URLs soweit vorhanden und SHA-256 stehen in `asset_sources.json`. Die Animationen und Produktmotive stammen aus der langen Show. Es wurden keine neuen Produktfotos benötigt.

Die erste Ausgabe nutzt ausschließlich vollständig abgeschlossene Blender-Hintergrundbilder der langen Show. Es waren keine laufenden Blender-/FFmpeg-Renderjobs vorhanden. Die verwendeten PNGs wurden auf vollständige PNG-Signatur und IEND geprüft und bei der Montage vollständig decodiert. `render_provenance.json` dokumentiert die Zuordnung und SHA-256 aller 840 Hintergrundframes. Die Ausgangsbilder enthalten keine eingebrannten Anzeigen-Texte. Große neue Texte entstehen erst in `finish_video.py`.

Um die Produkte sofort sichtbar zu zeigen, wird pro Quelltafel nur der ruhige Bereich von etwa 25–86 Prozent ihrer ursprünglichen Bewegung verwendet. Dieser Bereich wird über die neue Tafelzeit verteilt. `render_frames.py` verwendet dieselbe Bildzuordnung auch beim Neu-Rendern aus der mitgelieferten `.blend`; die ursprüngliche Animation bleibt im Blender-Projekt bearbeitbar. Für Produktkarten wird das Bild bei der Montage nach links versetzt, damit das einzelne Produkt mittig erscheint. Bilder werden dabei nicht gestreckt.

## Bearbeiten und erneut erzeugen

Werkzeuge nach [TOOLCHAIN.md](../../../TOOLCHAIN.md): Blender 4.5.14 LTS/Eevee, Python, Pillow 12.3.0, numpy 2.3.5 und imageio-ffmpeg 0.6.0. Die Schrift ist Arial Bold aus Windows. Im Repository-Hauptordner:

```powershell
$displayTools = Get-Content -LiteralPath .display-tools\toolchain.json -Raw | ConvertFrom-Json
$production = 'ledshow-seefeld/production/bahnhof-kurz-20261017'
& $displayTools.blender --background --threads 5 --python "$production/prepare_project.py"
& $displayTools.blender --background --threads 5 "$production/UNSER_KRAUT_BAHNHOF_28S.blend" --python "$production/render_frames.py"
& $displayTools.python "$production/finish_video.py"
```

`prepare_project.py` ist die Quelle für die sechs Tafeln und erzeugt `storyboard.json` neu. Direktes Editieren der JSON wird beim erneuten Ausführen dieses Generators ersetzt. `finish_video.py` enthält die Textanordnung und Exportnamen. Es schützt bereits vorhandene fertige Ausgaben vor Überschreiben. Für eine neue Bearbeitung zuerst eigenen Produktionsordner und neue Exportnamen wählen und die Verweise in `VORSCHAU.html` und `publication.json` anpassen. Die aktuelle Variante ist auf 28 Sekunden/840 Frames ausgelegt; bei geänderten Zeiten auch die Exportprüfungen anpassen.

Bei geänderten 3D-Szenen einen frischen `build/frames`-Ordner verwenden und ohne `--source-cache` rendern. Der optionale Cache-Schalter in `render_frames.py` dient ausschließlich der Wiederverwendung bereits fertiger, passender Originalbilder; er ist für neue Szeneninhalte ungeeignet. Frames und laufende Renderjobs bleiben lokal. Die mitgelieferte Blender-Datei kann auch ohne Neu-Erzeugung direkt bearbeitet werden; ihre großen Anzeigentexte entstehen weiterhin im abschließenden Python-Export.

## Prüfung und Veröffentlichung

- [export_verification.json](export_verification.json): alle drei Videos vollständig decodiert; jeweils 840 Frames, 28 Sekunden, korrekte Größen, keine Audiospur/Rotation.
- [independent_video_check.json](independent_video_check.json): unabhängige Prüfung der LED-MP4 mit `tools/Test-DisplayVideo.py --seconds 28`.
- Alle sechs Tafeln wurden aus der tatsächlich komprimierten LED-Datei extrahiert und auf Lesbarkeit, Produktdarstellung und Beschnitt geprüft.
- Zusätzlich wurden je drei Zeitpunkte jeder Tafel geprüft: [Bewegungskontrolle](preview/BEWEGUNGSKONTROLLE.png). Der Neu-Render eines Tee-Bildes aus der gepackten sechs-Szenen-Datei war pixelgleich zum verwendeten Original-Hintergrundbild. [QA-Nachweis](qa_validation.json).
- [original_preservation.json](original_preservation.json) bestätigt die unveränderten Dateibytes aller drei langen Video-Exporte und des ursprünglichen Blender-Projekts gegenüber dem Ausgangs-Commit.
- Die Quelldateien und Exporte der langen Herbst-Show bleiben bytegleich.
- Die Wiedergabe und Helligkeit am echten LED-Controller bleiben vor Ort zu prüfen.

Nach gezieltem Staging, Commit und GitHub-Push zusätzlich die gemeinsame NAS-Projektkopie mit `tools/Sync-DisplayProject.ps1 -Mode Publish` aktualisieren. Die verpflichtende Geschäftsablage ist:

```text
\\nas-christoph\Business\christine-geschäft\Videos\Schaufenster-Display\Codex_Fassung_17-10-26_Bahnhof_28s
```

Veröffentlichung des sauberen, committed Projektstands im Repository-Hauptordner:

```powershell
& .venv\Scripts\python.exe ledshow-seefeld/tools/publish_herbst_archive.py --repo . --show-config ledshow-seefeld/production/bahnhof-kurz-20261017/publication.json --destination '\\nas-christoph\Business\christine-geschäft\Videos\Schaufenster-Display\Codex_Fassung_17-10-26_Bahnhof_28s'
```

Der Publisher überträgt nur den Git-versionierten Projektstand, erhält relative Verweise und prüft sämtliche Nutzdateien per SHA-256. `DATEIMANIFEST.json`, `CHECKSUMS.sha256` und `PRUEFPROTOKOLL.json` halten den Stand fest. Erst danach den Haupt-Einstieg `00_START_HIER.html` und bei Bedarf den Codex-Einstieg aus den geprüften Vorlagen unter `ledshow-seefeld/display/` aktualisieren. Frühere Fassungen erhalten. Die Ablage enthält auch die lange Show und ihre Quellen.
