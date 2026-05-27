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

## Portable Browser-Preview

Eine sofort nutzbare Preview liegt unter:

```text
ledshow-seefeld/display/index.html
```

Diese Preview braucht keine Installation und keinen Build-Schritt. Sie kann auf einem anderen PC direkt im Browser geoeffnet werden und laeuft nativ als 192 x 128 Canvas mit pixeliger Kontrollskalierung. Wenn Produktbilder unter `assets/raw/` liegen, werden sie automatisch eingebunden; ohne Bilder nutzt die Show klare Vektor-Packshots.

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
