# Unser Kraut Seefeld - LEDshow / Onbon Projekt

Professionelles Schaufenster-LED-Projekt fuer ein kleines P2.5-Display bei Unser Kraut in Seefeld in Tirol.

## Zielgeraet

- Displaytyp: P2.5 LED
- Physische Groesse: 48 x 32 cm
- Native Aufloesung: 192 x 128 px
- Seitenverhaeltnis: 3:2
- Helligkeit: ca. 800 nit
- Playback: LEDshow Suite / LED Max / Onbon
- Einsatz: Schaufenster, Laufkundschaft vor dem Geschaeft

## Gestaltungsprinzip

Dieses Display ist sehr klein in Pixeln. Gute Inhalte muessen daher wie ein LED-Schaufenster-Spot gestaltet werden, nicht wie ein Flyer.

Wichtig:

- Native Ausgabe immer 192 x 128 px.
- Keine Skalierung auf andere Seitenverhaeltnisse.
- Maximal 1 bis 3 Worte pro Szene.
- Produkt gross, Text gross, Hintergrund dunkel.
- Starke Hell-Dunkel-Kontraste.
- Wenig Details, keine kleinen Preise, keine langen Saetze.
- Keine Produktlisten oder Webshop-Kacheln.
- Szenen kurz halten, ca. 2.5 bis 4 Sekunden.
- Loop so bauen, dass er ohne harten Bruch wieder von vorne starten kann.

## Empfohlener Look

- Dunkelgruener bis schwarzer Hintergrund.
- Produkt in der rechten oder mittleren Bildhaelfte gross freigestellt.
- Kurze Begriffe links: CBD OELE, HANF TEE, VAPES, HONIG, PFLEGE.
- Leichte Bewegung: Produkt-Slide, sanfter Zoom, Lichtkante, Glow.
- Lokaler Bezug: SEEFELD, TIROL, JETZT REIN.

## Produktfokus

Priorisierte Produktgruppen fuer Laufkundschaft:

1. CBD Oele
2. Hanftee / Hanfblueten
3. Cannabee / Honig mit Hanfbluetenol aus Tirol
4. Vapes
5. Naturkosmetik / Cremes / Pflege
6. Hanfsamen / Snacks / Protein
7. Tierprodukte, wenn das Bild stark und klar ist
8. Geschenk-/Mitbringsel-Szene

## Ausgabeformate

Primaerformat fuer LEDshow Suite:

- MP4
- 192 x 128 px
- 30 fps
- H.264 Baseline
- yuv420p
- ohne Audio

Kompatibilitaetsformat:

- AVI
- MPEG4 Video
- 192 x 128 px
- 30 fps
- yuv420p
- ohne Audio

PC-Kontrollvorschau:

- 1920 x 1280 px
- nearest-neighbor Skalierung
- wirkt pixelig, aber zeigt am PC die echte LED-Pixelwirkung ohne Weichzeichnung

## Download und Uebertragung auf den LED-Monitor

Auf einem zweiten PC zuerst das private GitHub-Repo klonen:

```powershell
git clone https://github.com/Gummihund/unser-kraut-ledshow-seefeld.git
cd unser-kraut-ledshow-seefeld
```

Die fertige Datei fuer den LED-Monitor liegt danach hier:

```text
ledshow-seefeld\output\mp4\unser-kraut-seefeld-ledshow-192x128.mp4
```

Empfohlener Ablauf:

1. LEDshow Suite / LED Max / Onbon starten.
2. LED-Controller per LAN-Kabel mit dem PC verbinden.
3. Screen/Controller in der LED-Software erkennen lassen.
4. MP4-Datei importieren:

```text
ledshow-seefeld\output\mp4\unser-kraut-seefeld-ledshow-192x128.mp4
```

5. Aufloesung bei 192 x 128 px belassen.
6. Programm/Video an den Controller senden.
7. Den Speichern-/Upload-Modus der Software verwenden, damit die Show im Controller bleibt und nicht nur als PC-Live-Playback laeuft.

Wenn MP4 auf einem aelteren Controller nicht akzeptiert wird, aus derselben Show eine AVI/MPEG4-Kompatibilitaetsversion rendern und diese uebertragen.

## Portable Browser-Preview

Eine sofort nutzbare Preview liegt unter:

```text
ledshow-seefeld/display/index.html
```

Diese Preview braucht keine Installation und keinen Build-Schritt. Sie kann auf einem anderen PC direkt im Browser geoeffnet werden und laeuft nativ als 192 x 128 Canvas mit pixeliger Kontrollskalierung. Wenn Produktbilder unter `assets/raw/` liegen, werden sie automatisch eingebunden; ohne Bilder nutzt die Show klare Vektor-Packshots.

Fuer den echten LED-Screen bitte nicht die HTML-Datei hochladen. Der Screen braucht eine fertige Offline-Datei:

```text
ledshow-seefeld/output/mp4/unser-kraut-seefeld-ledshow-192x128.mp4
```

Diese MP4 enthaelt alle Bilder und Texte fest eingebettet und funktioniert nach dem Upload ohne Internet.

Offline-Render:

```powershell
python ledshow-seefeld/tools/render_offline_ledshow.py
```

## Ordnerstruktur

```text
ledshow-seefeld/
  README.md
  storyboard.md
  sources.md
  render_commands.sh
  display/
    index.html
    styles.css
    ledshow.js
  tools/
    render_offline_ledshow.py
  assets/
    raw/          # manuell geladene Produktbilder von unser-kraut.at
    prepared/     # freigestellte oder zugeschnittene Bilder
  output/
    mp4/
    avi/
    preview/
```

## Naechster Produktionsschritt

Frische Produktbilder direkt von unser-kraut.at laden und in `assets/raw/` ablegen. Danach aus diesen Bildern eine echte 192 x 128 LEDshow-Datei rendern.
