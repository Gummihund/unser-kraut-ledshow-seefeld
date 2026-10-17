# Gemeinsam mit eigenem Codex am Display arbeiten

Stand: 17.10.2026. Einstieg für Christine und weitere berechtigte Mitarbeitende auf Windows.

## Video ansehen

Gewohnter Geschäftsordner mit der veröffentlichten Bahnhof-Kurzfassung und der langen Herbst-Show:

```text
\\nas-christoph\Business\christine-geschäft\Videos\Schaufenster-Display
```

Dort `00_START_HIER.html` für die Show öffnen. Der zusätzliche Einstieg `01_MIT_CODEX_BEARBEITEN.html` erklärt die gemeinsame Bearbeitung. Die Show-Ablage ist ein veröffentlichter Versionsstand; die jeweils aktuellen Arbeitsanweisungen und Quellen stehen im folgenden gemeinsamen Arbeitsprojekt und auf GitHub. Details: [NAS-ABLAGE.md](ledshow-seefeld/NAS-ABLAGE.md).

Gemeinsamer NAS-Projektordner:

```text
\\nas-christoph\Business\Codex-Projekte\unser-kraut-ledshow-seefeld
```

Letzte fertige Show für das LED unten im Schaufenster:

```text
ledshow-seefeld\videos\schaufenster-unten-led\UNSER_KRAUT_BAHNHOF_KURZ_20261017_192x128.mp4
```

Die Datei mit `VORSCHAU_768x512` im Namen ist die größere PC-Vorschau. Vorschau und Tafelauswahl: [Bahnhof-Kurzfassung](ledshow-seefeld/production/bahnhof-kurz-20261017/VORSCHAU.html). Die [lange Herbst-Show mit Original-/Neu-Vergleich](ledshow-seefeld/production/herbst-show-20261016/VORSCHAU.html) bleibt unverändert erhalten. Falls der Browser NAS-Videos blockiert, die Vorschau im lokalen Git-Clone öffnen.

## Einmal auf dem eigenen Windows-PC einrichten

1. NAS-Ordner im Explorer öffnen. Zum Veröffentlichen muss der eigene NAS-Benutzer auch schreiben dürfen. Bestehende Berechtigungen verwenden; keine fremden Anmeldedaten kopieren.
2. Git für Windows und Codex mit dem eigenen Konto verwenden. Für direkte Pushes ist eigener GitHub-Schreibzugriff auf `Gummihund/unser-kraut-ledshow-seefeld` nötig. NAS-Zugriff allein vergibt diesen Zugriff nicht. Christines GitHub-Schreibzugriff ist nach Aussage vom 16.10.2026 vermutlich vorhanden, aber noch nicht bestätigt.
3. Einen eigenen lokalen Clone erstellen, beispielsweise in PowerShell:

```powershell
$displayClone = Join-Path $env:USERPROFILE 'Documents\Codex\unser-kraut-ledshow-seefeld'
New-Item -ItemType Directory -Path (Split-Path -Parent $displayClone) -Force | Out-Null
git clone https://github.com/Gummihund/unser-kraut-ledshow-seefeld.git $displayClone
Set-Location -LiteralPath $displayClone
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\Sync-DisplayProject.ps1 -Mode Sync
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\Setup-DisplayTools.ps1 -Install
```

Das Setup richtet eine lokale Python-Umgebung und bei Bedarf Blender 4.5.14 LTS ein. Falls Python fehlt, Python 3.12 x64 von [python.org](https://www.python.org/downloads/windows/) installieren und wiederholen. Die technische Anleitung steht in [TOOLCHAIN.md](TOOLCHAIN.md).

4. Diesen lokalen Clone als Projektordner in Codex öffnen. Dann den folgenden Startauftrag hineinkopieren. Es ist keine Kopie von Christophs Chat oder Codex-Profil nötig. Codex liest die gemeinsamen Projektanweisungen aus `AGENTS.md`; der dokumentierte Stand reist mit den Dateien. Siehe [offizielle OpenAI-Dokumentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Startauftrag für den eigenen Codex

> Arbeite im bestehenden Display-Repository von Unser Kraut. Lies AGENTS.md, README.md, START-HIER.md, PC-UEBERGREIFEND.md, TOOLCHAIN.md und ledshow-seefeld/display-register.md. Lies für die letzte Herbst-Show auch deren README.md und BAHNHOF-PRUEFUNG.md. Prüfe Git- und NAS-Stand, führe vor Änderungen tools/Sync-DisplayProject.ps1 -Mode Sync aus und gleiche fremde Änderungen bewusst ab. Prüfe mit tools/Setup-DisplayTools.ps1 die Werkzeuge; richte fehlende Werkzeuge mit -Install ein. Verwende Blender 4.5.14 LTS/Eevee, Pillow, numpy und FFmpeg über imageio-ffmpeg wie im Projekt. Erhalte Originaldateien. Lege neue Varianten mit eigenem Produktionsordner und eindeutigem Videonamen an. Fertige LED-Videos brauchen 192 × 128 Pixel, 30 fps, H.264 Baseline, yuv420p, keine Rotation und keine Audiospur. Prüfe sie mit tools/Test-DisplayVideo.py und visuell in nativer Auflösung. Aktualisiere Register und Anleitungen, stage nur die geprüften Projektdateien ausdrücklich, committe und pushe sie und veröffentliche anschließend mit tools/Sync-DisplayProject.ps1 -Mode Publish. Prüfe GitHub und NAS getrennt. Keine laufenden Renderjobs, Zugangsdaten oder Codex-Profile veröffentlichen. Für das Spin-Display zuerst die fehlenden Gerätedaten erfragen. Mein konkreter Änderungswunsch lautet: …

## Vor jeder Bearbeitung und nach Fertigstellung

Vorher `git status --short --branch` und `git fetch origin` prüfen. Bei sauberem Arbeitsbaum `git pull --ff-only`, danach `Sync-DisplayProject.ps1 -Mode Sync`. Lokale Änderungen vorher sichern, nicht automatisch verwerfen. Bei einer belegten NAS-Sperre den anderen Abgleich fertiglaufen lassen; keine Sperre löschen oder fremde Prozesse beenden.

Neue fertige Dateien gehören in `ledshow-seefeld/videos/schaufenster-unten-led/` beziehungsweise `ledshow-seefeld/videos/spin-display-1-stock/`. Das Register und der jeweilige Produktionsordner enthalten die Zuordnung und den Prüfnachweis. Renderframes und unvollständige Videos bleiben lokal in `build/`.

Nach Prüfung genau die gewünschten Dateien mit `git add <Pfad>` auswählen, `git diff --cached` prüfen, committen, `git push` ausführen und anschließend:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\Sync-DisplayProject.ps1 -Mode Publish
```

Der Helfer überträgt ausschließlich Git-getrackte, zugelassene Projektdateien mit Hashprüfung. Eine neue Datei muss daher vor dem Publish ausdrücklich gestagt worden sein. GitHub-Push und NAS-Publish sind zwei getrennte Schritte. Scheitert ein Push an fehlenden Rechten, den Stand lokal erhalten und Christoph den fehlenden Repository-Zugriff nennen. Nicht mit fremden Zugangsdaten umgehen.

Jede fertige Display-Show muss zusätzlich in Christines gewohntem Geschäfts-Videoordner erscheinen. Das gehört dauerhaft zum Auftrag und braucht keine erneute Bestätigung. Nach [NAS-ABLAGE.md](ledshow-seefeld/NAS-ABLAGE.md) als eigenen eindeutig datierten Versionsordner mit vollständigen Quellen, Assets, Storyboard, Dokumentation, Git-Commit, Dateimanifest und SHA-256-Prüfprotokoll veröffentlichen, alle Zieldateien prüfen und danach `00_START_HIER.html` aktualisieren. Die vorhandenen Show-Versionen erhalten. Der dortige Publisher ist momentan auf die vollständige Herbst-Show verlinkt; bei neuen Videonamen muss Codex dessen Startseiten-Verweise passend zur neuen Show vorbereiten und prüfen. Die zentrale NAS-Projektkopie wird davon unabhängig mit `Sync-DisplayProject.ps1` aktualisiert.

## Was bereits geprüft ist und was noch fehlt

Die Werkzeuge und die letzte LED-Datei wurden am vorbereitenden PC geprüft. Ein vollständiger Einrichtungs-, Bearbeitungs- und Veröffentlichungstest auf Christines PC ist noch offen. Auch ihr tatsächlicher NAS-Schreibzugriff und GitHub-Push müssen dort einmal bestätigt werden. Es wurde kein Zugriff auf ihren PC eingerichtet und keine Anmeldung übertragen.

NAS-Dateien teilen den dokumentierten Projektstand. Eigene Konten, verfügbare Codex-Modelle, Plugins und persönliche Chatverläufe bleiben kontobezogen. Für die vorhandene Blender-Produktion sind keine kostenpflichtigen Bild-/Video-Plugins nötig; sie arbeitet mit den mitgelieferten Quellen und lokalen Werkzeugen.
