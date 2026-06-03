# Quellen und Asset-Plan

## Hauptquelle

- Website: https://www.unser-kraut.at
- Shop/Marke: Unser Kraut, Seefeld in Tirol
- GitHub-Zielrepo: https://github.com/Gummihund/unser-kraut-ledshow-seefeld

## Direkte Quellseiten fuer Produktbilder

Diese Seiten enthalten passende Produktbilder fuer die LED-Szenen. Bitte Bilder lokal speichern und mit den Dateinamen aus dem Asset-Plan in `assets/raw/` legen.

- CBD Oele: https://www.unser-kraut.at/cbd-oel-kaufen
- Hanftee: https://www.unser-kraut.at/hanftee
- Hanfblaettertee: https://www.unser-kraut.at/onlineshop/hanfblättertee-austria-bio-garantie-lose
- Hanfblaetter und Fruechte Tee: https://www.unser-kraut.at/onlineshop/hanfblaetter-und-fruechte-tee-austria-bio-qualitaet
- Hanf-Kraeutertee: https://www.unser-kraut.at/onlineshop/hanf-kräutertee-aus-österreich
- CBD Oel 10 Prozent: https://www.unser-kraut.at/onlineshop/cbd-oel-10prozent-vollspektrum-premium-guenstig-kaufen-oesterreich
- Vape Mesh Himbeere: https://www.unser-kraut.at/onlineshop/vapes-mesh-flash-himbeere-led-vape-ohne-nikotin-thc
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

Aktuell eingebundene Einzelbilder:

```text
Datei: assets/raw/cbd-oel-10prozent-premium.jpg
Quelle: https://static.wixstatic.com/media/76f9c9_a123ab60b3cd47fcbeb7d0b2a7693902~mv2.jpg/v1/fit/w_500,h_500,q_90/file.jpg
Produktgruppe: CBD Oele
Verwendung: Szene 2

Datei: assets/raw/hanftee-blaetter-01.jpg
Quelle: https://static.wixstatic.com/media/76f9c9_5f0fe1b983344697bfc34e6141a26f0b~mv2.jpg/v1/fit/w_500,h_500,q_90/file.jpg
Produktgruppe: Hanftee
Verwendung: Szene 3

Datei: assets/raw/hanftee-01.jpg
Quelle: https://static.wixstatic.com/media/76f9c9_c5cc7045b132430ea7826517c2f407a3~mv2.jpg/v1/fit/w_500,h_500,q_90/file.jpg
Produktgruppe: Hanftee
Verwendung: alternative Tee-Packung

Datei: assets/raw/hanftee-kraeuter-01.jpg
Quelle: https://static.wixstatic.com/media/76f9c9_c382df17726e46e09050e99a24de6156~mv2.jpg/v1/fit/w_500,h_500,q_90/file.jpg
Produktgruppe: Hanftee
Verwendung: alternative Tee-Packung

Datei: assets/raw/vape-mesh-himbeere.png
Quelle: https://static.wixstatic.com/media/76f9c9_7269afac671e4ad79f11e4e1b696514d~mv2.png/v1/fit/w_900,h_900,q_95/file.png
Produktgruppe: Vapes
Verwendung: Szene 5
```

## Hinweis zur Website-Erreichbarkeit

In einigen Codex-/Cloud-Runtimes kann direkter HTTP-Zugriff auf unser-kraut.at durch 403 oder Tunnel-Blockaden verhindert sein. In diesem Fall die Bilder manuell im Browser herunterladen und lokal in `assets/raw/` speichern.
