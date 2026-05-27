# Quellen und Asset-Plan

## Hauptquelle

- Website: https://www.unser-kraut.at
- Shop/Marke: Unser Kraut, Seefeld in Tirol
- GitHub-Zielrepo: https://github.com/Gummihund/unser-kraut-ledshow-seefeld

## Direkte Quellseiten fuer Produktbilder

Diese Seiten enthalten passende Produktbilder fuer die LED-Szenen. Bitte Bilder lokal speichern und mit den Dateinamen aus dem Asset-Plan in `assets/raw/` legen.

- CBD Oele: https://www.unser-kraut.at/cbd-oel-kaufen
- Hanftee: https://www.unser-kraut.at/hanftee-hanfbluetentee-hanffruechtetee
- Hanfblueten / Aroma-Hanf: https://www.unser-kraut.at/hanfblueten
- Cannabee / Honig: https://www.unser-kraut.at/onlineshop
- Vapes: https://www.unser-kraut.at/vapes
- CBD Koerperpflege: https://www.unser-kraut.at/cbd-koerperpflege
- CBD Gesichtspflege: https://www.unser-kraut.at/cbd-gesichtspflege-antiaging
- Tierprodukte: https://www.unser-kraut.at/cbd-oel-hund-katze-pferd

## Zu sammelnde Produktbilder

Die Produktbilder sollen frisch von unser-kraut.at geladen und in `assets/raw/` abgelegt werden. Fuer die finale LEDshow-Datei sind grosse, kontrastreiche Einzelprodukte besser als komplette Shop-Screenshots.

Prioritaet A:

- CBD Oel Flasche
- Hanftee / Tee-Packung
- Hanfblueten-Produkt
- Cannabee / Honig mit Hanfbluetenol aus Tirol
- Vape-Produkte

Prioritaet B:

- Naturkosmetik / Creme / Pflege
- Hanfsamen
- Snacks / Protein
- Tierprodukte
- Geschenkartikel / Bad / Buch / Mitbringsel

## Benennungsstandard fuer Assets

```text
assets/raw/brand-logo.png
assets/raw/cbd-oel-01.png
assets/raw/hanftee-01.png
assets/raw/hanfblueten-01.png
assets/raw/cannabee-honig-01.png
assets/raw/vape-01.png
assets/raw/pflege-creme-01.png
assets/raw/hanfsamen-01.png
assets/raw/snack-protein-01.png
assets/raw/tierprodukt-01.png
```

Prepared Assets:

```text
assets/prepared/cbd-oel-cutout.png
assets/prepared/hanftee-cutout.png
assets/prepared/honig-cutout.png
assets/prepared/vape-cutout.png
```

## Recherche- und Designnotizen

Best Practices fuer kleine LED-Schaufensterdisplays:

- Inhalte muessen bei nativer Pixelzahl funktionieren, nicht erst am grossen Monitor.
- Wenige, grosse Elemente schlagen viele kleine Details.
- Dunkle Hintergruende sparen optisches Rauschen und lassen Produkte heller wirken.
- Bewegung muss langsam und klar sein.
- Hoher Kontrast ist wichtiger als fotorealistische Detailtreue.
- Produkt + 1 kurzer Begriff ist besser als Produkt + Beschreibung.

## Quellen in der finalen Produktion dokumentieren

Beim Download echter Produktbilder bitte je Bild erfassen:

```text
Datei: assets/raw/cbd-oel-01.png
Quelle: https://www.unser-kraut.at/...
Produktgruppe: CBD Oele
Verwendung: Szene 2
```

## Hinweis zur Website-Erreichbarkeit

In einigen Codex-/Cloud-Runtimes kann direkter HTTP-Zugriff auf unser-kraut.at durch 403 oder Tunnel-Blockaden verhindert sein. In diesem Fall die Bilder manuell im Browser herunterladen und lokal in `assets/raw/` speichern.
