🇬🇧 [English version](verlauf.en.md)

# Projektverlauf

| Datum | Was |
|---|---|
| 03./04.10.2026 | Störung **D1** (Brennerstörung) an der Vitotronic – Tank leer, niemand hat es bemerkt. Idee: Optolink auslesen und in HA melden. |
| 04.10. | Typschild: Vitotronic 200 **KW2**. Weg festgelegt: ESPHome-PR #4453 (`protocol: KW`), Schaltung nach openv/VitoWiFi, Adressen aus der openv-Tabelle V200KW2. |
| 04.10. | WLAN-Test am Kessel mit einem D1 mini: −41/−42 dBm (AP direkt vor dem Heizungskeller). |
| 04.10. | Entscheidung: ESP32-CAM-Set bleibt unangetastet, stattdessen neuer **ESP32-WROOM-32U DevKitC** mit externer Antenne. |
| 04.10. | Bestellt: 2× ESP32 + IR-LEDs (Zustellung 06.10.), Fototransistor L-93DP3C (Zustellung 09.10.), Magnete 10 × 3 mm (06.10.). |
| 04.10. | `heizung-optolink.yaml` geschrieben, validiert und kompiliert (RAM 28 %, Flash 50 %); Gehäuse-SCAD + STL erster Stand. |
| 05.10. | Öl geliefert (1.500 l), Brenner läuft nach Entlüften wieder. |
| 06.10. | Maße gemessen (Jens): Platine 48,24 × 28,15 mm, USB-C ragt 1,6 mm über, Lampenabstand **14,4 mm** → SCAD angepasst. SMA-Bohrung unter die Platine verlegt. |
| 06.10. ~19:40 | ESP32 geflasht, `192.168.178.193`, HA-Integration „Heizung“ mit 24 Entitäten. **Falle:** zuerst Prüfbuild mit Dummy-Secrets geflasht, `upload` kompilierte nicht neu → mit `esphome run` und echten Secrets korrigiert. |
| 06.10. ~20:00 | Im ESPHome Builder eingetragen, online; Builder-Fassung ab jetzt führend. Feste IP in der FRITZ!Box. |
| 06.10. abends | Datenblatt L-93DP3C geprüft: **Kollektor = kurzes Bein**. Schaltplan gedruckt. |
| 07.10. | Erster Druck des ESP-Gehäuses (Jens) zeigt zwei Fehler: Magnettaschen durch den Boden, Auflagen unter den Stiftleisten → Boden 4 mm, 4 Stützen zwischen den Pinreihen. Jens: „passt jetzt so“. |
| 07.10. | USB-Zugriff am PC per udev-Regel dauerhaft gelöst. |
| 08.10. | Optolink-Gehäuse gedruckt (laut Jens). |
| 08.10. | Doku-Repo angelegt. |
| 09.10. | Fototransistor (L-93DP3C) nicht geliefert; als Vorsorge SFH 309 FA bei Reichelt bestellt. Lesekopf-Termin auf Sa 10.10. verschoben. |
| 10.10. | L-93DP3C weiter nicht da → **SFH 309** (3 mm klar) im Elektronik-Fachhandel vor Ort gekauft, Schaltplan umgestellt, Lesekopf gelötet. |
| 10.10. abends | Am Kessel keine Antwort. Zwei Lötfehler gefunden: **IR-LED verpolt** und **LED-Vorwiderstand 220 kΩ statt 220 Ω** (rot-rot-gelb). Danach Reflexionstest bestanden. |
| 10.10. 19:24 | ESP32 fällt aus und bootet am USB scheinbar nicht mehr → für **defekt** gehalten, Ersatz bestellt. **Falsch:** Am 11.10. lief das Board am PC einwandfrei. Zur selben Zeit leitete ein WLAN-Access-Point auf 2,4 GHz nichts weiter; dass die serielle Ausgabe mitten im Boot abbricht, ist normal und kein Absturz. |
| 11.10. ~11:20 | **Erste Antwort der Regelung** (KW-Sync, Kennung `20 98`) – mit einem Raspberry Pi als Übergangs-Leser. Ursache der Fehlversuche: Die **Fenster im Kopf lagen 2,4 mm zu hoch**. Kopf nach unten verschoben → Antwort. |
| 11.10. | Kopf neu konstruiert (`v_versatz_y` −1,5 → 0,9) und gedruckt – passt auf Anhieb. Magnete halten an der Kunststofffront nicht → Kopf mit Klebeband fixiert. |
| 11.10. | **Adress-Scan**: Kessel-Soll ist `0x5502` (nicht `0x555A`), Vorlauf-Soll gibt es an dieser KW2 nicht, genutzter Heizkreis ist **M2** (`0x3906`); neu: Warmwasser-Soll, Heizkurve. Übergangsweise schrieb der Pi die Werte per REST nach HA. |
| 12.10. | **ESP32 am Kessel in Betrieb**, Pi abgebaut. Bus überlastet (~21 Lesungen/min angefordert, ~17 möglich) → Intervalle gesenkt, Warteschlange 0–3. |
| 12.10. | HA: Ölverbrauch aus Brennerlaufzeit (2,4 l/h, ungeeicht). Erkenntnis: `0x0842` ist die **Freigabe**, nicht die Flamme; 1–25 min bis zum Start → Messung der Startverzögerung + Startalarm nach 45 min. |
| 12.10. | `0x7574` (Ölverbrauch der Regelung) = 0 → an dieser Anlage nicht geführt. Warmwasser-Soll-Filter (erster Wert nach Neustart war 5 statt 55) und Sensor „Neustart-Grund“ ergänzt. |
| 13.10. | **Sammelstörung** meldet seit 04:17 rund 20× kurz „an“, Brennerstörung aus, Brenner läuft normal. Display der Regelung zeigt dabei **keine Störung**; Fehlerhistorie: 10× d1 (Tank leer Anfang Oktober) → Lesefehler, Filter `delayed_on: 30min`. |
| 13.10. | **DS18B20 „Zirkulation Rücklauf“** an GPIO4 ergänzt (4,7 kΩ ans Kabelende gelötet, 3V3 per Wago geteilt), erster Wert 46,6 °C. |
| 13.10. 18:07 | **Brennerstörung** meldet 4 min fälschlich „an“ (Brenner lief, Display ohne Störung). Alarm in eigene Automation mit Plausibilitätsprüfung verlegt: Freigabe ≥ 30 min, Brennerstunden bzw. Kessel über 5 min. |
| 14.10. | **Fehlmeldungen geklärt** (Debug-Mitschnitt 17:34–18:24, 266 Anfragen): 47 Bus-Unterbrechungen in 50 min; die erste Anfrage danach liefert bei 1-Byte-Datenpunkten das Sync-Byte **0x05** als Antwort (21/21) → Sammelstörung, HK-Pumpe M2, **Brenner** (in HA 2× ~15 s falsch „an“), Betriebsart. 2/4-Byte-Anfragen laufen danach in Timeout (alte Bytes im Puffer). 18:28 OTA: Schaltzustände nur noch 0/1 übernehmen, Betriebsart/Raumsoll mit Bereichsfilter, Log zurück auf INFO. **Offen:** Ursache der häufigen Timeouts; die Komponente synchronisiert nach der Wiederaufnahme nicht neu. Zirkulation: `0x0846` in 50 min nur 6× gelesen (Soll 25) – erklärt den Versatz zur Rücklauftemperatur höchstens teilweise. |
