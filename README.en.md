🇩🇪 [Deutsche Version](README.md)

# Heating · Optolink (Vitotronic 200 KW2 → ESPHome → Home Assistant)

DIY read head on the Optolink interface of a Viessmann oil-fired boiler. An ESP32 running ESPHome
reads temperatures, burner state, burner hours and **fault messages** from the controller and passes them on to
Home Assistant. **Deliberately read-only** – the firmware contains nothing that writes to the controller.

> State of this documentation: **08.10.2026**. Device flashed and in HA, **read head not yet soldered**
> (phototransistor was announced for Fri 09.10. but has not arrived yet). All Optolink values in HA are therefore still `unknown`.

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
| **What is measured** | Burner fault (display **D1**), general fault, burner on/off, pumps, outdoor/boiler/hot-water/flow temperatures incl. setpoints, burner starts, **burner hours** |
| **What is controlled** | nothing (on purpose) |
| **Goal** | Push notification on burner fault (trigger: fault D1 on 03./04.10.2026 with an empty tank, which nobody noticed); oil consumption from burner hours × nozzle throughput as the basis for a tank forecast |

**Principle:** Behind a "V"-shaped cut-out at the front, the Vitotronic has two small lamps – an IR receiving diode
(left, red) and an IR transmitting diode (right, green). Through them it talks serially using the **KW protocol (VS1), 4800 baud 8E2**.
The read head sits on top of them, held by magnets: an **IR LED** (940 nm) transmits into the left lamp, a **phototransistor**
receives from the right one. The ESP32 drives both via a UART (RX GPIO16 / TX GPIO17) using the ESPHome component
`optolink` from **ESPHome PR #4453** (not yet merged into ESPHome). Circuit according to VitoWiFi/openv wiki.

---

## 2. Status (as of 08.10.2026)

| Area | Status | Date / remark |
|---|---|---|
| Concept, addresses, circuit | ✅ done | 04.10. – addresses from the openv table V200KW2, **not yet checked against the display** |
| Firmware (YAML) | ✅ done, compiled | 04.10. (RAM 28 %, flash 50 %), unchanged since |
| ESP32 flashed, Wi-Fi, HA | ✅ done | 06.10. ~19:40 – `192.168.178.193`, HA integration "Heizung" (heating), 24 entities |
| Fixed IP in the router | ✅ done | 06.10. (DHCP reservation, always the same IP) |
| In the ESPHome Builder | ✅ done, online | 06.10. ~20:00 – the Builder version is **authoritative** from now on |
| Enclosure (SCAD/STL) | ✅ done | 06.10. dimensions entered, 07.10. floor + supports corrected ("fits like this now", Jens) |
| Enclosure printed | ✅ printed | 08.10. according to Jens (whether it is exactly the version from 07.10. has not been explicitly confirmed) |
| Solder read head | ⏳ open | phototransistor not delivered yet (as of 09.10. evening), appointment moved to **Sat 10.10.** |
| Commissioning / check addresses | ⏳ open | after soldering, with `optolink: logger: true` |
| HA automations (push, oil consumption, forecast) | ⏳ open | only after successful commissioning |

---

## 3. Bill of materials

Prices and ASINs at the time of ordering (Amazon.de, October 2026).

| Part | Qty | Designation / type | Source, ASIN, price | Status |
|---|---|---|---|---|
| Microcontroller | 1 | **ESP32-WROOM-32U DevKitC V4**, USB-C, CP2102, IPEX antenna connector; board 48.24 × 28.15 mm | Amazon **B0F6567LB5**, 13.99 € (2 pieces ordered, the second one is for the tank level measurement) | ✅ delivered 06.10., flashed |
| Antenna | 1 | 2.4 GHz antenna with IPEX→SMA pigtail (SMA socket Ø ~6.4 mm, 1/4″) | included in the ESP32's antenna kit | ✅ available |
| IR LED | 1 (+ spare) | **Chanzon** IR LED 940 nm, 3 mm, 100 pieces (replacement for SFH487 / SIR 204 from the openv wiki) | Amazon **B01BVEKXNC**, 7.99 € | ✅ ordered 04.10., delivery announced for 06.10. (receipt not explicitly noted) |
| Phototransistor | 1 (+ spare) | **Kingbright L-93DP3C**, 3 mm, 940 nm, 5 pieces (replacement for SFH309FA) | Amazon **B01M3PGVRC**, 9.77 € (Marketplace) | ⏳ ordered, delivery was announced for Fri 09.10. – not arrived yet |
| Resistor | 1 | 220 Ω (series resistor IR LED) | AZ-Delivery resistor assortment | ✅ available |
| Resistor | 1 | 10 kΩ (pull-up phototransistor) | AZ-Delivery resistor assortment | ✅ available |
| Magnets | 4 | Neodymium disc magnet **10 × 3 mm** (2 in the read head, 2 in the floor of the ESP enclosure) | Amazon, Delaga, 50 pieces, 7.99 € | ✅ ordered 04.10., delivery announced for 06.10. |
| Connecting wires | 4 | Dupont jumpers **female–female** (F2F), suggested colours red/black/yellow/green | ELEGOO jumper set M2M/F2M/F2F (40 × 20 cm) | ✅ available |
| Power supply | 1 | USB-C cable + USB power supply 5 V | – | ❓ **not in the notes** – probably available, clarify before installation |
| Filament | ~20 g (estimated) | **PETG** (heat near the boiler) | available | ✅ available, enclosure printed 08.10. |
| Adhesive | a little | Hot glue (fix the board on the supports, optional) or superglue for the V key (optional) | available (assumed) | ✅ |
| Screws | 0 | none – push-fit lids and magnets | – | – |
| Tools | – | Soldering iron, multimeter (diode test), calipers, 3D printer | available | ✅ |

Not used, but easily confused: the **AZ-Delivery LED assortment** is visible light and useless for Optolink.
The **ESP32-CAM set** (with MB board) remains untouched – it was originally intended, but was dropped on
04.10. in favour of a new ESP32.

Original components according to openv/VitoWiFi: IR LED **SFH487** (or SIR 204 EVL), phototransistor **SFH309FA** – not
available on Amazon; in case of problems they can be obtained from Reichelt as a replacement.

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
| Phototransistor L-93DP3C | Emitter → GND | **Collector** → GPIO16 + 10 kΩ | Kingbright datasheet (DSAC1289), checked 06.10. |

The printout still says "usually the short leg – check!" for the phototransistor; this has since been confirmed by the datasheet.
Nevertheless, double-check with the multimeter's diode test before soldering. Getting it the wrong way round breaks nothing,
you just get no data.

**Position in the head** (looking **at** the controller = looking at the back of the head while soldering):

| Position | Controller lamp | Function in the controller | Our component |
|---|---|---|---|
| left | red ("Störung" / fault) | IR receiver | **IR LED** |
| right | green ("Betrieb" / operation) | IR transmitter | **Phototransistor** |

Distance between the lamps centre to centre: **14.4 mm** (measured by Jens 06.10.; the openv wiki states 14 mm).
Inside the head, "LED", "FT" (phototransistor) and "OBEN" (top) are embossed.

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
| Logger | `level: INFO`; UART0 stays free for the USB log |
| API | encrypted (`heizung_api_key`) |
| OTA | `platform: esphome`, without its own password (secured via the API key) |
| Fallback hotspot | SSID `Heizung-Fallback`, password from secret, with captive portal |

### Entities in Home Assistant (24)

Device "Heizung" (heating) in the ESPHome integration. The entity IDs follow the ESPHome pattern from
`friendly_name` + name (e.g. presumably `sensor.heizung_brennerstunden`) – **not checked in HA**.

| Name | Type | Address | Format | Interval |
|---|---|---|---|---|
| Brennerstörung (burner fault, = display D1) | binary, problem | `0x0883` | 0/1 | 15 s |
| Sammelstörung (general fault) | binary, problem | `0x0847` | 0/1 | 15 s |
| Brenner (1. Stufe) (burner, stage 1) | binary, running | `0x0842` | 0/1 | 15 s |
| Speicherladepumpe (tank charging pump) | binary, running | `0x0845` | 0/1 | 60 s |
| Zirkulationspumpe (circulation pump) | binary, running | `0x0846` | 0/1 | 60 s |
| Heizkreispumpe (heating circuit pump) | binary, running | `0x2906` | 0/1 | 60 s |
| Außentemperatur (outdoor temperature) | °C | `0x0800` | 2 B ÷ 10, signed | 120 s |
| Außentemperatur gedämpft (outdoor temperature, damped) | °C | `0x5527` | 2 B ÷ 10, signed | 600 s |
| Kesseltemperatur (boiler temperature) | °C | `0x0802` | 2 B ÷ 10 | 60 s |
| Kesselsolltemperatur (boiler setpoint) | °C | `0x555A` | 2 B ÷ 10 | 120 s |
| Warmwassertemperatur (Speicher) (hot-water temperature, tank) | °C | `0x0804` | 2 B ÷ 10 | 120 s |
| Vorlauftemperatur (Sensor 17B) (flow temperature, sensor 17B) | °C | `0x080C` | 2 B ÷ 10 | 120 s |
| Vorlaufsolltemperatur (A1M1) (flow setpoint, A1M1) | °C | `0x2544` | 2 B ÷ 10 | 300 s |
| Abgastemperatur (flue gas temperature; only meaningful with a flue gas sensor) | °C, diagnostic | `0x0808` | 2 B ÷ 10 | 300 s |
| Brennerstarts (burner starts) | counter | `0x088A` | 4 B | 300 s |
| Brennerstunden (Stufe 1) (burner hours, stage 1) | h, total_increasing | `0x08A7` | 4 B, seconds ÷ 3600 | 300 s |
| Ölverbrauch Regelung (oil consumption, controller) | diagnostic | `0x7574` | 4 B ÷ 1000 – **meaning unclear**, observe first | 1800 s |
| Betriebsart (Rohwert) (operating mode, raw value) | diagnostic | `0x2301` | 1 B | 600 s |
| Raumtemperatur Soll (room temperature setpoint) | °C, diagnostic | `0x2306` | 1 B | 600 s |
| Optolink-Warteschlange (Optolink queue) | diagnostic | – | `QUEUE_SIZE` | 60 s |
| Gerätekennung (device ID) | text, diagnostic | – | `DEVICE_INFO` | 1800 s |
| Optolink-Status (Optolink status) | text, diagnostic | – | `STATE_INFO` | 30 s |
| WLAN-Signal (Wi-Fi signal) | dBm | – | – | 120 s |
| Laufzeit (uptime) | s | – | – | 600 s |

All addresses come from the openv table "Adressen" (addresses), column V200KW2/KW1, and have **not yet** been checked against the
controller's display.

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
4. **Attach:** head with the V into the cut-out of the controller, ESP enclosure magnetically onto the boiler sheet metal, USB power.
5. **Check:** log shows responses, "Optolink-Status" leaves `unknown`, device ID `0x2098`(?);
   compare boiler and outdoor temperature with the display.
6. **Finish:** `logger: false`, OTA again; create HA automations (section 8).

---

## 8. Home Assistant integration

The repo contains **no HA packages** (there is no `ha/` here) – the automations have not been created yet.
Planned (as of 04.–08.10.):

| Plan | Basis | Status |
|---|---|---|
| Push on **burner fault** and **general fault** to the household members | `binary_sensor` Brennerstörung / Sammelstörung → `on` | ⏳ planned |
| Oil consumption | burner hours × nozzle throughput (≤ 2.4 l/h), calibrate against delivered quantities → [`docs/einmessen.en.md`](docs/einmessen.en.md) | ⏳ planned |
| Tank forecast / warning | early warning at **1,500 l**, urgent at **800 l** | ⏳ planned |

**Important for the automations:** Without the head or without a connection, the Optolink binary sensors report `unknown`, not
`off`. An automation "burner fault = off → all good" would otherwise give false reassurance. Prolonged `unknown`/`unavailable`
should also be reported (suggestion, not implemented).

The parallel level measurement on the underground tank (pneumatic, ESP32 "Öltank" (oil tank) `.194`) is a **separate project** and
not part of this repo.

---

## 9. Open items, next steps, appointments

| When | What | Who |
|---|---|---|
| **Sat 10.10.2026** (moved from 09.10.) | As soon as a phototransistor is available → solder read head, attach, commissioning with `logger: true`. If both L-93DP3C and SFH 309 FA arrive: use the **SFH 309 FA** (daylight filter); check its pinout in the datasheet before soldering | Jens |
| during installation | Clarify whether "enclosure fits" (07.10.) referred to the print or to the preview – according to Jens it was printed on 08.10. | Jens |
| after soldering | Check addresses against the display (esp. outdoor, boiler, hot-water temperature, burner state) | Jens + Claude |
| after soldering | Read the Wi-Fi signal in the basement at the installation location (at the PC −47 dBm; test unit at the boiler 04.10. −41/−42 dBm) | – |
| afterwards | Observe the meaning of "Ölverbrauch Regelung" (`0x7574`) and "Betriebsart (Rohwert)" | – |
| afterwards | HA: push on fault, oil consumption, tank forecast | Claude |
| afterwards | Set the starting value for oil consumption only after dipping the tank (content since 05.10. presumably ~1,900 l, **unconfirmed**) | Jens |
| open | Clarify power supply (USB power supply, cable route) at the boiler | Jens |
| ordered 09.10. | **SFH 309 FA** (Reichelt) as a fallback in case the L-93DP3C does not arrive; SFH487 only for poor reception | Jens |

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
| `gehaeuse/kopf.stl`, `kopf_deckel.stl`, `v_schluessel.stl` | read head with lid and guide V |
| `gehaeuse/esp.stl`, `esp_deckel.stl` | ESP32 enclosure with lid |
| `gehaeuse/vorschau_*.png` | rendered images |
| `plaene/optolink-schaltplan.pdf` | circuit diagram + connection table + position in the head (A4) |
| `plaene/optolink_plan.svg` | the same as SVG |
| `plaene/optolink_plan.py` | matplotlib script that generates the diagram (output paths in it are local) |
| `.gitignore` | excludes secrets, build folders and backup copies |

**Sources:** openv wiki ("Die Optolink-Schnittstelle", "ESPHome-Optolink", "Adressen", `vito.scad`), VitoWiFi,
ESPHome PR #4453.
