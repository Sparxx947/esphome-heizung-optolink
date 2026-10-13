🇬🇧 [English version](README.en.md)

# Heizung · Optolink (Vitotronic 200 KW2 → ESPHome → Home Assistant)

Selbstbau-Lesekopf an der Optolink-Schnittstelle einer Viessmann-Ölheizung. Ein ESP32 mit ESPHome
liest Temperaturen, Brennerzustand, Brennerstunden und **Störmeldungen** aus der Regelung und gibt sie an
Home Assistant weiter. **Bewusst nur lesend** – die Firmware enthält nichts, was in die Regelung schreibt.

> Stand dieser Dokumentation: **13.10.2026**. **In Betrieb seit 12.10.2026**: Der Lesekopf sitzt an der Regelung,
> der ESP32 liest alle Werte und gibt sie an Home Assistant. Seit 13.10. misst ein zusätzlicher **DS18B20** die
> Temperatur der Zirkulationsleitung.

> **Nachbauen:** Eigene Secrets nach der Vorlage [`firmware/secrets.example.yaml`](firmware/secrets.example.yaml)
> anlegen (WLAN, API-Schlüssel, Hotspot-Passwort) und die feste IP an das eigene Netz anpassen. Die Adressen in der
> Firmware gelten für die Vitotronic 200 KW2 – für andere Viessmann-Regelungen stehen sie im
> [openv-Wiki](https://github.com/openv/openv/wiki) (Seite „Adressen“).

---

## 1. Kurzbeschreibung

| | |
|---|---|
| **Anlage** | Ölkessel Viessmann **Vitola 111** (mit integriertem Speicher), Regelung **Vitotronic 200 Typ KW2** (witterungsgeführt, Gerätekennung `0x2098`), Brenner Viessmann VEA I-2 (Bj. 1999, max. 2,0 kg/h ≈ 2,4 l/h) |
| **Einbauort** | Heizungskeller, Lesekopf vorn links am „V“ der Regelung, ESP-Gehäuse magnetisch am Kesselblech |
| **Was gemessen wird** | Brennerstörung (Anzeige **D1**), Sammelstörung, Brennerfreigabe, Pumpen, Außen-/Kessel-/Warmwasser-/Vorlauftemperaturen, Kessel- und Warmwasser-Sollwert, Heizkurve, Brennerstarts, **Brennerstunden**; dazu per DS18B20 die **Zirkulation (Rücklauf)** |
| **Was gesteuert wird** | nichts (absichtlich) |
| **Ziel** | Push bei Brennerstörung (Anlass: Störung D1 am 03./04.10.2026 bei leerem Tank, die niemand bemerkt hat); Ölverbrauch aus Brennerstunden × Düsendurchsatz als Grundlage für eine Tankprognose |

**Prinzip:** Die Vitotronic hat vorn hinter einem „V“-förmigen Ausschnitt zwei Lämpchen – eine IR-Empfangsdiode
(links, rot) und eine IR-Sendediode (rechts, grün). Darüber spricht sie seriell im **KW-Protokoll (VS1), 4800 Baud 8E2**.
Der Lesekopf sitzt davor: eine **IR-LED** (940 nm) sendet in die linke Lampe, ein **Fototransistor**
empfängt von der rechten. Der ESP32 bedient beide über einen UART (RX GPIO16 / TX GPIO17) mit der ESPHome-Komponente
`optolink` aus **ESPHome-PR #4453** (noch nicht in ESPHome gemergt). Schaltung nach VitoWiFi/openv-Wiki.

---

## 2. Status (Stand 13.10.2026)

| Bereich | Status | Datum / Bemerkung |
|---|---|---|
| Konzept, Schaltung | ✅ fertig | 04.10. |
| Adressen | ✅ an der Anlage geprüft | 11.10. – Adress-Scan; drei Adressen der openv-Tabelle passten nicht (siehe Abschnitt 6) |
| Firmware (YAML) | ✅ in Betrieb | Stand 13.10. (RAM 28,5 %, Flash 50,9 %) |
| ESP32, WLAN, HA | ✅ in Betrieb | `192.168.178.193`, HA-Integration „Heizung“, 29 Entitäten |
| Gehäuse | ✅ gedruckt | ESP-Gehäuse 07./08.10.; Lesekopf am 11.10. neu gedruckt (Fenster lagen 2,4 mm zu hoch) |
| Lesekopf | ✅ in Betrieb | gelötet 10.10. (SFH 309), erste Antwort der Regelung 11.10., am ESP32 seit 12.10. |
| Busauslastung | ✅ entlastet | 12.10. – Abfrageintervalle gesenkt, Warteschlange meist 0–3 |
| HA: Push bei Brennerstörung | ✅ aktiv | nach 5 min Störung an alle Bewohner, mit Durchsage |
| HA: Ölverbrauch aus Brennerlaufzeit | ✅ aktiv, **nicht geeicht** | seit 12.10.; Düsendurchsatz 2,4 l/h = Typschild-Maximum, Eichung gegen die Tankmessung geplant |
| HA: Startverzögerung + Startalarm | ✅ aktiv | 12.10. – Push, wenn der Brenner 45 min nach der Freigabe nicht startet |
| Zirkulationsfühler DS18B20 | ✅ in Betrieb | 13.10. – GPIO4, erster Wert 46,6 °C bei laufender Pumpe |
| Sammelstörung | ⚠️ mit Filter | 13.10. – meldete ~20× kurz „an“ ohne Störung an der Regelung; meldet jetzt erst nach 30 min |

---

## 3. Stückliste

Preise und ASINs zum Zeitpunkt der Bestellung (Amazon.de, Oktober 2026).

| Teil | Menge | Bezeichnung / Typ | Bezugsquelle, ASIN, Preis | Status |
|---|---|---|---|---|
| Mikrocontroller | 1 | **ESP32-WROOM-32U DevKitC V4**, USB-C, CP2102, IPEX-Antennenbuchse; Platine 48,24 × 28,15 mm | Amazon **B0F6567LB5**, 13,99 € (2 Stück bestellt, der zweite ist die Tankmessung) | ✅ geliefert 06.10., geflasht |
| Antenne | 1 | 2,4-GHz-Antenne mit IPEX→SMA-Pigtail (SMA-Buchse Ø ~6,4 mm, 1/4″) | im Antennen-Kit des ESP32 enthalten | ✅ vorhanden |
| IR-LED | 1 (+ Reserve) | **Chanzon** IR-LED 940 nm, 3 mm, 100 Stück (Ersatz für SFH487 / SIR 204 aus dem openv-Wiki) | Amazon **B01BVEKXNC**, 7,99 € | ✅ bestellt 04.10., Zustellung 06.10. angekündigt (Eingang nicht ausdrücklich notiert) |
| Fototransistor | 1 | **Osram SFH 309**, 3 mm klar (eingebaut) | Elektronik-Fachhandel vor Ort, 10.10. | ✅ eingebaut 10.10. |
| (Fototransistor) | – | Kingbright L-93DP3C, 3 mm, 940 nm (ursprünglich bestellt) | Amazon **B01M3PGVRC**, 9,77 € (Marketplace) | ❌ kam nicht rechtzeitig, nicht verwendet |
| Widerstand | 1 | 220 Ω (Vorwiderstand IR-LED) | AZ-Delivery-Widerstandssortiment | ✅ vorhanden |
| Widerstand | 1 | 10 kΩ (Pull-up Fototransistor) | AZ-Delivery-Widerstandssortiment | ✅ vorhanden |
| Magnete | 4 | Neodym-Scheibenmagnet **10 × 3 mm** (2 im Lesekopf, 2 im Boden des ESP-Gehäuses) | Amazon, Delaga, 50 Stück, 7,99 € | ✅ verbaut – **am Kopf wirkungslos** (Front der Regelung ist Kunststoff), Kopf mit Klebeband befestigt |
| Temperaturfühler | 1 | **DS18B20** wasserdicht, Edelstahlhülse, 3 Adern, 2 m Kabel (5er-Pack) | Amazon **B0HG8Y9X45**, 10,49 € | ✅ eingebaut 13.10. |
| Widerstand | 1 | 4,7 kΩ (Pull-up DS18B20, gelb-violett-rot) | Widerstandssortiment | ✅ eingebaut 13.10. |
| Verbinder | 1 | Wago-Klemme (3V3 für Lesekopf **und** Fühler, der DevKitC hat nur einen 3V3-Pin) | vorhanden | ✅ |
| Verbindungskabel | 4 | Dupont-Jumper **Buchse–Buchse** (F2F), Farbvorschlag rot/schwarz/gelb/grün | ELEGOO-Jumper-Set M2M/F2M/F2F (40 × 20 cm) | ✅ vorhanden |
| Stromversorgung | 1 | USB-C-Kabel + USB-Netzteil 5 V | vorhanden | ✅ in Betrieb seit 12.10. (Sensor „Neustart-Grund“ zeigt Unterspannung als „Brownout“) |
| Filament | ~20 g (geschätzt) | **PETG** (Wärme am Kessel) | vorhanden | ✅ vorhanden, Gehäuse gedruckt 08.10. |
| Kleber | wenig | Heißkleber (Platine auf Stützen fixieren, optional) bzw. Sekundenkleber für V-Schlüssel (optional) | vorhanden (angenommen) | ✅ |
| Schrauben | 0 | keine – Steckdeckel und Magnete | – | – |
| Werkzeug | – | Lötkolben, Multimeter (Diodentest), Messschieber, 3D-Drucker | vorhanden | ✅ |

Nicht verwendet, aber verwechslungsgefährdet: Das **AZ-Delivery-LED-Sortiment** ist sichtbares Licht und für Optolink
unbrauchbar. Das **ESP32-CAM-Set** (mit MB-Board) bleibt unangetastet – es war ursprünglich vorgesehen, wurde am
04.10. aber zugunsten eines neuen ESP32 verworfen.

Original-Bauteile laut openv/VitoWiFi: IR-LED **SFH487** (bzw. SIR 204 EVL), Fototransistor **SFH309FA**. Verbaut ist
der **SFH 309** (klare Linse, ohne Tageslichtfilter) – er funktioniert, weil der Kopf das Fremdlicht abschirmt.

---

## 4. Pinbelegung und Verdrahtung

Schaltplan zum Ausdrucken: [`plaene/optolink-schaltplan.pdf`](plaene/optolink-schaltplan.pdf)
(SVG: [`plaene/optolink_plan.svg`](plaene/optolink_plan.svg), Erzeuger: [`plaene/optolink_plan.py`](plaene/optolink_plan.py)).

```
3,3 V ── 220 Ω ── IR-LED (Anode) │ Kathode ── GPIO17 (TX)
3,3 V ── 10 kΩ ──┬── GPIO16 (RX)
                 └── Kollektor Fototransistor │ Emitter ── GND
```

**Die Widerstände sitzen im Lesekopf**, zum ESP gehen nur vier Leitungen:

| Leitung | ESP32-Pin (Aufdruck) | Im Lesekopf an | Farbvorschlag |
|---|---|---|---|
| 1 | `3V3` | 220 Ω (zur LED-Anode) **und** 10 kΩ (zum FT-Kollektor) | rot |
| 2 | `GND` | Emitter Fototransistor | schwarz |
| 3 | `GPIO17` / „TX2“ / „17“ | Kathode IR-LED | gelb |
| 4 | `GPIO16` / „RX2“ / „16“ | Kollektor Fototransistor + 10 kΩ | grün |

**Beinchen:**

| Bauteil | Langes Bein | Kurzes Bein | Quelle |
|---|---|---|---|
| IR-LED (Chanzon) | Anode (+) → 220 Ω | Kathode (flache Seite) → GPIO17 | übliche LED-Konvention |
| Fototransistor SFH 309 (verbaut) | Emitter → GND | **Kollektor** (abgeflachte Seite) → GPIO16 + 10 kΩ | Osram-Datenblatt („Package marking: Collector“) |
| Fototransistor L-93DP3C (Alternative) | Emitter → GND | **Kollektor** → GPIO16 + 10 kΩ | Kingbright-Datenblatt (DSAC1289) |

Vor dem Löten mit dem Multimeter gegenprüfen. **Am 10.10. war die IR-LED verpolt eingelötet und der LED-Vorwiderstand
220 kΩ statt 220 Ω** (Farbringe rot-rot-**gelb** statt rot-rot-**braun**) – beides zusammen kostete einen Abend. Falsch
herum geht nichts kaputt, es kommen nur keine Daten.

**Lage im Kopf** (Blick **auf** die Regelung = Blick auf die Rückseite des Kopfs beim Löten):

| Position | Lampe der Regelung | Funktion der Regelung | Unser Bauteil |
|---|---|---|---|
| links | rot („Störung“) | IR-Empfänger | **IR-LED** |
| rechts | grün („Betrieb“) | IR-Sender | **Fototransistor** |

Abstand der Lampen Mitte–Mitte: **14,4 mm** (Jens gemessen 06.10.; openv-Wiki nennt 14 mm).
Im Kopf ist innen „LED“, „FT“ und „OBEN“ eingeprägt.

**Höhe:** Die V-Spitze der Regelung liegt **3,5 mm unter**, die V-Oberkante **6,2 mm über** der Lampenmitte (gemessen
11.10.). Mit dem ersten Kopf lagen die Fenster 2,4 mm zu hoch – die Regelung antwortete erst, als der Kopf nach unten
verschoben wurde. Korrigiert über `v_versatz_y = 0.9` im SCAD.

> **Die rote Lampe ist zugleich die Störungsanzeige der Regelung.** Mit aufgesetztem Kopf ist sie verdeckt. Eine Störung
> erkennt man dann am Display („Störung“ blinkt, Taste ⓘ zeigt den Code) – oder in Home Assistant.

### Zusatz: Zirkulationsfühler DS18B20 (seit 13.10.)

Plan zum Ausdrucken: [`plaene/ds18b20-zirkulation-plan.pdf`](plaene/ds18b20-zirkulation-plan.pdf)
(Erzeuger [`plaene/ds18b20_plan.py`](plaene/ds18b20_plan.py)). Belegung von Lesekopf und Fühler am ESP32:
[`plaene/esp32-belegung.pdf`](plaene/esp32-belegung.pdf) (Lesekopf **und** Fühler, Stand 13.10.; Erzeuger [`plaene/esp32_belegung_plan.py`](plaene/esp32_belegung_plan.py)).

| Fühlerader | ESP32-Pin | Bemerkung |
|---|---|---|
| rot | `3V3` über Wago | der DevKitC hat nur **einen** 3V3-Pin – den teilen sich Lesekopf und Fühler |
| schwarz | `GND` (rechte Reihe, 7. von oben) | |
| gelb | `GPIO4` (rechte Reihe, 13. von oben, direkt unter 16) | 4,7 kΩ zwischen gelb und rot, am Kabelende eingelötet |

Der Fühler liegt flach auf der Zirkulationsleitung (Rücklauf vom Haus zum Speicher) nahe der Zirkulationspumpe,
mit Kabelbindern befestigt und unter der Rohrisolierung. Zweck: erkennen, wann die Zirkulation läuft (warm) und wann
nicht (kühlt aus) – die Pumpe selbst meldet die Regelung zwar (`0x0846`), aber nicht, ob tatsächlich Wasser fließt.

---

## 5. Gehäuse

Quelle: [`gehaeuse/optolink-gehaeuse.scad`](gehaeuse/optolink-gehaeuse.scad) (OpenSCAD, parametrisch; Teil über
`TEIL = "…"` wählen). Geometrie des Kopfs angelehnt an `vito.scad` aus dem openv-Wiki.

| STL | Wofür | Maße (aus SCAD) | Druckausrichtung |
|---|---|---|---|
| [`kopf.stl`](gehaeuse/kopf.stl) | Lesekopf: Frontplatte 4 mm mit zwei Fenstern Ø 3,2 mm (14,4 mm Abstand), Kragenanschlag für die Bauteilfüße, 2 Magnettaschen 10,3 × 3,2 mm (0,6 mm Restwand zur Front), Hohlraum 12 mm für Widerstände, Kabelauslass 7 × 4 mm oben | Ø 34 mm, 16 mm tief | **Front aufs Bett** |
| [`kopf_deckel.stl`](gehaeuse/kopf_deckel.stl) | Rückdeckel mit Steckkragen und Kabelauslass für 4 Litzen | Ø 34 mm | flach |
| [`v_schluessel.stl`](gehaeuse/v_schluessel.stl) | Führungs-„V“, wird mit 2-mm-Zapfen in die Front gesteckt (ggf. geklebt) und greift ins „V“ der Regelung (ragt 6 mm vor, max. 8 zulässig) | Steg 1,6 mm | stehend |
| [`esp.stl`](gehaeuse/esp.stl) | Gehäuse für den ESP32: USB-C an der linken Stirnseite, SMA-Bohrung Ø 6,6 rechts **unter** der Platine, Dupont-Auslass 12 × 6 mm seitlich unten, Lüftungsschlitze, 2 Magnettaschen im Boden, Prägung „HEIZUNG“ | außen ca. 55,5 × 33,8 × 31 mm, innen 51,5 × 29,8 mm | Boden aufs Bett |
| [`esp_deckel.stl`](gehaeuse/esp_deckel.stl) | Steckdeckel | – | flach |

**Nachtrag 11.10.:** Die Fenster im ersten Kopf lagen 2,4 mm zu hoch (`v_versatz_y` war −1,5, richtig ist **0,9**);
`kopf.stl` ist neu erzeugt. Die Vorschaubilder zeigen noch den alten Stand. Die **Magnete im Kopf halten nicht** – die
Front der Vitotronic ist aus Kunststoff. Der Kopf ist mit Klebeband in der funktionierenden Lage befestigt.

Vorschauen: [`vorschau_alle.png`](gehaeuse/vorschau_alle.png), [`vorschau_esp.png`](gehaeuse/vorschau_esp.png),
[`vorschau_kopf_vorn.png`](gehaeuse/vorschau_kopf_vorn.png), [`vorschau_kopf_hinten.png`](gehaeuse/vorschau_kopf_hinten.png).

**Druckeinstellungen:** PETG (Kesselnähe), 0,2 mm Schicht, 3 Wände, **ohne Stützmaterial**.

**Bestückung ESP-Gehäuse:** Die Platine liegt mit den beiden Stirnseiten auf **vier Stützen** (je Stirnseite zwei,
17 mm hoch, ca. 4,9 mm breit, 4,5 mm tief), die **zwischen den Stiftleisten** stehen: 3,2 mm Abstand zum Längsrand,
12 mm in der Mitte frei (dort sitzen die USB-Lötlaschen bzw. die SMA-Mutter). Bei Bedarf mit Heißkleber fixieren.
Unter der Platine ist Platz für die nach unten zeigenden Stifte und die Dupont-Buchsen. SMA-Buchse von innen durch
die Bohrung stecken, Mutter außen. Je ein Magnet in die beiden Bodentaschen (von unten), zwei in den Kopf (von hinten).

**Lehren aus den Fehldrucken** (Details in [`docs/verlauf.md`](docs/verlauf.md)):

| Fehler | Ursache | Korrektur |
|---|---|---|
| SMA-Bohrung wäre zugewachsen (06.10.) | lag hinter der rechten Platinenauflage | Bohrung unter die Platine (`sma_z = 8`), 12 mm Lücke für die Mutter |
| Magnettaschen gingen durch den Boden (07.10.) | Tasche 3,2 mm tief in 2,0-mm-Boden | `boden = 4.0` → 0,8 mm Restwand |
| Platine lag auf den Stiften (07.10.) | Stiftleisten laufen über die **ganze** Platinenlänge (19 × 2,54 = 48,3 mm); durchgehende Auflagen blockierten die Pins | 4 Einzelstützen zwischen den Pinreihen |

Regel daraus: Vor jedem STL-Export jede Tasche gegen die Wandstärke prüfen und die Platinen-Unterseite
(Stiftleisten, Buchsen, Lötlaschen) gegen jede Auflage; kritische Maße vorher messen lassen.

---

## 6. Firmware

Datei: [`firmware/heizung-optolink.yaml`](firmware/heizung-optolink.yaml) – entspricht dem Stand im ESPHome Builder.

| Einstellung | Wert |
|---|---|
| Gerätename / Hostname | `heizung-optolink` → `heizung-optolink.local` |
| Anzeigename (`friendly_name`) | `Heizung` |
| IP | **192.168.178.193** (feste DHCP-Reservierung in der FRITZ!Box) |
| Board / Framework | `esp32dev`, **Arduino** (Pflicht für die Optolink-Komponente) |
| Externe Komponente | `github://pr#4453`, Komponente `optolink` |
| Optolink | `protocol: KW`, `rx_pin: GPIO16`, `tx_pin: GPIO17`, `logger: false` (für Inbetriebnahme `true`) |
| 1-Wire | `GPIO4`, ein DS18B20 (`dallas_temp`, ohne feste Adresse – nur ein Fühler am Bus) |
| Logger | `level: INFO`; UART0 bleibt für das USB-Log frei |
| API | verschlüsselt (`heizung_api_key`) |
| OTA | `platform: esphome`, ohne eigenes Passwort (abgesichert über den API-Schlüssel) |
| Fallback-Hotspot | SSID `Heizung-Fallback`, Passwort aus Secret, mit Captive Portal |

### Entitäten in Home Assistant (29)

Gerät „Heizung“ in der ESPHome-Integration, Entity-IDs `sensor.heizung_…` / `binary_sensor.heizung_…`
(z. B. `sensor.heizung_brennerstunden`, `sensor.heizung_zirkulation_rucklauf`). Einige später ergänzte Entitäten
bekamen von HA das Präfix des Bereichs (`…heizungskeller_heizung_…`).

| Name | Typ | Adresse | Format | Intervall | Befund |
|---|---|---|---|---|---|
| Brennerstörung (= Anzeige D1) | binär, problem | `0x0883` | 0/1 | 120 s | ✅ |
| Sammelstörung | binär, problem, **`delayed_on: 30min`** | `0x0847` | 0/1 | 120 s | ⚠️ Fehlmeldungen, siehe [Fehlersuche](docs/fehlersuche.md) |
| Brenner | binär, running | `0x0842` | 0/1 | 30 s | ✅ – **Freigabe der Regelung, nicht Flamme** |
| Speicherladepumpe | binär, running | `0x0845` | 0/1 | 120 s | ✅ |
| Zirkulationspumpe | binär, running | `0x0846` | 0/1 | 120 s | ✅ |
| Heizkreispumpe (A1) | binär, running | `0x2906` | 0/1 | 1800 s | immer aus – Heizkreis ohne Mischer nicht genutzt |
| Heizkreispumpe M2 | binär, running | `0x3906` | 0/1 | 120 s | ✅ – der genutzte Heizkreis |
| Zirkulation Rücklauf | °C (DS18B20) | GPIO4 | – | 60 s | ✅ 13.10. |
| Außentemperatur | °C | `0x0800` | 2 B ÷ 10, vorzeichenbehaftet | 120 s | ✅ |
| Außentemperatur gedämpft | °C | `0x5527` | 2 B ÷ 10, vorzeichenbehaftet | 600 s | ✅ |
| Kesseltemperatur | °C | `0x0802` | 2 B ÷ 10 | 60 s | ✅ |
| Kesselsolltemperatur | °C | **`0x5502`** | 2 B ÷ 10 | 300 s | ✅ (`0x555A` aus der Tabelle liefert hier FF FF) |
| Warmwassertemperatur (Speicher) | °C | `0x0804` | 2 B ÷ 10 | 120 s | ✅ |
| Vorlauftemperatur (Sensor 17B) | °C | `0x080C` | 2 B ÷ 10 | 120 s | ✅ |
| Warmwasser-Solltemperatur | °C | `0x6300` | 1 B, Filter 30–95 °C | 600 s | ✅ (erster Wert nach Neustart war einmal 5 statt 55) |
| Abgastemperatur | °C, Diagnose | `0x0808` | 2 B ÷ 10 | 1800 s | kein Abgasfühler verbaut – konstanter Wert |
| Brennerstarts | Zähler | `0x088A` | 4 B | 60 s | ✅ |
| Brennerstunden (Stufe 1) | h, total_increasing | `0x08A7` | 4 B, Sekunden ÷ 3600 | 60 s | ✅ |
| Ölverbrauch Regelung | Diagnose | `0x7574` | 4 B ÷ 1000 | 1800 s | immer 0 – an dieser KW2 nicht geführt |
| Heizkurve Neigung | Diagnose | `0x2305` | 1 B ÷ 10 | 1800 s | ✅ (1,4) |
| Heizkurve Niveau | K, Diagnose | `0x2304` | 1 B, vorzeichenbehaftet | 1800 s | ✅ (0) |
| Betriebsart (Rohwert) | Diagnose | `0x2301` | 1 B | 600 s | Zuordnung offen |
| Raumtemperatur Soll | °C, Diagnose | `0x2306` | 1 B | 600 s | unplausibel – Zuordnung offen |
| Optolink-Warteschlange | Diagnose | – | `QUEUE_SIZE` | 60 s | |
| Gerätekennung | Text, Diagnose | – | `DEVICE_INFO` | 1800 s | ✅ `Device ID: 2098` |
| Optolink-Status | Text, Diagnose | – | `STATE_INFO` | 30 s | |
| Neustart-Grund | Text, Diagnose | – | `debug: reset_reason` | 3600 s | nach OTA „software via esp_restart“ |
| WLAN-Signal | dBm | – | – | 120 s | |
| Laufzeit | s | – | – | 600 s | |

✅ = Wert plausibel (Adress-Scan 11.10., Betrieb seit 12.10.); nicht jeder Wert wurde einzeln mit dem Display verglichen.

Entfernt am 11.10.: **Vorlaufsolltemperatur** (`0x2544` bzw. `0x3544` liefern an dieser KW2 FF FF).

**Busauslastung:** Der Optolink schafft im KW-Protokoll bei 4800 Baud rund **17 Lesungen pro Minute**. Die erste
Fassung forderte ~21 an – die Warteschlange stand bei 18–22, es gab Zeitüberschreitungen. Seit dem 12.10. sind es
rechnerisch ~9 pro Minute (Intervalle in der Tabelle), die Warteschlange liegt meist bei 0–3, direkt nach einem
Neustart kurz höher. Der DS18B20 hängt an einem eigenen Bus und belastet den Optolink nicht.

### Secrets

[`firmware/secrets.example.yaml`](firmware/secrets.example.yaml) ist nur eine Vorlage mit den Schlüsselnamen
`wifi_ssid`, `wifi_password`, `heizung_api_key`, `heizung_ap_password`. **Echte Werte stehen nur im ESPHome Builder**
(dessen `secrets.yaml`), nie im Repo – `.gitignore` schließt `secrets.yaml` und `secrets.*.yaml` aus.
API-Schlüssel erzeugen: `openssl rand -base64 32`.

### Flashen

| Weg | Wann | Wie |
|---|---|---|
| **Builder, OTA** (Normalfall) | jede Änderung | YAML im ESPHome Builder bearbeiten → **INSTALL → Wirelessly** |
| **USB** (Erstflash / Notfall) | leeres Board, Gerät nicht mehr im WLAN | `esphome run heizung-optolink.yaml --no-logs --device /dev/ttyUSB0` mit **echten** Secrets (z. B. per podman-Image `ghcr.io/esphome/esphome`) |
| OTA vom PC (Notweg) | Builder nicht verfügbar | `esphome run … --no-logs --device 192.168.178.193` mit echten Secrets in einer temporären `secrets.yaml`, danach löschen |

> **Falle (06.10. passiert):** Nie einen Prüfbuild mit Dummy-Secrets flashen – das Gerät bekommt dann falsches
> Hotspot-Passwort und falschen API-Schlüssel. Und `esphome upload` **kompiliert nicht neu**, sondern spielt den
> letzten Build aus `.esphome/` auf. Für echte Firmware immer `esphome run`, auf „Successfully compiled“ achten und
> danach per API mit dem echten Schlüssel gegenprüfen.

Der Builder ist die führende Fassung. Wird dort etwas geändert, diese Datei hier nachziehen (und umgekehrt).

---

## 7. Anleitungen

Ausführlich in eigenen Dateien:

- [`docs/einbau.md`](docs/einbau.md) – Aufbau des Lesekopfs, Bestückung des Gehäuses, Montage am Kessel
- [`docs/einmessen.md`](docs/einmessen.md) – Inbetriebnahme, Adressen gegen das Display prüfen, Ölverbrauch aus Brennerstunden eichen
- [`docs/fehlersuche.md`](docs/fehlersuche.md) – bekannte Fehlerbilder mit Ursache und Lösung

### Kurzfassung

1. **Löten:** IR-LED links, Fototransistor rechts (Blick auf die Rückseite des Kopfs, „OBEN“ oben), Beinchen vorher
   per Diodentest prüfen, Widerstände im Kopf, 4 Dupont-Litzen durch den Kabelauslass.
2. **Gehäuse:** Magnete einsetzen, V-Schlüssel in die Front stecken, ESP auf die Stützen, Antenne an SMA.
3. **Firmware:** im Builder `optolink:` → `logger: true` setzen, **INSTALL → Wirelessly**.
4. **Aufsetzen:** Kopf mit dem V in den Ausschnitt der Regelung, **mit Klebeband sichern** (die Magnete halten an
   der Kunststofffront nicht), ESP-Gehäuse magnetisch ans Kesselblech, USB-Strom.
5. **Prüfen:** Log zeigt Antworten, „Optolink-Status“ verlässt `unknown`, Gerätekennung `Device ID: 2098`;
   Kessel- und Außentemperatur mit dem Display vergleichen. Kommt nichts: Kopf **in der Höhe** verschieben.
6. **Abschließen:** `logger: false`, erneut OTA; HA-Automationen anlegen (Abschnitt 8).

---

## 8. Home-Assistant-Anbindung

Im Repo liegen **keine HA-Pakete** – alles ist in der HA-Oberfläche angelegt (UI-Helfer und -Automationen).

| Vorhaben | Umsetzung | Status |
|---|---|---|
| Push bei **Brennerstörung** | Brennerstörung 5 min `on` → Nachricht an alle Bewohner (alle Kanäle) mit Durchsage und letztem Ölbestand der Tankmessung | ✅ aktiv |
| Push bei **Sammelstörung** | – | ❌ bewusst nicht: die Adresse liefert gelegentlich Fehlmeldungen |
| **Ölverbrauch** | `input_number` „Öl-Düsendurchsatz“ (2,4 l/h) × Utility-Meter „Brennerstunden seit Messbeginn“ (zählt nur Zuwächse, ESP-Ausfälle verlieren nichts) → Template „Heizöl verbraucht“ + Tageszähler | ✅ aktiv, **nicht geeicht** |
| **Startverzögerung** | Freigabe (`0x0842` an) stempelt die Zeit, der nächste Anstieg der Brennerstarts schreibt die Wartezeit in `input_number` | ✅ aktiv |
| **Startalarm** | Freigabe seit 45 min, aber kein Start → Push „Brenner startet nicht“; startet er später doch → Entwarnung | ✅ aktiv, Selbsttest läuft beim nächsten Brennerstart |
| Tankprognose / Warnung | über die separate pneumatische Tankmessung | ✅ dort umgesetzt |

**Erkenntnis 12.10.:** `0x0842` („Brenner“) ist die **Freigabe** durch die Regelung, nicht die Flamme. Zwischen
Freigabe und tatsächlichem Start vergehen an dieser Anlage 1–25 min (Ursache ungeprüft, vermutlich Ölvorwärmung).
Gestartet hat der Brenner, wenn der Zähler „Brennerstarts“ steigt.

**Wichtig für Automationen:** Ohne Verbindung melden die Optolink-Binärsensoren `unknown`/`unavailable`, nicht `off`.
„Brennerstörung = aus“ ist deshalb kein Beleg für störungsfreien Betrieb.

Die Füllstandsmessung am Erdtank (pneumatisch, eigener ESP32) ist ein **eigenes Projekt** und nicht Teil dieses Repos.

---

## 9. Offene Punkte, nächste Schritte, Termine

| Wann | Was |
|---|---|
| 14.10.2026 | Selbsttest des Startalarms auswerten (läuft automatisch beim nächsten Brennerstart) |
| 14.10.2026 | Zirkulation: Temperaturverlauf der ersten Nacht auswerten – schaltet die Pumpe nachts ab? |
| 15.–18.10.2026 | Vergleichstest: Startverzögerung mit stark verringerten Optolink-Abfragen – belastet der Bus die Regelung? |
| 02.11.2026 | Düsendurchsatz gegen die Tankmessung eichen (Wochensummen, Lieferungen herausrechnen) |
| offen | Sammelstörung: Ursache der Fehlmeldungen klären (Verdacht: Antwort eines anderen Datenpunkts falsch zugeordnet) |
| offen | Bedeutung von „Betriebsart (Rohwert)“ und „Raumtemperatur Soll“ klären |
| offen | Fehlerhistorie der Regelung über den Optolink lesen (Format noch nicht dekodiert) |
| offen | Halterung für den Kopf statt Klebeband |

---

## 10. Dateiübersicht

| Pfad | Inhalt |
|---|---|
| `README.md` | diese Übersicht |
| `docs/einbau.md` | Aufbau und Montage Schritt für Schritt |
| `docs/einmessen.md` | Inbetriebnahme, Adressprüfung, Ölverbrauchs-Abgleich |
| `docs/fehlersuche.md` | Fehlerbilder, Ursachen, Lösungen |
| `docs/verlauf.md` | Projektverlauf mit Datum |
| `firmware/heizung-optolink.yaml` | ESPHome-Konfiguration (Stand Builder) |
| `firmware/secrets.example.yaml` | Vorlage für die Secrets (ohne echte Werte) |
| `gehaeuse/optolink-gehaeuse.scad` | OpenSCAD-Quelltext aller Gehäuseteile |
| `gehaeuse/kopf.stl`, `kopf_deckel.stl`, `v_schluessel.stl` | Lesekopf mit Deckel und Führungs-V (Kopf Stand 11.10.) |
| `gehaeuse/esp.stl`, `esp_deckel.stl` | ESP32-Gehäuse mit Deckel |
| `gehaeuse/vorschau_*.png` | Renderbilder (Stand 08.10.) |
| `plaene/optolink-schaltplan.pdf` | Schaltplan Lesekopf + Anschlusstabelle + Lage im Kopf (A4, SFH 309) |
| `plaene/optolink_plan.svg` | dasselbe als SVG |
| `plaene/optolink_plan.py` | matplotlib-Skript, das den Plan erzeugt |
| `plaene/esp32-belegung.pdf` | Anschlussblatt Lesekopf + DS18B20 → ESP32-Stiftleiste (13.10.) |
| `plaene/esp32_belegung_plan.py` | matplotlib-Skript dazu |
| `plaene/ds18b20-zirkulation-plan.pdf` | Löt- und Anschlussplan des Zirkulationsfühlers (13.10.) |
| `plaene/ds18b20_plan.py` | matplotlib-Skript dazu |
| `.gitignore` | schließt Secrets, Build-Ordner und Sicherungskopien aus |

**Quellen:** openv-Wiki („Die Optolink-Schnittstelle“, „ESPHome-Optolink“, „Adressen“, `vito.scad`), VitoWiFi,
ESPHome-PR #4453.
