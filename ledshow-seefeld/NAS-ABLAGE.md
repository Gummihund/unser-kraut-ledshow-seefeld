# Projekt- und Videoablage auf der NAS

Stand: 16.10.2026. Zwei Ablagen haben unterschiedliche Aufgaben.

Dauerhafte Nutzerpräferenz: Die zusätzliche Geschäftsablage ist für jede fertige Display-Show Teil des Auftrags und benötigt keine erneute Bestätigung. Nach vollständiger Prüfung jeweils einen datierten Versionsordner samt Quellen, Assets, Storyboard, vollständiger Dokumentation, Herkunft/Git-Commit, Dateimanifest und SHA-256-Prüfprotokoll erstellen und `00_START_HIER.html` aktualisieren. Frühere Fassungen und Originale erhalten.

## Arbeitsprojekt

`\\nas-christoph\Business\Codex-Projekte\unser-kraut-ledshow-seefeld`

Gemeinsame Projektkopie für die PCs. Änderungen entstehen im lokalen Git-Clone, werden geprüft, gezielt committed und gepusht und mit `tools/Sync-DisplayProject.ps1 -Mode Publish` veröffentlicht. Ablauf und Konfliktregeln: [PC-UEBERGREIFEND.md](../PC-UEBERGREIFEND.md). GitHub bleibt das versionierte Projektarchiv.

## Geschäft: Videos und vollständiger Projektstand

`\\nas-christoph\Business\christine-geschäft\Videos\Schaufenster-Display`

`01_MIT_CODEX_BEARBEITEN.html` ist der zusätzliche Einstieg für Christine mit eigenem Codex. Die versionierte Vorlage liegt unter `ledshow-seefeld/display/01_MIT_CODEX_BEARBEITEN.html`; bei Änderungen die geprüfte Datei zusätzlich unter diesem Namen in den Video-Hauptordner kopieren und den SHA-256 vergleichen. Der Einstieg verweist auf [START-HIER.md](../START-HIER.md), [TOOLCHAIN.md](../TOOLCHAIN.md) und die aktuelle gemeinsame Arbeitsprojektkopie. Die nachfolgende Herbst-Ablage bleibt ein festgehaltener Versionsstand und wird dafür nicht überschrieben.

Der geprüfte Projektstand für die gemeinsame Bearbeitung einschließlich derselben fertigen Herbst-Videos und der neuen Werkzeuge/Anleitungen wird separat unter `Codex_Fassung_16-10-26_Gemeinsame_Bearbeitung` veröffentlicht. Dort enthält `START.html` auch direkte Verweise auf den Codex-Einstieg, die Werkzeug-Einrichtung und die Bahnhof-Bewertung. `00_START_HIER.html` im Hauptordner führt auf diesen vollständigen Stand und erhält einen Link zur bisherigen Herbst-Fassung. Die versionierte Vorlage für diesen Haupt-Einstieg liegt unter `ledshow-seefeld/display/00_START_HIER.html`.

`00_START_HIER.html` ist der Einstieg im gewohnten Videoordner. Die neue vollständige Herbst-Show liegt einschließlich aller versionierten Projektdateien unter:

`Codex_Fassung_16-10-26_Herbst_3D`

Dort `START.html` öffnen. Die gewohnte Struktur des gesamten Repositorys bleibt erhalten, damit Vorschauen, Bildverweise und der Original/Neu-Vergleich funktionieren. Die drei aktuellen Videos liegen unter `ledshow-seefeld/videos/schaufenster-unten-led/`:

- `UNSER_KRAUT_HERBST_20261016_192x128.mp4`: für das LED-Schaufenster, 192 × 128, 30 fps, ohne Ton.
- `UNSER_KRAUT_HERBST_20261016_VORSCHAU_768x512.mp4`: größere PC-Vorschau.
- `UNSER_KRAUT_HERBST_20261016_192x128_KOMPATIBEL.avi`: Alternative für den Controller, ohne Ton.

Unter `ledshow-seefeld/production/herbst-show-20261016/` liegen Blender-Projekt, Storyboard, Produktbilder, Quellen, Vergleichsansicht, Kontaktbögen und technische Exportprüfung. Die übrigen versionierten Projektdateien einschließlich älterer Shows sind ebenfalls enthalten. Root-README, Display-Register und PC-Dokumentation gehören zum gleichen Projektstand.

`DATEIMANIFEST.json` dokumentiert den vollständigen Git-Commit, jeden Dateipfad, die Größe und SHA-256. `CHECKSUMS.sha256` enthält die Prüfsummen auch als Textliste. `PRUEFPROTOKOLL.json` entsteht erst nach erfolgreichem Vergleich sämtlicher Nutzdateien auf der NAS. Diese drei Verwaltungsdateien stehen nicht in ihrem eigenen Inhaltsmanifest. Die Gerätewiedergabe muss weiterhin vor Ort getestet werden.

Der Originalordner `09-10-26 Herbst` sowie `Codex_Fassung_14-10-26` und `Codex_Fassung_14-10-26_final` bleiben erhalten. Die neue Ablage ersetzt oder bereinigt diese Ordner nicht.

## Veröffentlichung dieses Projektstands wiederholen

Der Publisher `tools/publish_herbst_archive.py` im Ordner `ledshow-seefeld` verwendet nur die in Git ausgewählten Dateien des sauberen, committed Projektstands. Er benötigt Python 3 und ausschließlich die Standardbibliothek. Im Repository-Root ausführen:

```powershell
python ledshow-seefeld/tools/publish_herbst_archive.py --repo . --destination '\\nas-christoph\Business\christine-geschäft\Videos\Schaufenster-Display\Codex_Fassung_16-10-26_Herbst_3D'
```

Bei einer Wiederholung muss derselbe Commit ausgecheckt sein wie im vorhandenen `DATEIMANIFEST.json`. Abweichende vorhandene Dateien stoppen den Vorgang; es wird nichts pauschal überschrieben oder gelöscht. Keine `.git`-Daten, laufenden Renderjobs, lokalen Programme oder übrigen Dokumente aus dem übergeordneten Mischordner werden übernommen.

Für neue Shows einen neuen eindeutig datierten Versionsordner verwenden, die Startseite auf die neue Show abstimmen und nach vollständiger Prüfsummenprüfung den Einstieg im Video-Hauptordner aktualisieren. Dies ist ein manueller Veröffentlichungsablauf, keine automatische Synchronisierung.
