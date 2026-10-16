# Eignung der Herbst-Show für Laufkundschaft am Bahnhof

Prüfung: 16.10.2026. Gegenstand: `UNSER_KRAUT_HERBST_20261016_192x128.mp4`. Die bestehende Show wurde nicht verändert. Dies ist eine gestalterische Einschätzung, keine gemessene Werbewirkung und keine inhaltliche Bestätigung der gelieferten Produkt-/Werbeaussagen.

## Ergebnis

Als ausführlicher Überblick über das Sortiment brauchbar, als kurze Einladung für vorbeigehende Menschen nur teilweise passend. Die große Inhaltsmenge stammt aus dem Auftrag, alle 54 Tafeln des Originalvideos vollständig zu übernehmen. Diese Inhaltstreue wurde erfüllt; eine solche Vollfassung verfolgt ein anderes Ziel als ein kurzer Bahnhof-Loop.

Beibehalten würde ich die dunklen Hintergründe, die hellen Schriftfarben, die wiederkehrende Gestaltung und die Zuordnung echter Produktbilder. Vereinfachen würde ich die Textmenge, die kleinteiligen Motive und die Abhängigkeit zwischen aufeinanderfolgenden Tafeln. Die LED-Auflösung begrenzt die Detailwirkung auch bei hochwertigen Blender-Quellen.

## Konkrete Beobachtungen

| Beispiel | Beobachtung und Folge |
| --- | --- |
| Tafel 1, 0–4 s | „UNSER KRAUT / DEIN FACHGESCHÄFT“ nennt den Namen, aber noch keine konkrete Produktkategorie. Das erste CBD-Produkt erscheint bei 12 s. Wer nur die ersten Sekunden sieht, weiß unter Umständen noch nicht, was er hier bekommt. |
| Tafel 6, 19–24,5 s | „HOL DIR / DEIN PASSENDES“ und sechs Flaschen. Die Produktkategorie wird aus den vorhergehenden Tafeln verständlicher; allein bleibt der Satz unvollständig. Sechs kleine Flaschen sind auf 192 × 128 schwer zu unterscheiden. |
| Tafel 7, 24,5–28,5 s | Gute Richtung: Beratungseinladung. Vier Textzeilen im geteilten Bild ergeben allerdings nur etwa 10,75 native Schriftpixel. |
| Tafel 9, 33,5–37,5 s | Fünf Zeilen über das Pflege-Sortiment. Für einen flüchtigen Blick zu viel zu lesen, obwohl der Text innerhalb des Bildes bleibt. |
| Tafeln 11, 28, 33, 39 | Neben dem Produkt liegen Schriftgrößen rechnerisch etwa bei 10–12,25 Pixeln; auf dem kleinen LED fehlt Reserve für Abstand, Glas und Spiegelungen. |
| Tafeln 38/39, 142,5–148 s | Frage „HAST DU AUSZEIT NÖTIG?“ und erst danach die Tee-Antwort. Beide zusammen sinnvoll, beim Einstieg mitten im Loop schwächer. Die Tee-Tafel steht nur 2,5 s. |
| Tafeln 40/41, 148–154,5 s | „WENN DIR DAS LEBEN SAURES GIBT…“ bekommt erst auf der Folgetafel seine Fortsetzung. Eine einzelne Tafel soll für Passanten bereits eine vollständige Aussage enthalten. |
| Tafeln 45/46, 166–171 s | „KOMM GERNE REIN“ und „WIR NEHMEN UNS ZEIT“ sind passende Botschaften, erscheinen aber erst nach 2:46 und jeweils nur 2,5 s. |
| Tafeln 47–53 | Geschenkideen und regionale Produkte sind konkrete Anlässe zum Reinkommen. Ein einzelnes Motiv mit kurzer Benennung wäre für Passanten stärker als der ganze Block. Tafel 52 zeigt das Produkt 8,5 s ohne zusätzlichen Text. |

Die vorhandene `typography_check.json` nennt für 53 Texttafeln Schriftgrößen von 10 bis 25,5 nativen Pixeln; 21 davon liegen für die zuerst erfasste Zeile unter 14 Pixeln. Das ist keine universelle Lesbarkeitsschwelle, sondern zeigt die Unterschiede innerhalb dieser Show. Ein bestandener Clipping-Test bedeutet nur, dass Text ins Bild passt.

## Vorschlag für einen separaten Test-Loop

Eine zusätzliche, etwa 25–30 Sekunden lange Kurzfassung mit fünf eigenständigen Tafeln, ungefähr fünf bis sechs Sekunden pro Tafel:

1. Name + klare Kategorie, beispielsweise „UNSER KRAUT / HANF & CBD“.
2. Ein großes Tee-Produkt + „BIO HANFTEE“.
3. Ein großes Pflege-Produkt + „HAUTPFLEGE MIT CBD“.
4. Eine konkrete Geschenkidee + kurze Benennung.
5. „KOMM GERNE REIN / WIR BERATEN DICH“.

Die Formulierungen sind Vorschläge, keine hier beauftragte oder produzierte neue Anzeige. Kategorien und Sortiment vor Produktion bestätigen. Auf jeder Produkttafel möglichst auch eine kleine, gut lesbare Namenskennung. Keine Pflicht, bis zur letzten Tafel zu warten: die Einladung kann auf Produkttafeln mitlaufen, soweit sie lesbar bleibt. Weniger Partikel und Nebenobjekte, ein Hauptmotiv, möglichst zwei kurze Textzeilen. Das am realen Fenster bei Tageslicht aus dem üblichen Laufweg testen.

## Prüfbasis und Grenzen

Alle 54 aus der komprimierten LED-Datei gewonnenen Tafeln in `preview/LED_EXPORT_1.jpg` bis `LED_EXPORT_3.jpg` visuell geprüft; Texte, Dauer und Abhängigkeiten mit `storyboard.json` abgeglichen. Die vorhandenen größeren Vorschauen dienen nur als zusätzliche Gestaltungsreferenz.

Aktuelle unabhängige technische Prüfung: [bahnhof-video-check.json](bahnhof-video-check.json). Vollständiger Decode von 6.240 Frames/208 s, H.264 Constrained Baseline, yuv420p, 192 × 128, 30 fps, keine Audiospur, keine gemeldete Rotation. SHA-256: `741108d6ad327a50fce6fcf6b7bcd1d69edbbd7dd3e4cf49d4ef306b8815c660`.

Betrachtungsabstand, direkte Sonne, Glasreflexionen und Reaktionen von Passanten wurden hier nicht vor Ort gemessen. Die Bewegungswirkung über den gesamten Ablauf wurde nicht in Echtzeit vor dem echten Gerät beurteilt. Daraus folgt keine belastbare Besucher- oder Umsatzprognose.
