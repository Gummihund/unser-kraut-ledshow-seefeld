# Vollständige Herbst-Show aus DISPLAY Schaufenster 226

Die vom Benutzer am 16.10.2026 genannte Videodatei wurde vollständig in 54 Tafeln zerlegt. Die neue Fassung übernimmt deren sichtbare Texte, Informationen, Reihenfolge und Szenenzeiten. Gesamtlänge: 208 Sekunden, 6.240 Bilder bei 30 fps. Neue Gestaltung mit Blender 4.5.14 LTS / Eevee.

## Dateien zum Abspielen

Im Ordner `../../videos/schaufenster-unten-led/`:

- `UNSER_KRAUT_HERBST_20261016_192x128.mp4`: Ausgabe für das bekannte P2.5-Schaufenster-LED. 192 × 128, H.264 Constrained Baseline, yuv420p, 30 fps, ohne Ton und Rotation.
- `UNSER_KRAUT_HERBST_20261016_VORSCHAU_768x512.mp4`: größere PC-Vorschau.
- `UNSER_KRAUT_HERBST_20261016_192x128_KOMPATIBEL.avi`: alternative Videodatei für einen Controller, der die MP4 nicht akzeptiert.

`VORSCHAU.html` lokal öffnen. „Original / Neu vergleichen“ spielt die alte und neue Fassung synchron ab. Dort stehen auch alle übernommenen Texte und eine Auswahl für alle 54 Tafeln. Die Referenzdatei ist bereits im bestehenden Videoordner enthalten.

Die technische Exportprüfung steht in `export_verification.json`. Alle drei Videos werden vor ihrer Übernahme in den Videoordner vollständig decodiert. Die tatsächliche Wiedergabe und Helligkeit am LED-Controller sind vor Ort noch zu prüfen. Kein Upload zum LED-Gerät erfolgt durch diesen Dateiexport.

## Inhaltstreue

- Quelle: `DISPLAY Schaufenster 226 - 192 x 128.mp4`, 499.087 Bytes.
- SHA-256 der ausdrücklich genannten NAS-Datei: `b542f489d8a42242aa08bb7905f28e879705fd3ab2a93a91835f1b3fc790bed9`.
- Die bestehende Referenz `DISPLAY-Schaufenster-226-192x128.mp4` wurde als bitgleich geprüft.
- `reference/card_01.png` bis `card_54.png` enthalten je ein Originalbild aus jeder Tafel.
- `storyboard.json` enthält die wörtlich erfassten Texte, Bildzuordnung und alle Bildgrenzen.
- Bewertungen, produktbezogene Werbeaussagen und sonstige Angaben werden als vom Benutzer gelieferter Anzeigeninhalt übernommen. Sie wurden für diesen Gestaltungsauftrag nicht als aktuelle Sachbehauptungen neu recherchiert oder bestätigt.
- Zeilenumbrüche, Schrift, räumliche Anordnung und Gestaltung ändern sich. Es werden keine Textzeilen gekürzt oder durch neue Werbeaussagen ersetzt.

## Bilder und 3D-Gestaltung

Passende Produktfotos wurden am 16.10.2026 neu von `unser-kraut.at` geladen. Quelle und Dateizuordnung stehen in `asset_sources.json`. Originalfotos bleiben als Texturen erhalten. Wo die passende hochauflösende Aufnahme nicht verfügbar war, bleiben die Originalpixel aus der gelieferten Show erhalten, etwa für einzelne ältere Tierprodukt-Verpackungen, den Hund und das Schlussmotiv.

Die Szenen verwenden modellierte Flaschen, gebogene Produktflächen, räumliche Verpackungsformen, schwebende Bildtafeln, Lichtportale, Kamerafahrten und Partikel. Einige zusammengesetzte Produktfotos bleiben bewusst vollständig auf räumlichen Bildtafeln sichtbar. Blattmotive wurden als stilisierte 3D-Geometrie nachgebildet. Die Formen sind künstlerische Rekonstruktionen, keine maßhaltigen Hersteller-CAD-Dateien.

## Bearbeiten und neu rendern

Für einen zweiten PC zuerst [START-HIER.md](../../../START-HIER.md) und [TOOLCHAIN.md](../../../TOOLCHAIN.md) lesen. Das Werkzeug-Setup richtet die festgelegten Versionen lokal ein. Die Bewertung für das Schaufenster am Bahnhof steht in [BAHNHOF-PRUEFUNG.md](BAHNHOF-PRUEFUNG.md). Neue Varianten bekommen eigene Ordner und Namen; die folgenden Befehle beschreiben die vollständige Originalshow.

`UNSER_KRAUT_HERBST_3D.blend` enthält alle 54 animierten Szenen und gepackte Texturen. Für das Öffnen sind keine automatisch auszuführenden Skripte erforderlich. Die großen LED-Texte entstehen beim abschließenden Export, damit sie bei 192 × 128 Pixeln stabil lesbar bleiben.

Mit normalem Python und den kostenlosen Paketen Pillow, numpy und imageio-ffmpeg:

```powershell
python -m pip install Pillow numpy imageio-ffmpeg
python create_storyboard.py
python prepare_assets.py
blender --background --threads 5 --python build_show.py -- --stills
blender --background --threads 5 UNSER_KRAUT_HERBST_3D.blend --python render_frames.py
python finish_video.py
```

Optional können zwei getrennte Prozesse ohne überlappende Bildbereiche rendern:

```powershell
blender --background --threads 3 UNSER_KRAUT_HERBST_3D.blend --python render_frames.py -- --first-card 1 --last-card 34
blender --background --threads 3 UNSER_KRAUT_HERBST_3D.blend --python render_frames.py -- --first-card 35 --last-card 54
```

Bereits vollständig geschriebene PNG-Dateien werden beim Fortsetzen wiederverwendet. Der Ordner `build` und Blender-Sicherungskopien gehören nicht in Git oder den NAS-Abgleich. Bestehende Shows bleiben erhalten.
