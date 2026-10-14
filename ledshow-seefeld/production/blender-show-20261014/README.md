# Unser Kraut: Blender-3D-Show fürs Schaufenster

Erstellt am 14. Oktober 2026 mit Blender 4.5.14 LTS und Eevee. Fünf räumliche Szenen mit modellierten Produkten, Originaletiketten, Kamerafahrten, Partikeln und Lichtportalen. Die Show dauert 30 Sekunden und enthält keinen Ton.

## Abspielen

Die LED-Datei liegt unter `../../videos/schaufenster-unten-led/UNSER_KRAUT_3D_BLENDER_20261014_192x128.mp4`.

- Native Ausgabe: 192 × 128 Pixel, 3:2, 30 fps, H.264 Constrained Baseline, yuv420p, ohne Ton und Rotation.
- PC-Vorschau: `UNSER_KRAUT_3D_BLENDER_20261014_VORSCHAU_768x512.mp4` im selben Videoordner.
- Alternative für Controller: `UNSER_KRAUT_3D_BLENDER_20261014_192x128_KOMPATIBEL.avi`.
- Komprimierte Videodateien vollständig decodiert und mit 900 Bildern pro Datei geprüft. Ergebnisse in `export_verification.json`.
- Wiedergabe und Helligkeit am echten Controller vor Ort noch prüfen. Für LEDshow Suite / LED Max / Onbon die LED-MP4 importieren, Fläche auf 192 × 128 belassen, Schleife aktivieren und Programm auf dem Controller speichern.

## Szenen

1. CBD-Flasche vor einem grünen Lichttunnel, 0–6 Sekunden.
2. Drei räumlich gestaffelte Flaschen desselben 10%-Produkts, 6–12 Sekunden.
3. Hanftee-Verpackung mit botanischem Portal und geometrischen Blättern, 12–18 Sekunden.
4. Seefeld-Schokolade als schwebender Fächer vor einem goldenen Tunnel, 18–24 Sekunden.
5. Dreidimensionales Markenmedaillon und „Komm rein“, 24–30 Sekunden.

Die Verpackungsformen wurden künstlerisch anhand der Produktfotos rekonstruiert. Es sind keine maßhaltigen Hersteller-CAD-Modelle. Die sichtbaren Vorderseiten nutzen Originalfotos bzw. Originaletiketten. Nicht sichtbare Verpackungsrückseiten sind neutral gestaltet. Die botanischen Blätter sind stilisierte 3D-Geometrie. Keine Preise, Öffnungszeiten oder gesundheitlichen Wirkversprechen hinzugefügt.

## Blender-Projekt bearbeiten

`UNSER_KRAUT_3D.blend` enthält fünf separate, vollständig animierte Szenen und die gepackten Texturen. In Blender oben zwischen den Szenen wechseln. Die Bildbereiche sind 1–180, 181–360, 361–540, 541–720 und 721–900. Die Projektdatei enthält keine benötigten automatisch auszuführenden Skripte.

Die LED-Texte entstehen im abschließenden Export in `finish_video.py`, damit die Buchstaben in der sehr geringen nativen Auflösung stabil lesbar bleiben. Die räumlichen Produktbilder, Beleuchtung, Schatten, Reflexionen und Bewegungen entstehen in Blender.

Neu aufbauen:

```powershell
blender --background --threads 5 --python build_show.py -- --stills
blender --background --threads 5 UNSER_KRAUT_3D.blend --python render_frames.py
python -m pip install Pillow numpy imageio-ffmpeg
python finish_video.py
```

Blender: https://www.blender.org/download/

Verwendete portable Windows-Version: Blender 4.5.14 LTS. Download über den Blender-Spiegel der RWTH Aachen, SHA-256 gegen dessen Blender-Prüfsummendatei geprüft. Das Programm und unfertige Einzelbilder gehören nicht in Git oder den NAS-Abgleich.

Windows-Archiv SHA-256: `b9533d2397ac1984db4466fb23a7a4649391cca93f6e84209f9bcc60d071c8b9`.

## Bildquellen

- CBD-Produktfotografie: https://www.unser-kraut.at/onlineshop/cbd-oel-10-prozent-vollspektrum
- Originaldatei CBD: https://static.wixstatic.com/media/76f9c9_15d861af82164750b724675aceda9f05~mv2.jpg
- Hanftee: https://static.wixstatic.com/media/76f9c9_5f0fe1b983344697bfc34e6141a26f0b~mv2.jpg
- Schokolade: https://static.wixstatic.com/media/76f9c9_7cdb14b916364e9fb018d1fdc9875310~mv2.jpg
- Unverändertes Markenlogo: https://static.wixstatic.com/media/4dd46a_d017a8282c02449eac177054c708af92~mv2.png

Die Produktbilder wurden aus der vorangegangenen lokalen Show übernommen. Der Ausschnitt `cbd-label.png` stammt aus dem Originalfoto und dient als Textur auf der gebogenen Etikettfläche.
