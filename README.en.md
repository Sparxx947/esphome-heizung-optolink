🇩🇪 [Deutsche Version](README.md)

# Heating · Optolink (Vitotronic 200 KW2 → ESPHome → Home Assistant)

DIY read head on the Optolink interface of a Viessmann oil-fired boiler. An ESP32 running ESPHome
reads temperatures, burner state, burner hours and **fault messages** from the controller and passes them on to
Home Assistant. **Deliberately read-only** – the firmware contains nothing that writes to the controller.

> State of this documentation: **13.10.2026**. **In operation since 12.10.2026**: the read head sits on the controller,
> the ESP32 reads all values and passes them on to Home Assistant. Since 13.10. an additional **DS18B20** measures the
> temperature of the circulation pipe.

> **Rebuilding:** Create your own secrets from the template [`firmware/secrets.example.yaml`](firmware/secrets.example.yaml)
> (Wi-Fi, API key, hotspot password) and adapt the fixed IP to your own network. The addresses in the
> firmware apply to the Vitotronic 200 KW2 – for other Viessmann controllers they can be found in the
> [openv wiki](https://github.com/openv/openv/wiki) (page "Adressen" / addresses).

---

## 1. Summary

| | |
|---|---|
| **System** | Oil boiler Viessmann **Vitola 111** (with integrated hot-water tank), controller **Vitotronic 200 type KW2** (weather-compensated, device ID `0x2098`), burner Viessmann VEA I-2 (built 1999, max. 2.0 kg/h ≈ 2.4 l/h) |
| **Location** | Boiler room in the basement, read head at the front left on the "V" of the controller, ESP enclosure magnetically attached to the boiler sheet metal |
| **What is measured** | Burner fault (display **D1**), general fault, burner enable signal, pumps, outdoor/boiler/hot-water/flow temperatures, boiler and hot-water setpoint, heating curve, burner starts, **burner hours**; plus, via DS18B20, the **circulation (return)** |
| **What is controlled** | nothing (on purpose) |
| **Goal** | Push notification on burner fault (trigger: fault D1 on 03./04.10.2026 with an empty tank, which nobody noticed); oil consumption from burner hours × nozzle throughput as the basis for a tank forecast |

**Principle:** Behind a "V"-shaped cut-out at the front, the Vitotronic has two small lamps – an IR receiving diode
(left, red) and an IR transmitting diode (right, green). Through them it talks serially using the **KW protocol (VS1), 4800 baud 8E2**.
The read head sits in front of them: an **IR LED** (940 nm) transmits into the left lamp, a **phototransistor**
receives from the right one. The ESP32 drives both via a UART (RX GPIO16 / TX GPIO17) using the ESPHome component
`optolink` from **ESPHome PR #4453** (not yet merged into ESPHome). Circuit according to VitoWiFi/openv wiki.

---

## 2. Status (as of 13.10.2026)

| Area | Status | Date / remark |
|---|---|---|
| Concept, circuit | ✅ done | 04.10. |
| Addresses | ✅ checked on the system | 11.10. – address scan; three addresses from the openv table did not fit (see section 6) |
| Firmware (YAML) | ✅ in operation | as of 13.10. (RAM 28.5 %, flash 50.9 %) |
| ESP32, Wi-Fi, HA | ✅ in operation | `192.168.178.193`, HA integration "Heizung" (heating), 29 entities |
| Enclosure | ✅ printed | ESP enclosure 07./08.10.; read head reprinted on 11.10. (windows were 2.4 mm too high) |
| Read head | ✅ in operation | soldered 10.10. (SFH 309), first response from the controller 11.10., on the ESP32 since 12.10. |
| Bus load | ✅ relieved | 12.10. – polling intervals reduced, queue mostly 0–3 |
| HA: push on burner fault | ✅ active | after 5 min of fault to all household members, with announcement |
| HA: oil consumption from burner runtime | ✅ active, **not calibrated** | since 12.10.; nozzle throughput 2.4 l/h = nameplate maximum, calibration against the tank measurement planned |
| HA: start delay + start alarm | ✅ active | 12.10. – push if the burner has not started 45 min after the enable signal |
| Circulation sensor DS18B20 | ✅ in operation | 13.10. – GPIO4, first value 46.6 °C with the pump running |
| General fault | ⚠️ with filter | 13.10. – reported "on" briefly ~20× without a fault at the controller; now only reports after 30 min |

---

## 3. Bill of materials

Prices and ASINs at the time of ordering (Amazon.de, October 2026).

| Part | Qty | Designation / type | Source, ASIN, price | Status |
|---|---|---|---|---|
| Microcontroller | 1 | **ESP32-WROOM-32U DevKitC V4**, USB-C, CP2102, IPEX antenna connector; board 48.24 × 28.15 mm | Amazon **B0F6567LB5**, 13.99 € (2 pieces ordered, the second one is for the tank level measurement) | ✅ delivered 06.10., flashed |
| Antenna | 1 | 2.4 GHz antenna with IPEX→SMA pigtail (SMA socket Ø ~6.4 mm, 1/4″) | included in the ESP32's antenna kit | ✅ available |
| IR LED | 1 (+ spare) | **Chanzon** IR LED 940 nm, 3 mm, 100 pieces (replacement for SFH487 / SIR 204 from the openv wiki) | Amazon **B01BVEKXNC**, 7.99 € | ✅ ordered 04.10., delivery announced for 06.10. (receipt not explicitly noted) |
| Phototransistor | 1 | **Osram SFH 309**, 3 mm clear (installed) | local electronics shop, 10.10. | ✅ installed 10.10. |
| (Phototransistor) | – | Kingbright L-93DP3C, 3 mm, 940 nm (originally ordered) | Amazon **B01M3PGVRC**, 9.77 € (Marketplace) | ❌ did not arrive in time, not used |
| Resistor | 1 | 220 Ω (series resistor IR LED) | AZ-Delivery resistor assortment | ✅ available |
| Resistor | 1 | 10 kΩ (pull-up phototransistor) | AZ-Delivery resistor assortment | ✅ available |
| Magnets | 4 | Neodymium disc magnet **10 × 3 mm** (2 in the read head, 2 in the floor of the ESP enclosure) | Amazon, Delaga, 50 pieces, 7.99 € | ✅ fitted – **ineffective on the head** (the controller's front is plastic), head fixed with adhesive tape |
| Temperature sensor | 1 | **DS18B20** waterproof, stainless-steel sleeve, 3 wires, 2 m cable (pack of 5) | Amazon **B0HG8Y9X45**, 10.49 € | ✅ installed 13.10. |
| Resistor | 1 | 4.7 kΩ (pull-up DS18B20, yellow-violet-red) | resistor assortment | ✅ installed 13.10. |
| Connector | 1 | Wago terminal (3V3 for the read head **and** the sensor, the DevKitC has only one 3V3 pin) | available | ✅ |
| Connecting wires | 4 | Dupont jumpers **female–female** (F2F), suggested colours red/black/yellow/green | ELEGOO jumper set M2M/F2M/F2F (40 × 20 cm) | ✅ available |
| Power supply | 1 | USB-C cable + USB power supply 5 V | available | ✅ in operation since 12.10. (sensor "Neustart-Grund" (reset reason) shows undervoltage as "Brownout") |
| Filament | ~20 g (estimated) | **PETG** (heat near the boiler) | available | ✅ available, enclosure printed 08.10. |
| Adhesive | a little | Hot glue (fix the board on the supports, optional) or superglue for the V key (optional) | available (assumed) | ✅ |
| Screws | 0 | none – push-fit lids and magnets | – | – |
| Tools | – | Soldering iron, multimeter (diode test), calipers, 3D printer | available | ✅ |

Not used, but easily confused: the **AZ-Delivery LED assortment** is visible light and useless for Optolink.
The **ESP32-CAM set** (with MB board) remains untouched – it was originally intended, but was dropped on
04.10. in favour of a new ESP32.

Original components according to openv/VitoWiFi: IR LED **SFH487** (or SIR 204 EVL), phototransistor **SFH309FA**. Installed is
the **SFH 309** (clear lens, without daylight filter) – it works because the head shields the ambient light.

---

## 4. Pinout and wiring

Circuit diagram for printing: [`plaene/optolink-schaltplan.pdf`](plaene/optolink-schaltplan.pdf)
(SVG: [`plaene/optolink_plan.svg`](plaene/optolink_plan.svg), generator: [`plaene/optolink_plan.py`](plaene/optolink_plan.py)).

```
3,3 V ── 220 Ω ── IR-LED (Anode) │ Kathode ── GPIO17 (TX)
3,3 V ── 10 kΩ ──┬── GPIO16 (RX)
                 └── Kollektor Fototransistor │ Emitter ── GND
```

(Diagram labels: `Kathode` = cathode, `Kollektor Fototransistor` = phototransistor collector.)

**The resistors sit inside the read head**, only four wires go to the ESP:

| Wire | ESP32 pin (silkscreen) | Connected in the read head to | Suggested colour |
|---|---|---|---|
| 1 | `3V3` | 220 Ω (to the LED anode) **and** 10 kΩ (to the PT collector) | red |
| 2 | `GND` | Emitter of the phototransistor | black |
| 3 | `GPIO17` / "TX2" / "17" | Cathode of the IR LED | yellow |
| 4 | `GPIO16` / "RX2" / "16" | Collector of the phototransistor + 10 kΩ | green |

**Legs:**

| Component | Long leg | Short leg | Source |
|---|---|---|---|
| IR LED (Chanzon) | Anode (+) → 220 Ω | Cathode (flat side) → GPIO17 | usual LED convention |
| Phototransistor SFH 309 (installed) | Emitter → GND | **Collector** (flattened side) → GPIO16 + 10 kΩ | Osram datasheet ("Package marking: Collector") |
| Phototransistor L-93DP3C (alternative) | Emitter → GND | **Collector** → GPIO16 + 10 kΩ | Kingbright datasheet (DSAC1289) |

Double-check with the multimeter before soldering. **On 10.10. the IR LED was soldered in with reversed polarity and the LED series
resistor was 220 kΩ instead of 220 Ω** (colour bands red-red-**yellow** instead of red-red-**brown**) – the two together cost an evening.
Getting it the wrong way round breaks nothing, you just get no data.

**Position in the head** (looking **at** the controller = looking at the back of the head while soldering):

| Position | Controller lamp | Function in the controller | Our component |
|---|---|---|---|
| left | red ("Störung" / fault) | IR receiver | **IR LED** |
| right | green ("Betrieb" / operation) | IR transmitter | **Phototransistor** |

Distance between the lamps centre to centre: **14.4 mm** (measured by Jens 06.10.; the openv wiki states 14 mm).
Inside the head, "LED", "FT" (phototransistor) and "OBEN" (top) are embossed.

**Height:** The tip of the controller's V lies **3.5 mm below**, the upper edge of the V **6.2 mm above** the centre of the lamps (measured
11.10.). With the first head the windows were 2.4 mm too high – the controller only responded once the head was moved
down. Corrected via `v_versatz_y = 0.9` in the SCAD.

> **The red lamp is also the controller's fault indicator.** With the head attached it is covered. A fault
> can then be recognised on the display ("Störung" (fault) flashes, the ⓘ button shows the code) – or in Home Assistant.

### Addition: circulation sensor DS18B20 (since 13.10.)

Plan for printing: [`plaene/ds18b20-zirkulation-plan.pdf`](plaene/ds18b20-zirkulation-plan.pdf)
(generator [`plaene/ds18b20_plan.py`](plaene/ds18b20_plan.py)). Pin assignment of the read head on the ESP32:
[`plaene/esp32-belegung.pdf`](plaene/esp32-belegung.pdf) (as of 12.10., without the sensor).

| Sensor wire | ESP32 pin | Remark |
|---|---|---|
| red | `3V3` via Wago | the DevKitC has only **one** 3V3 pin – the read head and the sensor share it |
| black | `GND` (right row, 7th from the top) | |
| yellow | `GPIO4` (right row, 13th from the top, directly below 16) | 4.7 kΩ between yellow and red, soldered in at the cable end |

The sensor lies flat on the circulation pipe (return from the house to the tank) near the circulation pump,
fixed with cable ties and under the pipe insulation. Purpose: detect when the circulation is running (warm) and when
not (cooling down) – the controller does report the pump itself (`0x0846`), but not whether water is actually flowing.

---

## 5. Enclosure

Source: [`gehaeuse/optolink-gehaeuse.scad`](gehaeuse/optolink-gehaeuse.scad) (OpenSCAD, parametric; select the part via
`TEIL = "…"`). Geometry of the head based on `vito.scad` from the openv wiki.

| STL | Purpose | Dimensions (from SCAD) | Print orientation |
|---|---|---|---|
| [`kopf.stl`](gehaeuse/kopf.stl) | Read head: front plate 4 mm with two windows Ø 3.2 mm (14.4 mm apart), collar stop for the component bases, 2 magnet pockets 10.3 × 3.2 mm (0.6 mm remaining wall to the front), 12 mm cavity for resistors, cable outlet 7 × 4 mm at the top | Ø 34 mm, 16 mm deep | **front on the bed** |
| [`kopf_deckel.stl`](gehaeuse/kopf_deckel.stl) | Rear lid with push-fit collar and cable outlet for 4 strands | Ø 34 mm | flat |
| [`v_schluessel.stl`](gehaeuse/v_schluessel.stl) | Guide "V", plugged into the front with a 2 mm peg (glued if necessary) and engages the "V" of the controller (protrudes 6 mm, max. 8 permitted) | web 1.6 mm | upright |
| [`esp.stl`](gehaeuse/esp.stl) | Enclosure for the ESP32: USB-C on the left end face, SMA hole Ø 6.6 on the right **below** the board, Dupont outlet 12 × 6 mm at the bottom of the side, ventilation slots, 2 magnet pockets in the floor, embossing "HEIZUNG" (heating) | outside approx. 55.5 × 33.8 × 31 mm, inside 51.5 × 29.8 mm | floor on the bed |
| [`esp_deckel.stl`](gehaeuse/esp_deckel.stl) | Push-fit lid | – | flat |

**Addendum 11.10.:** The windows in the first head were 2.4 mm too high (`v_versatz_y` was −1.5, correct is **0.9**);
`kopf.stl` has been regenerated. The preview images still show the old state. The **magnets in the head do not hold** – the
front of the Vitotronic is made of plastic. The head is fixed with adhesive tape in the working position.

Previews: [`vorschau_alle.png`](gehaeuse/vorschau_alle.png), [`vorschau_esp.png`](gehaeuse/vorschau_esp.png),
[`vorschau_kopf_vorn.png`](gehaeuse/vorschau_kopf_vorn.png), [`vorschau_kopf_hinten.png`](gehaeuse/vorschau_kopf_hinten.png).

**Print settings:** PETG (close to the boiler), 0.2 mm layer height, 3 walls, **no supports**.

**Assembling the ESP enclosure:** The board rests with its two end faces on **four supports** (two per end face,
17 mm high, approx. 4.9 mm wide, 4.5 mm deep), which stand **between the pin headers**: 3.2 mm from the long edge,
12 mm free in the middle (that is where the USB solder tabs and the SMA nut sit). Fix with hot glue if needed.
Below the board there is room for the downward-pointing pins and the Dupont sockets. Push the SMA socket through
the hole from the inside, nut on the outside. One magnet into each of the two floor pockets (from below), two into the head (from behind).

**Lessons from the failed prints** (details in [`docs/verlauf.en.md`](docs/verlauf.en.md)):

| Fault | Cause | Correction |
|---|---|---|
| SMA hole would have been blocked (06.10.) | was located behind the right-hand board support | hole moved below the board (`sma_z = 8`), 12 mm gap for the nut |
| Magnet pockets went through the floor (07.10.) | pocket 3.2 mm deep in a 2.0 mm floor | `boden = 4.0` → 0.8 mm remaining wall |
| Board rested on the pins (07.10.) | pin headers run along the **entire** board length (19 × 2.54 = 48.3 mm); continuous supports blocked the pins | 4 individual supports between the pin rows |

Rule derived from this: before every STL export, check every pocket against the wall thickness and the underside of the board
(pin headers, sockets, solder tabs) against every support; have critical dimensions measured beforehand.

---

## 6. Firmware

File: [`firmware/heizung-optolink.yaml`](firmware/heizung-optolink.yaml) – matches the state in the ESPHome Builder.

| Setting | Value |
|---|---|
| Device name / hostname | `heizung-optolink` → `heizung-optolink.local` |
| Display name (`friendly_name`) | `Heizung` (heating) |
| IP | **192.168.178.193** (fixed DHCP reservation in the FRITZ!Box) |
| Board / framework | `esp32dev`, **Arduino** (mandatory for the Optolink component) |
| External component | `github://pr#4453`, component `optolink` |
| Optolink | `protocol: KW`, `rx_pin: GPIO16`, `tx_pin: GPIO17`, `logger: false` (`true` for commissioning) |
| 1-Wire | `GPIO4`, one DS18B20 (`dallas_temp`, without a fixed address – only one sensor on the bus) |
| Logger | `level: INFO`; UART0 stays free for the USB log |
| API | encrypted (`heizung_api_key`) |
| OTA | `platform: esphome`, without its own password (secured via the API key) |
| Fallback hotspot | SSID `Heizung-Fallback`, password from secret, with captive portal |

### Entities in Home Assistant (29)

Device "Heizung" (heating) in the ESPHome integration, entity IDs `sensor.heizung_…` / `binary_sensor.heizung_…`
(e.g. `sensor.heizung_brennerstunden`, `sensor.heizung_zirkulation_rucklauf`). Some entities added later
were given the area prefix by HA (`…heizungskeller_heizung_…`).

| Name | Type | Address | Format | Interval | Finding |
|---|---|---|---|---|---|
| Brennerstörung (burner fault, = display D1) | binary, problem | `0x0883` | 0/1 | 120 s | ✅ |
| Sammelstörung (general fault) | binary, problem, **`delayed_on: 30min`** | `0x0847` | 0/1 | 120 s | ⚠️ false reports, see [troubleshooting](docs/fehlersuche.en.md) |
| Brenner (burner) | binary, running | `0x0842` | 0/1 | 30 s | ✅ – **enable signal from the controller, not flame** |
| Speicherladepumpe (tank charging pump) | binary, running | `0x0845` | 0/1 | 120 s | ✅ |
| Zirkulationspumpe (circulation pump) | binary, running | `0x0846` | 0/1 | 120 s | ✅ |
| Heizkreispumpe (A1) (heating circuit pump, A1) | binary, running | `0x2906` | 0/1 | 1800 s | always off – heating circuit without mixer not used |
| Heizkreispumpe M2 (heating circuit pump M2) | binary, running | `0x3906` | 0/1 | 120 s | ✅ – the heating circuit in use |
| Zirkulation Rücklauf (circulation return) | °C (DS18B20) | GPIO4 | – | 60 s | ✅ 13.10. |
| Außentemperatur (outdoor temperature) | °C | `0x0800` | 2 B ÷ 10, signed | 120 s | ✅ |
| Außentemperatur gedämpft (outdoor temperature, damped) | °C | `0x5527` | 2 B ÷ 10, signed | 600 s | ✅ |
| Kesseltemperatur (boiler temperature) | °C | `0x0802` | 2 B ÷ 10 | 60 s | ✅ |
| Kesselsolltemperatur (boiler setpoint) | °C | **`0x5502`** | 2 B ÷ 10 | 300 s | ✅ (`0x555A` from the table returns FF FF here) |
| Warmwassertemperatur (Speicher) (hot-water temperature, tank) | °C | `0x0804` | 2 B ÷ 10 | 120 s | ✅ |
| Vorlauftemperatur (Sensor 17B) (flow temperature, sensor 17B) | °C | `0x080C` | 2 B ÷ 10 | 120 s | ✅ |
| Warmwasser-Solltemperatur (hot-water setpoint) | °C | `0x6300` | 1 B, filter 30–95 °C | 600 s | ✅ (first value after a restart was once 5 instead of 55) |
| Abgastemperatur (flue gas temperature) | °C, diagnostic | `0x0808` | 2 B ÷ 10 | 1800 s | no flue gas sensor fitted – constant value |
| Brennerstarts (burner starts) | counter | `0x088A` | 4 B | 60 s | ✅ |
| Brennerstunden (Stufe 1) (burner hours, stage 1) | h, total_increasing | `0x08A7` | 4 B, seconds ÷ 3600 | 60 s | ✅ |
| Ölverbrauch Regelung (oil consumption, controller) | diagnostic | `0x7574` | 4 B ÷ 1000 | 1800 s | always 0 – not kept by this KW2 |
| Heizkurve Neigung (heating curve slope) | diagnostic | `0x2305` | 1 B ÷ 10 | 1800 s | ✅ (1.4) |
| Heizkurve Niveau (heating curve level) | K, diagnostic | `0x2304` | 1 B, signed | 1800 s | ✅ (0) |
| Betriebsart (Rohwert) (operating mode, raw value) | diagnostic | `0x2301` | 1 B | 600 s | mapping open |
| Raumtemperatur Soll (room temperature setpoint) | °C, diagnostic | `0x2306` | 1 B | 600 s | implausible – mapping open |
| Optolink-Warteschlange (Optolink queue) | diagnostic | – | `QUEUE_SIZE` | 60 s | |
| Gerätekennung (device ID) | text, diagnostic | – | `DEVICE_INFO` | 1800 s | ✅ `Device ID: 2098` |
| Optolink-Status (Optolink status) | text, diagnostic | – | `STATE_INFO` | 30 s | |
| Neustart-Grund (reset reason) | text, diagnostic | – | `debug: reset_reason` | 3600 s | after OTA "software via esp_restart" |
| WLAN-Signal (Wi-Fi signal) | dBm | – | – | 120 s | |
| Laufzeit (uptime) | s | – | – | 600 s | |

✅ = value plausible (address scan 11.10., in operation since 12.10.); not every value was compared individually with the display.

Removed on 11.10.: **Vorlaufsolltemperatur** (flow setpoint) (`0x2544` or `0x3544` return FF FF on this KW2).

**Bus load:** In the KW protocol at 4800 baud, the Optolink manages about **17 reads per minute**. The first
version requested ~21 – the queue stood at 18–22, there were timeouts. Since 12.10. it is
~9 per minute by calculation (intervals in the table), the queue is mostly at 0–3, briefly higher directly after a
restart. The DS18B20 is on its own bus and does not load the Optolink.

### Secrets

[`firmware/secrets.example.yaml`](firmware/secrets.example.yaml) is only a template with the key names
`wifi_ssid`, `wifi_password`, `heizung_api_key`, `heizung_ap_password`. **Real values exist only in the ESPHome Builder**
(its `secrets.yaml`), never in the repo – `.gitignore` excludes `secrets.yaml` and `secrets.*.yaml`.
Generate an API key: `openssl rand -base64 32`.

### Flashing

| Method | When | How |
|---|---|---|
| **Builder, OTA** (normal case) | every change | edit the YAML in the ESPHome Builder → **INSTALL → Wirelessly** |
| **USB** (first flash / emergency) | blank board, device no longer on Wi-Fi | `esphome run heizung-optolink.yaml --no-logs --device /dev/ttyUSB0` with **real** secrets (e.g. via the podman image `ghcr.io/esphome/esphome`) |
| OTA from the PC (fallback) | Builder not available | `esphome run … --no-logs --device 192.168.178.193` with real secrets in a temporary `secrets.yaml`, delete it afterwards |

> **Trap (happened 06.10.):** Never flash a test build with dummy secrets – the device then gets the wrong
> hotspot password and the wrong API key. And `esphome upload` **does not recompile**, but uploads the
> last build from `.esphome/`. For real firmware always use `esphome run`, watch for "Successfully compiled" and
> afterwards verify via the API with the real key.

The Builder is the authoritative version. If something is changed there, update this file accordingly (and vice versa).

---

## 7. Instructions

In detail in separate files:

- [`docs/einbau.en.md`](docs/einbau.en.md) – assembling the read head, fitting out the enclosure, mounting on the boiler
- [`docs/einmessen.en.md`](docs/einmessen.en.md) – commissioning, checking addresses against the display, calibrating oil consumption from burner hours
- [`docs/fehlersuche.en.md`](docs/fehlersuche.en.md) – known failure patterns with cause and solution

### Short version

1. **Soldering:** IR LED left, phototransistor right (looking at the back of the head, "OBEN" (top) at the top), check the legs
   beforehand with the diode test, resistors inside the head, 4 Dupont strands through the cable outlet.
2. **Enclosure:** insert the magnets, plug the V key into the front, ESP onto the supports, antenna onto the SMA.
3. **Firmware:** in the Builder set `optolink:` → `logger: true`, **INSTALL → Wirelessly**.
4. **Attach:** head with the V into the cut-out of the controller, **secure with adhesive tape** (the magnets do not hold on
   the plastic front), ESP enclosure magnetically onto the boiler sheet metal, USB power.
5. **Check:** log shows responses, "Optolink-Status" leaves `unknown`, device ID `Device ID: 2098`;
   compare boiler and outdoor temperature with the display. If nothing arrives: move the head **vertically**.
6. **Finish:** `logger: false`, OTA again; create HA automations (section 8).

---

## 8. Home Assistant integration

The repo contains **no HA packages** – everything has been created in the HA user interface (UI helpers and automations).

| Plan | Implementation | Status |
|---|---|---|
| Push on **burner fault** | Brennerstörung `on` for 5 min → message to all household members (all channels) with announcement and the latest oil level from the tank measurement | ✅ active |
| Push on **general fault** | – | ❌ deliberately not: the address occasionally delivers false reports |
| **Oil consumption** | `input_number` "Öl-Düsendurchsatz" (oil nozzle throughput, 2.4 l/h) × utility meter "Brennerstunden seit Messbeginn" (burner hours since start of measurement; counts only increments, ESP outages lose nothing) → template "Heizöl verbraucht" (heating oil consumed) + daily counter | ✅ active, **not calibrated** |
| **Start delay** | Enable signal (`0x0842` on) stamps the time, the next increase of the burner starts writes the waiting time into an `input_number` | ✅ active |
| **Start alarm** | Enable signal for 45 min, but no start → push "Brenner startet nicht" (burner does not start); if it does start later → all-clear | ✅ active, self-test runs at the next burner start |
| Tank forecast / warning | via the separate pneumatic tank measurement | ✅ implemented there |

**Finding 12.10.:** `0x0842` ("Brenner") is the **enable signal** from the controller, not the flame. Between
enable signal and actual start, 1–25 min pass on this system (cause unverified, presumably oil preheating).
The burner has started when the "Brennerstarts" (burner starts) counter increases.

**Important for automations:** Without a connection, the Optolink binary sensors report `unknown`/`unavailable`, not `off`.
"Burner fault = off" is therefore no proof of fault-free operation.

The level measurement on the underground tank (pneumatic, its own ESP32) is a **separate project** and not part of this repo.

---

## 9. Open items, next steps, appointments

| When | What |
|---|---|
| 14.10.2026 | Evaluate the self-test of the start alarm (runs automatically at the next burner start) |
| 14.10.2026 | Circulation: evaluate the temperature curve of the first night – does the pump switch off at night? |
| 15.–18.10.2026 | Comparison test: start delay with greatly reduced Optolink polling – does the bus load the controller? |
| 02.11.2026 | Calibrate the nozzle throughput against the tank measurement (weekly totals, deliveries subtracted) |
| open | General fault: clarify the cause of the false reports (suspicion: response of another data point wrongly assigned) |
| open | Clarify the meaning of "Betriebsart (Rohwert)" and "Raumtemperatur Soll" |
| open | Read the controller's fault history via the Optolink (format not yet decoded) |
| open | Holder for the head instead of adhesive tape |
| optional | Add the DS18B20 to the pin assignment sheet |

---

## 10. File overview

| Path | Content |
|---|---|
| `README.md` / `README.en.md` | this overview (German / English) |
| `docs/einbau.md` | assembly and mounting step by step |
| `docs/einmessen.md` | commissioning, address check, oil consumption calibration |
| `docs/fehlersuche.md` | failure patterns, causes, solutions |
| `docs/verlauf.md` | project history with dates |
| `docs/*.en.md` | English versions of the docs |
| `firmware/heizung-optolink.yaml` | ESPHome configuration (Builder state) |
| `firmware/secrets.example.yaml` | template for the secrets (without real values) |
| `gehaeuse/optolink-gehaeuse.scad` | OpenSCAD source of all enclosure parts |
| `gehaeuse/kopf.stl`, `kopf_deckel.stl`, `v_schluessel.stl` | read head with lid and guide V (head as of 11.10.) |
| `gehaeuse/esp.stl`, `esp_deckel.stl` | ESP32 enclosure with lid |
| `gehaeuse/vorschau_*.png` | rendered images (as of 08.10.) |
| `plaene/optolink-schaltplan.pdf` | circuit diagram of the read head + connection table + position in the head (A4, SFH 309) |
| `plaene/optolink_plan.svg` | the same as SVG |
| `plaene/optolink_plan.py` | matplotlib script that generates the diagram |
| `plaene/esp32-belegung.pdf` | connection sheet read head → ESP32 pin header (12.10.) |
| `plaene/ds18b20-zirkulation-plan.pdf` | soldering and connection plan of the circulation sensor (13.10.) |
| `plaene/ds18b20_plan.py` | matplotlib script for it |
| `.gitignore` | excludes secrets, build folders and backup copies |

**Sources:** openv wiki ("Die Optolink-Schnittstelle", "ESPHome-Optolink", "Adressen", `vito.scad`), VitoWiFi,
ESPHome PR #4453.
