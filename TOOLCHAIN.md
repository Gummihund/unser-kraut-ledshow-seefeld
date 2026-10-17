# Werkzeuge der Display-Produktion

Stand: 16.10.2026. Ziel: dieselbe Herstellungsweise auf einem zweiten Windows-PC ohne Christophs lokale Benutzerpfade.

| Aufgabe | Werkzeug / festgelegte Version |
| --- | --- |
| 3D-Szenen, Materialien, Animation, Rendering | Blender 4.5.14 LTS, Eevee |
| Produktionsskripte | Python, getestet mit 3.12.14; Setup akzeptiert 3.11–3.13 |
| Texte, Produkttexturen, Bildmontage | Pillow 12.3.0 |
| Bilddaten | numpy 2.3.5 |
| Video-Encoding und vollständige Decode-Prüfung | imageio-ffmpeg 0.6.0, Windows-Wheel mit FFmpeg 7.1 |
| Schrift für die vorhandenen Shows | Arial Bold aus Windows (`C:/Windows/Fonts/arialbd.ttf`) |
| Gemeinsame Versionierung und NAS-Übergabe | Git und PowerShell; `Sync-DisplayProject.ps1` |

Python-Pakete stehen in `tools/display-requirements.txt`. Die Blender-Python-API `bpy` gehört zu Blender; sie wird nicht per pip installiert. Für diese Produktion sind ImageGen, ein Cloud-Videoabo oder Browserautomatisierung nicht erforderlich.

## Setup und Prüfung

Im lokalen Clone auf Windows x64:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\Setup-DisplayTools.ps1 -Install
```

Das Setup sucht Python, erstellt `.venv`, installiert die festgelegten Pakete und lädt bei Bedarf das portable Blender-Archiv von `download.blender.org`. Dessen SHA-256 wird vor dem Entpacken geprüft. Das Archiv und Blender bleiben lokal unter `.display-tools`. Kein Admin-Installationsschritt und kein Produktionsrender werden gestartet. Unter `.display-tools/toolchain.json` stehen anschließend die tatsächlich verwendeten lokalen Pfade.

Vorhandene Programme können über absolute Pfade angegeben werden:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\Setup-DisplayTools.ps1 -Install -PythonExe 'C:\Pfad\python.exe' -BlenderExe 'C:\Pfad\blender.exe'
```

Ohne `-Install` prüft das Skript nur; es lädt nichts und legt keine Umgebung an. Für einen zuvor extern angegebenen Blender-Pfad diesen wieder angeben:

```powershell
$displayTools = Get-Content -LiteralPath .display-tools\toolchain.json -Raw | ConvertFrom-Json
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\Setup-DisplayTools.ps1 -PythonExe $displayTools.python -BlenderExe $displayTools.blender
```

Das Setup ist für Windows x64 ausgelegt. Andere Systeme benötigen passende Blender-Binärdateien und eine ausdrücklich geprüfte Schriftzuordnung. Schriften werden nicht aus Windows ins öffentliche Repository kopiert.

## Vorhandene Herbst-Show bearbeiten

Seit 17.10.2026 gibt es zusätzlich eine eigene [30-Sekunden-Seefeld-Kurzfassung](ledshow-seefeld/production/seefeld-sortiment-20261017/README.md). Sie verwendet dieselben Werkzeuge: sieben ausgewählte Blender-Szenen der langen Show und eine neue Vapes-Szene mit dem vorhandenen Originalfoto, jeweils mit großer stehender Schrift. Ihre Skripte, ihr Storyboard und ihre Exporte sind getrennt abgelegt. Die vollständige lange Show und die erste 28-Sekunden-Variante bleiben unverändert. Für die NAS-Geschäftsablage kann der Publisher eine Git-versionierte `publication.json` über `--show-config` lesen; diese legt die korrekten Kurzfassung-Verweise und Prüfdateien fest.

Quellen: `ledshow-seefeld/production/herbst-show-20261016/`. Dort stehen `.blend`, Produktbilder, Originalreferenzen, `storyboard.json` und alle Produktionsskripte. Die `.blend` enthält gepackte Texturen. Die abschließenden großen Texte entstehen mit Pillow beim Videoexport, nicht beim bloßen Öffnen der Blender-Datei.

Für Änderungen immer einen neuen Produktionsordner und neue Dateinamen verwenden. Der bestehende Export schreibt unter festen Namen; deshalb in einer Variante mindestens `NAME` in `finish_video.py`, den `.blend`-Dateinamen in `build_show.py` und die Vorschau-Verweise anpassen, bevor exportiert wird. Skripte für Tafeln und Zeiten sind auf die vollständige 54-Tafel-Show ausgelegt; für eine Kurzfassung müssen auch Szenenzuordnung, Framezahlen und Prüfungen entsprechend angepasst werden.

Texte und Zeiten stehen ursprünglich in `create_storyboard.py`; dieses Skript erzeugt `storyboard.json` neu. Wer nur JSON editiert und danach den Generator startet, verliert diese JSON-Änderung. `compose.py` enthält das Textlayout. `build_show.py` und `engine.py` erzeugen die 3D-Szenen. Bestehende Produktbilder und Referenzen sind bereits vorhanden; keine erneuten Downloads nötig.

Die Abfolge in einem vorbereiteten Produktionsordner ist:

```powershell
# Aus dem Repository-Hauptordner:
$displayTools = Get-Content -LiteralPath .display-tools\toolchain.json -Raw | ConvertFrom-Json
Set-Location ledshow-seefeld\production\herbst-show-20261016
& $displayTools.python create_storyboard.py
& $displayTools.python prepare_assets.py
& $displayTools.blender --background --threads 5 --python build_show.py -- --stills
& $displayTools.blender --background --threads 5 UNSER_KRAUT_HERBST_3D.blend --python render_frames.py
& $displayTools.python finish_video.py
```

Diese Befehle erklären die unveränderte Originalproduktion. Für neue Arbeit zuerst die oben beschriebene Variante anlegen. Bei geänderten Szenen alte Renderframes nicht weiterverwenden: einen frischen `build`-Ordner verwenden. `render_frames.py` überspringt bereits fertige PNGs und würde sonst alte Frames übernehmen. `finish_video.py` benötigt alle Frames und prüft die Videos vor ihrer Übernahme in den Videoordner. Der ZIP-Export bleibt lokal unter `build/`.

## Fertiges Video unabhängig prüfen

Vom Repository-Hauptordner, bei der unveränderten Herbst-Show zusätzlich mit erwarteter Länge:

```powershell
& .venv\Scripts\python.exe tools\Test-DisplayVideo.py ledshow-seefeld\videos\schaufenster-unten-led\UNSER_KRAUT_HERBST_20261016_192x128.mp4 --seconds 208
```

Prüft genau eine H.264-Baseline-Videospur, 192 × 128, 30 fps, yuv420p, keine Audio-/Rotationsmetadaten und vollständiges Decodieren. Mit `--report <Datei.json>` lässt sich der Prüfnachweis einschließlich SHA-256 speichern. Für andere LED-Varianten die passende Dauer angeben. Der Prüfer ist auf das bekannte untere LED ausgelegt; das Spin-Display benötigt zuerst sein eigenes bestätigtes Profil.

Zusätzlich die tatsächlich komprimierte 192 × 128-Datei visuell prüfen: alle Tafeln, Übergänge, Textgröße und vollständige Botschaften. Ein großer PC-Preview ersetzt diese Prüfung und den Test am realen Schaufenster nicht.

## Gemeinsame Ablage

Nur geprüfte Quellen, Produktbilder, `.blend`, Vorschauen, Nachweise und fertige Videos versionieren. `.venv`, `.display-tools`, ZIP-Pakete, Cache und Renderframes bleiben lokal. Eigene GitHub-/NAS-Anmeldungen verwenden. Gemeinsamer Ablauf: [START-HIER.md](START-HIER.md), [PC-UEBERGREIFEND.md](PC-UEBERGREIFEND.md).

`.gitattributes` legt LF-Zeilenenden für Textdateien fest und nimmt Binärmedien ausdrücklich von der Textkonvertierung aus. Dadurch erzeugt ein frischer Windows-Clone dieselben Dateibytes wie die NAS-Projektkopie, unabhängig von `core.autocrlf`. Bestehende CRLF-Textdateien wurden ohne Inhaltsänderung auf LF gebracht. Fertige Videos und Bilder bleiben bytegleich. Bei alten Clones die eigenen Änderungen zuerst sichern; anschließend die betroffenen Textdateien bewusst auf LF angleichen, bevor ein NAS-Initialkonflikt bewertet wird. Unterschiedliche Textinhalte weiterhin manuell zusammenführen.

Blender-Archiv: `https://download.blender.org/release/Blender4.5/blender-4.5.14-windows-x64.zip`. Erwarteter SHA-256 aus der zur ursprünglichen Installation gespeicherten offiziellen Prüfsummenliste: `b9533d2397ac1984db4466fb23a7a4649391cca93f6e84209f9bcc60d071c8b9`.

## Prüfung der Übergabe am 16.10.2026

Eine neue isolierte Python-Umgebung wurde aus den festgelegten Paketen eingerichtet. Das Setup wurde mit externem Blender-Pfad und mit lokalem, per SHA-256 geprüftem portablem Archiv erfolgreich ausgeführt. Die Archiv-Downloadstrecke wurde nicht erneut benötigt. Die Herbst-Datei öffnete mit 54 Szenen und vollständig gepackten Dateitexturen; ein einzelnes Testbild wurde mit Eevee gerendert. Der Videoprüfer bestand eine passende Testdatei und wies Dateien mit Audiospur beziehungsweise falscher Auflösung zurück. Die echte LED-MP4 wurde mit 6.240 Frames vollständig decodiert. Diese Tests ersetzen noch keinen Durchlauf auf Christines PC.

In einem frischen lokalen Clone wurden außerdem beide vorhandenen `finish_video.py --package-only`-Läufe erfolgreich ausgeführt, ohne den bisherigen externen `led-motion-runtime`-Ordner. Die ZIP-Dateien blieben im jeweiligen ignorierten `build`-Ordner. Der NAS-Helfer wurde in getrennten lokalen Testordnern für Erstveröffentlichung der neuen Werkzeugdateien und einer neuen `.blend`, lokale Änderung, Empfang einer gemeinsamen Änderung, beidseitigen Konflikt ohne vorherige Dateikopie und Ablehnung einer Verzeichnisverknüpfung geprüft.
