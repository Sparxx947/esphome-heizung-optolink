🇬🇧 [English version](README.en.md)

# Heizung · Optolink (Vitotronic 200 KW2 → ESPHome → Home Assistant)

Selbstbau-Lesekopf an der Optolink-Schnittstelle einer Viessmann-Ölheizung. Ein ESP32 mit ESPHome
liest Temperaturen, Brennerzustand, Brennerstunden und **Störmeldungen** aus der Regelung und gibt sie an
Home Assistant weiter. **Bewusst nur lesend** – die Firmware enthält nichts, was in die Regelung schreibt.

> Stand dieser Dokumentation: **08.10.2026**. Gerät geflasht und in HA, **Lesekopf noch nicht gelötet**
> (Fototransistor kommt Fr 09.10.). Alle Optolink-Werte stehen deshalb in HA noch auf `unknown`.

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
| **Was gemessen wird** | Brennerstörung (Anzeige **D1**), Sammelstörung, Brenner an/aus, Pumpen, Außen-/Kessel-/Warmwasser-/Vorlauftemperaturen inkl. Sollwerte, Brennerstarts, **Brennerstunden** |
| **Was gesteuert wird** | nichts (absichtlich) |
| **Ziel** | Push bei Brennerstörung (Anlass: Störung D1 am 03./04.10.2026 bei leerem Tank, die niemand bemerkt hat); Ölverbrauch aus Brennerstunden × Düsendurchsatz als Grundlage für eine Tankprognose |

**Prinzip:** Die Vitotronic hat vorn hinter einem „V“-förmigen Ausschnitt zwei Lämpchen – eine IR-Empfangsdiode
(links, rot) und eine IR-Sendediode (rechts, grün). Darüber spricht sie seriell im **KW-Protokoll (VS1), 4800 Baud 8E2**.
Der Lesekopf setzt mit Magneten darauf: eine **IR-LED** (940 nm) sendet in die linke Lampe, ein **Fototransistor**
empfängt von der rechten. Der ESP32 bedient beide über einen UART (RX GPIO16 / TX GPIO17) mit der ESPHome-Komponente
`optolink` aus **ESPHome-PR #4453** (noch nicht in ESPHome gemergt). Schaltung nach VitoWiFi/openv-Wiki.

---

## 2. Status (Stand 08.10.2026)

| Bereich | Status | Datum / Bemerkung |
|---|---|---|
| Konzept, Adressen, Schaltung | ✅ fertig | 04.10. – Adressen aus openv-Tabelle V200KW2, **noch nicht am Display geprüft** |
| Firmware (YAML) | ✅ fertig, kompiliert | 04.10. (RAM 28 %, Flash 50 %), unverändert seither |
| ESP32 geflasht, WLAN, HA | ✅ fertig | 06.10. ~19:40 – `192.168.178.193`, HA-Integration „Heizung“, 24 Entitäten |
| Feste IP im Router | ✅ fertig | 06.10. (DHCP-Reservierung, immer gleiche IP) |
| Im ESPHome Builder | ✅ fertig, online | 06.10. ~20:00 – Builder-Fassung ist ab jetzt **führend** |
| Gehäuse (SCAD/STL) | ✅ fertig | 06.10. Maße eingetragen, 07.10. Boden + Stützen korrigiert („passt jetzt so“, Jens) |
| Gehäuse gedruckt | ✅ gedruckt | 08.10. laut Jens (ob es exakt die Fassung vom 07.10. ist, ist nicht ausdrücklich bestätigt) |
| Lesekopf löten | ⏳ offen | Fototransistor kommt **Fr 09.10.**, Termin 09.10. 18:00 |
| Inbetriebnahme / Adressen prüfen | ⏳ offen | nach dem Löten, mit `optolink: logger: true` |
| HA-Automationen (Push, Ölverbrauch, Prognose) | ⏳ offen | erst nach erfolgreicher Inbetriebnahme |

---

## 3. Stückliste

Preise und ASINs zum Zeitpunkt der Bestellung (Amazon.de, Oktober 2026).

| Teil | Menge | Bezeichnung / Typ | Bezugsquelle, ASIN, Preis | Status |
|---|---|---|---|---|
| Mikrocontroller | 1 | **ESP32-WROOM-32U DevKitC V4**, USB-C, CP2102, IPEX-Antennenbuchse; Platine 48,24 × 28,15 mm | Amazon **B0F6567LB5**, 13,99 € (2 Stück bestellt, der zweite ist die Tankmessung) | ✅ geliefert 06.10., geflasht |
| Antenne | 1 | 2,4-GHz-Antenne mit IPEX→SMA-Pigtail (SMA-Buchse Ø ~6,4 mm, 1/4″) | im Antennen-Kit des ESP32 enthalten | ✅ vorhanden |
| IR-LED | 1 (+ Reserve) | **Chanzon** IR-LED 940 nm, 3 mm, 100 Stück (Ersatz für SFH487 / SIR 204 aus dem openv-Wiki) | Amazon **B01BVEKXNC**, 7,99 € | ✅ bestellt 04.10., Zustellung 06.10. angekündigt (Eingang nicht ausdrücklich notiert) |
| Fototransistor | 1 (+ Reserve) | **Kingbright L-93DP3C**, 3 mm, 940 nm, 5 Stück (Ersatz für SFH309FA) | Amazon **B01M3PGVRC**, 9,77 € (Marketplace) | ⏳ bestellt, Lieferung **Fr 09.10.** |
| Widerstand | 1 | 220 Ω (Vorwiderstand IR-LED) | AZ-Delivery-Widerstandssortiment | ✅ vorhanden |
| Widerstand | 1 | 10 kΩ (Pull-up Fototransistor) | AZ-Delivery-Widerstandssortiment | ✅ vorhanden |
| Magnete | 4 | Neodym-Scheibenmagnet **10 × 3 mm** (2 im Lesekopf, 2 im Boden des ESP-Gehäuses) | Amazon, Delaga, 50 Stück, 7,99 € | ✅ bestellt 04.10., Zustellung 06.10. angekündigt |
| Verbindungskabel | 4 | Dupont-Jumper **Buchse–Buchse** (F2F), Farbvorschlag rot/schwarz/gelb/grün | ELEGOO-Jumper-Set M2M/F2M/F2F (40 × 20 cm) | ✅ vorhanden |
| Stromversorgung | 1 | USB-C-Kabel + USB-Netzteil 5 V | – | ❓ **nicht in den Notizen** – vermutlich vorhanden, vor Einbau klären |
| Filament | ~20 g (geschätzt) | **PETG** (Wärme am Kessel) | vorhanden | ✅ vorhanden, Gehäuse gedruckt 08.10. |
| Kleber | wenig | Heißkleber (Platine auf Stützen fixieren, optional) bzw. Sekundenkleber für V-Schlüssel (optional) | vorhanden (angenommen) | ✅ |
| Schrauben | 0 | keine – Steckdeckel und Magnete | – | – |
| Werkzeug | – | Lötkolben, Multimeter (Diodentest), Messschieber, 3D-Drucker | vorhanden | ✅ |

Nicht verwendet, aber verwechslungsgefährdet: Das **AZ-Delivery-LED-Sortiment** ist sichtbares Licht und für Optolink
unbrauchbar. Das **ESP32-CAM-Set** (mit MB-Board) bleibt unangetastet – es war ursprünglich vorgesehen, wurde am
04.10. aber zugunsten eines neuen ESP32 verworfen.

Original-Bauteile laut openv/VitoWiFi: IR-LED **SFH487** (bzw. SIR 204 EVL), Fototransistor **SFH309FA** – bei Amazon
nicht erhältlich, bei Problemen als Tausch bei Reichelt möglich.

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
| Fototransistor L-93DP3C | Emitter → GND | **Kollektor** → GPIO16 + 10 kΩ | Kingbright-Datenblatt (DSAC1289), geprüft 06.10. |

Der Ausdruck nennt beim Fototransistor noch „meist kurzes Bein – prüfen!“; das ist inzwischen per Datenblatt bestätigt.
Trotzdem vor dem Löten mit dem Diodentest des Multimeters gegenprüfen. Falsch herum geht nichts kaputt, es kommen
nur keine Daten.

**Lage im Kopf** (Blick **auf** die Regelung = Blick auf die Rückseite des Kopfs beim Löten):

| Position | Lampe der Regelung | Funktion der Regelung | Unser Bauteil |
|---|---|---|---|
| links | rot („Störung“) | IR-Empfänger | **IR-LED** |
| rechts | grün („Betrieb“) | IR-Sender | **Fototransistor** |

Abstand der Lampen Mitte–Mitte: **14,4 mm** (Jens gemessen 06.10.; openv-Wiki nennt 14 mm).
Im Kopf ist innen „LED“, „FT“ und „OBEN“ eingeprägt.

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
| Logger | `level: INFO`; UART0 bleibt für das USB-Log frei |
| API | verschlüsselt (`heizung_api_key`) |
| OTA | `platform: esphome`, ohne eigenes Passwort (abgesichert über den API-Schlüssel) |
| Fallback-Hotspot | SSID `Heizung-Fallback`, Passwort aus Secret, mit Captive Portal |

### Entitäten in Home Assistant (24)

Gerät „Heizung“ in der ESPHome-Integration. Die Entity-IDs ergeben sich nach ESPHome-Muster aus
`friendly_name` + Name (z. B. vermutlich `sensor.heizung_brennerstunden`) – **in HA nicht nachgesehen**.

| Name | Typ | Adresse | Format | Intervall |
|---|---|---|---|---|
| Brennerstörung (= Anzeige D1) | binär, problem | `0x0883` | 0/1 | 15 s |
| Sammelstörung | binär, problem | `0x0847` | 0/1 | 15 s |
| Brenner (1. Stufe) | binär, running | `0x0842` | 0/1 | 15 s |
| Speicherladepumpe | binär, running | `0x0845` | 0/1 | 60 s |
| Zirkulationspumpe | binär, running | `0x0846` | 0/1 | 60 s |
| Heizkreispumpe | binär, running | `0x2906` | 0/1 | 60 s |
| Außentemperatur | °C | `0x0800` | 2 B ÷ 10, vorzeichenbehaftet | 120 s |
| Außentemperatur gedämpft | °C | `0x5527` | 2 B ÷ 10, vorzeichenbehaftet | 600 s |
| Kesseltemperatur | °C | `0x0802` | 2 B ÷ 10 | 60 s |
| Kesselsolltemperatur | °C | `0x555A` | 2 B ÷ 10 | 120 s |
| Warmwassertemperatur (Speicher) | °C | `0x0804` | 2 B ÷ 10 | 120 s |
| Vorlauftemperatur (Sensor 17B) | °C | `0x080C` | 2 B ÷ 10 | 120 s |
| Vorlaufsolltemperatur (A1M1) | °C | `0x2544` | 2 B ÷ 10 | 300 s |
| Abgastemperatur (nur mit Abgasfühler sinnvoll) | °C, Diagnose | `0x0808` | 2 B ÷ 10 | 300 s |
| Brennerstarts | Zähler | `0x088A` | 4 B | 300 s |
| Brennerstunden (Stufe 1) | h, total_increasing | `0x08A7` | 4 B, Sekunden ÷ 3600 | 300 s |
| Ölverbrauch Regelung | Diagnose | `0x7574` | 4 B ÷ 1000 – **Bedeutung unklar**, erst beobachten | 1800 s |
| Betriebsart (Rohwert) | Diagnose | `0x2301` | 1 B | 600 s |
| Raumtemperatur Soll | °C, Diagnose | `0x2306` | 1 B | 600 s |
| Optolink-Warteschlange | Diagnose | – | `QUEUE_SIZE` | 60 s |
| Gerätekennung | Text, Diagnose | – | `DEVICE_INFO` | 1800 s |
| Optolink-Status | Text, Diagnose | – | `STATE_INFO` | 30 s |
| WLAN-Signal | dBm | – | – | 120 s |
| Laufzeit | s | – | – | 600 s |

Alle Adressen stammen aus der openv-Tabelle „Adressen“, Spalte V200KW2/KW1, und sind **noch nicht** gegen das
Display der Regelung geprüft.

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
4. **Aufsetzen:** Kopf mit dem V in den Ausschnitt der Regelung, ESP-Gehäuse magnetisch ans Kesselblech, USB-Strom.
5. **Prüfen:** Log zeigt Antworten, „Optolink-Status“ verlässt `unknown`, Gerätekennung `0x2098`(?);
   Kessel- und Außentemperatur mit dem Display vergleichen.
6. **Abschließen:** `logger: false`, erneut OTA; HA-Automationen anlegen (Abschnitt 8).

---

## 8. Home-Assistant-Anbindung

Im Repo liegen **keine HA-Pakete** (`ha/` gibt es hier nicht) – die Automationen sind noch nicht angelegt.
Geplant (Stand 04.–08.10.):

| Vorhaben | Grundlage | Status |
|---|---|---|
| Push bei **Brennerstörung** und **Sammelstörung** an die Hausbewohner | `binary_sensor` Brennerstörung / Sammelstörung → `on` | ⏳ geplant |
| Ölverbrauch | Brennerstunden × Düsendurchsatz (≤ 2,4 l/h), an Liefermengen eichen → [`docs/einmessen.md`](docs/einmessen.md) | ⏳ geplant |
| Tankprognose / Warnung | Vorwarnung bei **1.500 l**, dringend bei **800 l** | ⏳ geplant |

**Wichtig für die Automationen:** Ohne Kopf bzw. ohne Verbindung melden die Optolink-Binärsensoren `unknown`, nicht
`off`. Eine Automation „Brennerstörung = aus → alles gut“ würde sonst falsch beruhigen. Auch `unknown`/`unavailable`
über längere Zeit sollte gemeldet werden (Vorschlag, nicht umgesetzt).

Die parallele Füllstandsmessung am Erdtank (pneumatisch, ESP32 „Öltank“ `.194`) ist ein **eigenes Projekt** und
nicht Teil dieses Repos.

---

## 9. Offene Punkte, nächste Schritte, Termine

| Wann | Was | Wer |
|---|---|---|
| **Fr 09.10.2026, 18:00** | Fototransistor da → Lesekopf löten, aufsetzen, Inbetriebnahme mit `logger: true` | Jens |
| beim Einbau | Klären, ob „Gehäuse passt“ (07.10.) nach Druck oder nach Vorschau galt – gedruckt wurde laut Jens am 08.10. | Jens |
| nach dem Löten | Adressen gegen das Display prüfen (v. a. Außen-, Kessel-, Warmwassertemperatur, Brennerzustand) | Jens + Claude |
| nach dem Löten | WLAN-Signal im Keller am Einbauort ablesen (am PC −47 dBm; Testling am Kessel 04.10. −41/−42 dBm) | – |
| danach | Bedeutung von „Ölverbrauch Regelung“ (`0x7574`) und „Betriebsart (Rohwert)“ beobachten | – |
| danach | HA: Push bei Störung, Ölverbrauch, Tankprognose | Claude |
| danach | Startwert für den Ölverbrauch erst nach der Peilung am Tank festlegen (Inhalt seit 05.10. vermutlich ~1.900 l, **unbestätigt**) | Jens |
| offen | Stromversorgung (USB-Netzteil, Kabelweg) am Kessel klären | Jens |
| bei Bedarf | Bei schlechtem Empfang: Bauteile gegen SFH309FA / SFH487 (Reichelt) tauschen | – |

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
| `gehaeuse/kopf.stl`, `kopf_deckel.stl`, `v_schluessel.stl` | Lesekopf mit Deckel und Führungs-V |
| `gehaeuse/esp.stl`, `esp_deckel.stl` | ESP32-Gehäuse mit Deckel |
| `gehaeuse/vorschau_*.png` | Renderbilder |
| `plaene/optolink-schaltplan.pdf` | Schaltplan + Anschlusstabelle + Lage im Kopf (A4) |
| `plaene/optolink_plan.svg` | dasselbe als SVG |
| `plaene/optolink_plan.py` | matplotlib-Skript, das den Plan erzeugt (Ausgabepfade darin sind lokal) |
| `.gitignore` | schließt Secrets, Build-Ordner und Sicherungskopien aus |

**Quellen:** openv-Wiki („Die Optolink-Schnittstelle“, „ESPHome-Optolink“, „Adressen“, `vito.scad`), VitoWiFi,
ESPHome-PR #4453.
