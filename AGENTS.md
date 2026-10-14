# Gemeinsames Display-Projekt

Antworte Christoph auf Deutsch. Lies README.md, PC-UEBERGREIFEND.md und ledshow-seefeld/display-register.md. Dieses Repository betrifft nur die beiden Displays von Unser Kraut. Beide Videos immer ohne Audiospur exportieren.

GitHub: Gummihund/unser-kraut-ledshow-seefeld. Gemeinsame NAS-Kopie: \\nas-christoph\Business\Codex-Projekte\unser-kraut-ledshow-seefeld. Lokal in einem eigenen Git-Clone arbeiten. Vor Änderungen Git- und NAS-Stand prüfen; `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools/Sync-DisplayProject.ps1 -Mode Sync` ausführen. Bei Konflikten beide Fassungen lesen und bewusst zusammenführen. Keine pauschale Spiegelung oder Löschung.

Nach relevanten Änderungen genau die geprüften Projektdateien committen und ins bestehende Repository pushen; anschließend `tools/Sync-DisplayProject.ps1 -Mode Publish` ausführen und beide Ergebnisse getrennt prüfen. GitHub-Sichtbarkeit am 14.10.2026: PUBLIC; nur dafür geeignete Projektinhalte aufnehmen. Neue Dateien müssen zuerst mit git add ausdrücklich ausgewählt werden. Der NAS-Abgleich überträgt nur Git-getrackte Dateien, keine .git-, Codex-Sitzungs-, Anmelde- oder Browserdaten. Fertige Medien in ledshow-seefeld/videos pro Gerät ablegen. Unfertige Renderläufe nicht veröffentlichen.

Auf der NAS-Kopie selbst nur lesen; für Änderungen lokal klonen und den Helfer verwenden. Codex Cloud verwendet das GitHub-Repository; ohne ausdrücklich eingerichtete separate Integration besteht kein NAS-Zugriff. In Cloud-Aufgaben GitHub aktualisieren und NAS-Publish als lokal ausstehenden Schritt melden. Den gemischten übergeordneten Ordner New project 4 niemals vollständig synchronisieren.
