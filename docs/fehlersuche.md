🇬🇧 [English version](fehlersuche.en.md)

# Fehlersuche

## Bereits aufgetretene Fehlerbilder

| Fehlerbild | Ursache | Lösung | Datum |
|---|---|---|---|
| Fallback-Hotspot nimmt das Passwort nicht an | Es wurde der **Prüfbuild mit Dummy-Secrets** geflasht (falsches Hotspot-Passwort, falscher API-Schlüssel) | Nie einen Prüfbuild flashen; mit echten Secrets neu flashen und per API gegenprüfen | 06.10. |
| Zweiter Flashversuch spielt wieder die alte Firmware auf | `esphome upload` kompiliert **nicht** neu, nimmt den letzten Build aus `.esphome/` | Für echte Firmware immer `esphome run …`; auf „Successfully compiled“ achten | 06.10. |
| USB-Port nach Umstecken gesperrt (Linux) | `/dev/ttyUSB0` wird bei jedem Anstecken neu angelegt, eine `setfacl`-Freigabe ist weg | Seit 07.10. udev-Regel am PC (`70-esp-seriell.rules`, CP210x/CH340/Espressif, `uaccess`) – kein `setfacl` mehr nötig | 06./07.10. |
| SMA-Bohrung im Druck nicht nutzbar | Bohrung lag hinter der rechten Platinenauflage | Bohrung unter die Platine verlegt (`sma_z = 8`), 12 mm Lücke | 06.10. |
| Magnettaschen gehen durch den Boden | Taschentiefe 3,2 mm > Bodenstärke 2,0 mm | `boden = 4.0` | 07.10. |
| Platine liegt nicht auf, Pins stoßen auf | Stiftleisten laufen über die ganze Platinenlänge; durchgehende Auflagen | 4 Einzelstützen zwischen den Pinreihen (3,2 mm vom Rand, 12 mm Mitte frei) | 07.10. |

Ein weiterer Flashfehler („No more data to read“ bei 460800 Baud) trat am **Tankmessungs-ESP32** auf, nicht an diesem
Gerät. Falls er hier auftritt: mit `esptool … --baud 115200` die fertige `firmware.factory.bin` schreiben.

## Erwartbare Fehlerbilder bei der Inbetriebnahme (noch nicht aufgetreten)

| Symptom | Mögliche Ursache | Prüfen / Lösung |
|---|---|---|
| Alle Optolink-Werte `unknown`, „Optolink-Status“ bleibt `communication state unknown` | Kopf nicht aufgesetzt / verdreht; LED und FT vertauscht; Beinchen falsch | Lage prüfen: LED links (rote Lampe), FT rechts (grüne Lampe), „OBEN“ oben; Polung per Diodentest |
| Keine Antworten im Log, LED sendet aber | Fototransistor falsch gepolt oder 10 kΩ fehlt | Kollektor (kurzes Bein) an GPIO16 + 10 kΩ nach 3V3, Emitter an GND |
| LED sendet nicht | LED verpolt (Kathode muss an GPIO17), 220 Ω offen | Handykamera (ohne IR-Filter) auf die LED richten – IR-Flackern bei Anfragen sichtbar (allgemeiner Kniff, hier nicht erprobt) |
| Sporadische Aussetzer | Kopf sitzt nicht plan, Fremdlicht | Kopf andrücken, V-Schlüssel prüfen; notfalls Bauteile gegen SFH487 / SFH309FA tauschen |
| Werte plausibel, aber eine Größe falsch | openv-Adresse passt nicht zu dieser Anlage | Adresse anhand [`einmessen.md`](einmessen.md) prüfen, Entität korrigieren oder deaktivieren |
| Außentemperatur im Winter 6000 °C o. ä. | Wert ohne Vorzeichen gelesen | `min_value: -60` muss in der YAML stehen (ist gesetzt) |
| Gerät in HA `unavailable` | WLAN, Strom | „WLAN-Signal“ (am Kessel am 04.10. −41/−42 dBm gemessen), USB-Netzteil prüfen; Fallback-Hotspot `Heizung-Fallback` |

## Wichtig für Automationen

Ohne Verbindung melden die Optolink-Binärsensoren **`unknown`**, nicht `off`. „Brennerstörung = aus“ ist deshalb
kein Beleg für störungsfreien Betrieb – ein dauerhaft `unknown` muss selbst als Problem gelten.

## Abgrenzung: Heizung meldet D1

D1 = **Brennerstörung**. Am 03./04.10. war die Ursache ein leerer Tank. Nach dem Befüllen am 05.10. lief der Brenner
erst nach Entlüften (Filter, Anschluss P an der Danfoss-Pumpe BFP 21 L3) und Reset am Feuerungsautomaten LOA24
(roter Knopf) wieder. Der Knopf „Entsperrung“ an der Regelung ist der **STB**, nicht der Brenner-Reset.
