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
| Optolink-Status bleibt `communication suspended`, keine Antwort | **IR-LED verpolt** eingelötet | Diodentest: rot an Anode muss ~1,1 V zeigen; umgelötet | 10.10. |
| LED sendet trotz richtiger Polung nicht | **Vorwiderstand 220 kΩ statt 220 Ω** (Farbringe rot-rot-gelb statt rot-rot-braun) | Widerstand vor dem Löten messen | 10.10. |
| Weiter keine Antwort, Bauteile in Ordnung | **Fenster 2,4 mm zu hoch** – V-Spitze liegt 3,5 mm unter, V-Oberkante 6,2 mm über der Lampenmitte | `v_versatz_y = 0.9`, Kopf neu gedruckt | 11.10. |
| Kopf hält nicht | Front der Regelung ist **Kunststoff**, die Magnete greifen nicht | Klebeband (in der funktionierenden Lage) | 11.10. |
| ESP32 „tot“, serielle Ausgabe bricht beim Boot ab | **Kein Defekt:** WLAN-Access-Point leitete auf 2,4 GHz nichts weiter; der Abbruch der seriellen Ausgabe ist normal | Vor einem Defekt-Urteil prüfen, ob andere WLAN-Geräte zur selben Zeit ausfielen; Board am USB des PCs gegenprüfen | 10./11.10. |
| Warteschlange 18–22, Zeitüberschreitungen | Mehr Abfragen als der Bus schafft (~17 Lesungen/min bei 4800 Baud) | Intervalle verlängern (siehe README, Abschnitt 6) | 12.10. |
| Warmwasser-Soll nach Neustart 5 statt 55 °C | erster Wert nach dem Start unplausibel | Filter: Werte außerhalb 30–95 °C verwerfen | 12.10. |
| **Sammelstörung** kurz „an“ (2–17 min, ~20× am Tag), Regelung zeigt keine Störung | **Geklärt 14.10. (Debug-Mitschnitt):** Nach jeder Bus-Unterbrechung („communication disrupted – suspending … 20000 ms“, ~1×/min) liefert die **erste Anfrage nach „resuming communication“** bei 1-Byte-Datenpunkten das **Sync-Byte 0x05** der Vitotronic als Antwort (21 von 21 Fällen); 0x05 ≠ 0 wird als „an“ gelesen | Schaltzustände als interne 1-Byte-Sensoren lesen, **nur 0/1 übernehmen** (Template-binary_sensor, gleiche Entitäts-IDs); `delayed_on: 30min` bleibt als Reserve | 13./14.10. |
| **Brennerstörung** 4 min „an“ (13.10. 18:07–18:11), Brenner lief, Regelung zeigt keine Störung | derselbe Lesefehler (Sync-Byte 0x05 nach Bus-Unterbrechung, siehe oben), jetzt an `0x0883`; seit 14.10. gefiltert | Alarm mit Plausibilitätsprüfung (README, Abschnitt 8). **Lehre:** Die Kesseltemperatur ist kein Beweis für eine Flamme – sie fiel bei laufendem Brenner unter Last von 80,8 auf 71,7 °C in 5 min. Beweis sind die steigenden Brennerstunden | 13.10. |
| **Heizkurve Neigung** springt zwischen 1,4 und 0,5 | Sync-Byte 0x05 nach Bus-Unterbrechung, durch `÷ 10` als 0,5 gelesen | Filter verwirft 0,5 (eine tatsächlich auf 0,5 gestellte Neigung wäre damit nicht mehr sichtbar) | 19.10. |

Ein weiterer Flashfehler („No more data to read“ bei 460800 Baud) trat am **Tankmessungs-ESP32** auf, nicht an diesem
Gerät. Falls er hier auftritt: mit `esptool … --baud 115200` die fertige `firmware.factory.bin` schreiben.

## Störung an der Regelung selbst prüfen

Die rote Störungsanzeige liegt **unter dem Lesekopf**. Stattdessen (Vitotronic 200 KW2, Serviceanleitung S. 39–40):

| Was | Tasten |
|---|---|
| aktuelle Störung | **ⓘ**, mit **＋/－** blättern (nicht OK – das quittiert) |
| quittierte Störungen | **OK** ca. 2 s |
| Fehlerhistorie (letzte 10, **ohne Datum**) | **„Heizen und Warmwasser“ + OK** ca. 2 s, ＋/－ blättern, OK beendet; **✲ löscht alle Einträge** |

Bei einer Störung blinkt außerdem im Display „Störung“. Code **d1** = Brennerstörung, **0F** = Wartung fällig (nur in der Historie).

## Weitere mögliche Fehlerbilder (hier nicht aufgetreten)

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
