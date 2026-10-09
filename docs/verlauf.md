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
| **10.10.** | geplant: Lesekopf löten, aufsetzen, Inbetriebnahme mit `logger: true`, Adressen prüfen (sobald ein Fototransistor da ist). |
