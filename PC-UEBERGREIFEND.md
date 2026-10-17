# Display-Projekt im Geschäft, daheim und in Codex Cloud

Stand: 14.10.2026. NAS DS925+ über bestehendes Tailscale/SMB erreichbar. Heim-PC bei Einrichtung offline; Einrichtung dort noch nicht live geprüft.

Ergänzung 16.10.2026: [START-HIER.md](START-HIER.md) enthält den Einstieg für Christine mit eigenem Codex und einen vollständigen Startauftrag. [TOOLCHAIN.md](TOOLCHAIN.md) und `tools/Setup-DisplayTools.ps1` richten dieselbe lokale Blender-/Python-/FFmpeg-Produktion ein. Werkzeuge am vorbereitenden PC geprüft; tatsächliche Einrichtung, NAS-Schreibzugriff und GitHub-Push auf Christines Windows-PC noch offen. NAS-Zugriff allein überträgt keine GitHub-Berechtigung oder Codex-Plugins. Gemeinsame Quellen und Anweisungen werden geteilt, persönliche Chatverläufe und Anmeldungen bleiben beim jeweiligen Konto.

## Gemeinsame Dateien

NAS: `\\nas-christoph\Business\Codex-Projekte\unser-kraut-ledshow-seefeld`

Alternativer Tailscale-Name: `\\nas-christoph.taild3d9c.ts.net\Business\Codex-Projekte\unser-kraut-ledshow-seefeld`

Daheim liegt die Business-Freigabe nach bestehender NAS-Dokumentation auch unter `D:\SynologyDrive\Business`. Der Projektordner kann dort nach dem Drive-Abgleich unter `Codex-Projekte\unser-kraut-ledshow-seefeld` erscheinen. Tatsächlichen Download und Offline-Verfügbarkeit prüfen; direkte NAS-Dateien sind nur bei erreichbarer NAS verfügbar.

Die gemeinsame Kopie enthält das ausgewählte Display-Repository mit Register, Produktbildern, Quellcode und fertigen Videos. Die übrigen Dokumente im gemischten ursprünglichen Arbeitsordner gehören nicht dazu. NAS-Handbuch für Netzwerkdetails: `\\nas-christoph\Business\Codex-Projekte\NAS-Handbuch`.

## Lokal arbeiten

Eigenen Git-Clone auf jedem PC verwenden. So geraten Git-Sperrdateien und lokale Programme nicht in einen Zwei-Wege-Dateisync. Beispielsweise:

```powershell
git clone https://github.com/Gummihund/unser-kraut-ledshow-seefeld.git D:\Codex\unser-kraut-ledshow-seefeld
cd D:\Codex\unser-kraut-ledshow-seefeld
git pull --ff-only
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\Sync-DisplayProject.ps1 -Mode Sync
```

Dann diesen lokalen Ordner in Codex als Projekt hinzufügen. Vor einem Pull den Arbeitsbaum prüfen und eigene Änderungen sichern. Nach Änderungen ausdrücklich die gewünschten Dateien stagen, Diff prüfen, committen und pushen; dann NAS veröffentlichen:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\Sync-DisplayProject.ps1 -Mode Publish
```

Der Helfer verwendet die von Git ausgewählte Dateiliste und SHA-256. Er hält fremde Änderungen fest, stoppt vor Konflikten und überträgt keine Löschungen. Keine Hintergrundautomatik eingerichtet. Neue Dateien erst gezielt stagen. Wenn die NAS-Kopie sich geändert hat und die lokale Datei bereits identisch ist, kann der Helfer die Vergleichsbasis gefahrlos übernehmen. Bei verschiedenen Fassungen zuerst manuell zusammenführen, nicht die Zustandsdatei löschen, um eine Prüfung zu umgehen.

## Codex Cloud und bestehende Chats

Codex Cloud kann dieses bestehende GitHub-Repository in einer Cloud-Umgebung bearbeiten. Sichtbarkeit am 14.10.2026 live geprüft: PUBLIC. Im Web oder in der Desktop-App `Work in > Cloud` wählen, Umgebung anlegen, dieses Repository auswählen und Einrichtung prüfen/veröffentlichen. Der Cloud-Stand erreicht die PCs über Git-Pull. Danach lokal den NAS-Publish ausführen. Cloud-Umgebung wurde mit dieser Dateieinrichtung nicht angelegt.

Die private Tailscale-Adresse der NAS ist aus einer Cloud-Umgebung nicht automatisch erreichbar. Eine zusätzliche Verbindung wäre eine eigene Einrichtung. Für dieses Projekt ist GitHub als Übergabe ausreichend.

Zum Weiterarbeiten im selben bestehenden lokalen Chat auf einem anderen Gerät den Geschäfts-PC als Codex-Host koppeln: `Einstellungen > Verbindungen > Diesen PC steuern` am Geschäfts-PC; am anderen Gerät `Andere Geräte steuern`. Die Funktion muss dort verfügbar sein. Geschäfts-PC und App müssen erreichbar bleiben. Projektdateien auf NAS synchronisieren keine lokalen Chatverläufe.

Offizielle Dokumentation:

- [Codex Cloud](https://learn.chatgpt.com/docs/cloud)
- [Geräte verbinden, SSH und Chat-Übergabe](https://learn.chatgpt.com/docs/remote-connections)

## Zusätzliche Geschäftsablage seit 16.10.2026

Aktuell seit 17.10.2026: Die 30-Sekunden-Seefeld-Kurzfassung samt Quellen und vollständigem Projektstand liegt unter `Codex_Fassung_17-10-26_Seefeld_Sortiment_30s`. `00_START_HIER.html` im Hauptordner führt dorthin. Alle Fassungen vom 16.10.2026 und die lange Show bleiben erhalten. [Bearbeiten und Veröffentlichen der Kurzfassung](ledshow-seefeld/production/seefeld-sortiment-20261017/README.md).

Fertige Videos und der gesamte zugehörige versionierte Projektstand werden zusätzlich im gewohnten Geschäftsordner abgelegt:

`\\nas-christoph\Business\christine-geschäft\Videos\Schaufenster-Display`

Dort `00_START_HIER.html` öffnen. Die vollständige Herbst-Show vom 16.10.2026 liegt unter `Codex_Fassung_16-10-26_Herbst_3D`. `START.html` im Versionsordner verlinkt LED-MP4, PC-Vorschau, AVI-Alternative, Blender-Datei, Original/Neu-Vergleich und die gesamte Projektdokumentation. Dateimanifest und SHA-256-Prüfprotokoll halten den zugehörigen Git-Commit und die geprüften Dateien fest. Ältere Ordner bleiben erhalten.

Diese zusätzliche, eigenständige Veröffentlichung ersetzt den obigen Git-/NAS-Arbeitsablauf nicht. [Ablageplan und erneute Veröffentlichung](ledshow-seefeld/NAS-ABLAGE.md). Keine automatische Hintergrundsynchronisierung.

## Prüfgrenzen

Heim-PC offline: Projektöffnung, GitHub-Anmeldung, Drive-Download und tatsächlicher Videoabruf dort noch offen. Spin-Display-Gerätedaten fehlen weiterhin laut Display-Register. Keine neue Netzfreigabe, Tailscale-Regel, Portweiterleitung, Benutzerberechtigung oder Backupaufgabe für diese Einrichtung ändern.
