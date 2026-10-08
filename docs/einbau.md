🇬🇧 [English version](einbau.en.md)

# Aufbau und Einbau

Schritt für Schritt vom Bauteil zum aufgesetzten Lesekopf. Schaltplan zum Danebenlegen:
[`../plaene/optolink-schaltplan.pdf`](../plaene/optolink-schaltplan.pdf).

## Vorher bereitlegen

- gedruckte Teile: `kopf`, `kopf_deckel`, `v_schluessel`, `esp`, `esp_deckel` (PETG)
- IR-LED Chanzon 940 nm, Fototransistor Kingbright L-93DP3C, 220 Ω, 10 kΩ
- 4 Neodym-Magnete 10 × 3 mm
- 4 Dupont-Leitungen Buchse–Buchse (rot, schwarz, gelb, grün)
- ESP32-WROOM-32U DevKitC (schon geflasht) mit Antenne + IPEX→SMA-Pigtail
- Lötkolben, Multimeter, Schrumpfschlauch/Isolierband, ggf. Heißkleber

## 1. Bauteile prüfen

1. **IR-LED:** langes Bein = Anode (+), kurzes Bein/flache Seite = Kathode.
   Diodentest: rot an Anode, schwarz an Kathode → Durchlassspannung wird angezeigt.
2. **Fototransistor L-93DP3C:** laut Datenblatt **Kollektor = kurzes Bein**, Emitter = langes Bein.
   Mit dem Multimeter gegenprüfen (Widerstand Kollektor→Emitter fällt bei Licht bzw. Fernbedienungs-IR deutlich).
3. Falsch eingebaut zerstört nichts – es kommen dann nur keine Daten.

## 2. Lesekopf löten

1. Kopf mit der Rückseite zu dir halten, Prägung **„OBEN“ nach oben**.
   Dann gilt dieselbe Seite wie beim Blick auf die Regelung:
   - **links („LED“)** → IR-LED (sendet in die rote Empfangslampe der Regelung)
   - **rechts („FT“)** → Fototransistor (empfängt von der grünen Sendelampe)
2. Beide Bauteile von hinten in die Fenster stecken, bis der Bauteilfuß am Kragen anliegt; die Linse schließt mit der
   Front (4 mm) bündig ab. Ggf. mit einem Tropfen Kleber sichern.
3. Im Hohlraum (12 mm tief) verdrahten:

   | Von | Nach |
   |---|---|
   | rot (3V3) | 220 Ω → LED-Anode **und** 10 kΩ → FT-Kollektor |
   | gelb (GPIO17) | LED-Kathode |
   | grün (GPIO16) | FT-Kollektor (gemeinsam mit dem 10 kΩ) |
   | schwarz (GND) | FT-Emitter |

4. Lötstellen isolieren, die vier Litzen oben durch den Kabelauslass (7 × 4 mm) führen.
5. **Zwei Magnete** von hinten in die Taschen ober- und unterhalb der Fenster (0,6 mm Restwand zur Front – sie halten
   durch). Polung so, dass der Kopf an der Regelung hält.
6. **V-Schlüssel** mit dem 2-mm-Zapfen in die Tasche in der Front stecken (Spitze nach unten), bei Bedarf kleben.
7. `kopf_deckel` aufstecken; der Kabelauslass im Steckkragen muss über dem im Kopf liegen.

## 3. ESP-Gehäuse bestücken

1. Je einen Magneten von unten in die beiden Bodentaschen (0,8 mm Restwand).
2. SMA-Buchse des Pigtails von innen durch die Bohrung rechts unten (Ø 6,6 mm), Mutter außen festziehen.
   Die Bohrung liegt bewusst **unter** der Platine.
3. Pigtail auf die IPEX-Buchse des ESP32 drücken.
4. Dupont-Leitungen auf die Stifte `3V3`, `GND`, `GPIO17`, `GPIO16` stecken (siehe Tabelle im README).
5. Platine mit **USB-C zur linken Stirnseite** auf die vier Stützen legen. Die Stützen stehen zwischen den
   Stiftreihen; darunter haben Stifte und Dupont-Buchsen Platz. Bei Bedarf mit Heißkleber fixieren.
6. Dupont-Leitungen durch den seitlichen Auslass (12 × 6 mm, nahe der USB-Seite) führen.
7. Deckel aufstecken.

## 4. Montage am Kessel

1. Lesekopf mit dem V-Schlüssel in den „V“-Ausschnitt der Vitotronic setzen (vorn links); die Magnete halten ihn.
   Der V-Steg ragt 6 mm vor, die Regelung erlaubt höchstens 8 mm.
2. ESP-Gehäuse in Reichweite der Litzen magnetisch an das Kesselblech setzen.
3. Antenne an die SMA-Buchse schrauben.
4. USB-C-Strom anschließen (Netzteil/Kabelweg ist in den Notizen noch nicht festgelegt).
5. Weiter mit [`einmessen.md`](einmessen.md).

## Hinweise

- Der „Entsperrung“-Knopf an der Regelung ist der **STB**, nicht der Brenner-Reset. Der Brenner-Reset ist der rote
  Entstörknopf am Feuerungsautomaten (Landis & Gyr LOA24). Für dieses Projekt muss keins von beiden betätigt werden.
- Den AFRISO-Leckanzeiger an der Tankanzeige nicht anfassen (gehört zum Tank, nicht hierher).
