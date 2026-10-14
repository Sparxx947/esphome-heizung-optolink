🇩🇪 [Deutsche Version](verlauf.md)

# Project history

| Date | What |
|---|---|
| 03./04.10.2026 | Fault **D1** (burner fault) on the Vitotronic – tank empty, nobody noticed. Idea: read out the Optolink and report to HA. |
| 04.10. | Type plate: Vitotronic 200 **KW2**. Approach decided: ESPHome PR #4453 (`protocol: KW`), circuit according to openv/VitoWiFi, addresses from the openv table V200KW2. |
| 04.10. | Wi-Fi test at the boiler with a D1 mini: −41/−42 dBm (AP directly in front of the boiler room). |
| 04.10. | Decision: the ESP32-CAM set remains untouched, instead a new **ESP32-WROOM-32U DevKitC** with external antenna. |
| 04.10. | Ordered: 2× ESP32 + IR LEDs (delivery 06.10.), phototransistor L-93DP3C (delivery 09.10.), magnets 10 × 3 mm (06.10.). |
| 04.10. | `heizung-optolink.yaml` written, validated and compiled (RAM 28 %, flash 50 %); enclosure SCAD + STL first version. |
| 05.10. | Oil delivered (1,500 l), burner runs again after bleeding. |
| 06.10. | Dimensions measured (Jens): board 48.24 × 28.15 mm, USB-C protrudes 1.6 mm, lamp distance **14.4 mm** → SCAD adapted. SMA hole moved below the board. |
| 06.10. ~19:40 | ESP32 flashed, `192.168.178.193`, HA integration "Heizung" (heating) with 24 entities. **Trap:** first flashed the test build with dummy secrets, `upload` did not recompile → corrected with `esphome run` and real secrets. |
| 06.10. ~20:00 | Added to the ESPHome Builder, online; Builder version authoritative from now on. Fixed IP in the FRITZ!Box. |
| 06.10. evening | Datasheet L-93DP3C checked: **collector = short leg**. Circuit diagram printed. |
| 07.10. | First print of the ESP enclosure (Jens) shows two faults: magnet pockets through the floor, supports under the pin headers → floor 4 mm, 4 supports between the pin rows. Jens: "fits like this now". |
| 07.10. | USB access on the PC permanently solved via a udev rule. |
| 08.10. | Optolink enclosure printed (according to Jens). |
| 08.10. | Documentation repo created. |
| 09.10. | Phototransistor (L-93DP3C) not delivered; SFH 309 FA ordered from Reichelt as a fallback. Read-head appointment moved to Sat 10.10. |
| 10.10. | L-93DP3C still not there → **SFH 309** (3 mm clear) bought at a local electronics shop, circuit diagram switched over, read head soldered. |
| 10.10. evening | No response at the boiler. Two soldering faults found: **IR LED reversed polarity** and **LED series resistor 220 kΩ instead of 220 Ω** (red-red-yellow). Reflection test passed afterwards. |
| 10.10. 19:24 | ESP32 drops out and apparently no longer boots on USB → considered **defective**, replacement ordered. **Wrong:** on 11.10. the board ran flawlessly on the PC. At the same time a Wi-Fi access point was not forwarding anything on 2.4 GHz; the serial output stopping in the middle of booting is normal and not a crash. |
| 11.10. ~11:20 | **First response from the controller** (KW sync, identifier `20 98`) – with a Raspberry Pi as interim reader. Cause of the failed attempts: the **windows in the head were 2.4 mm too high**. Head moved down → response. |
| 11.10. | Head redesigned (`v_versatz_y` −1.5 → 0.9) and printed – fits straight away. Magnets do not hold on the plastic front → head fixed with adhesive tape. |
| 11.10. | **Address scan**: boiler setpoint is `0x5502` (not `0x555A`), flow setpoint does not exist on this KW2, heating circuit in use is **M2** (`0x3906`); new: hot-water setpoint, heating curve. In the interim the Pi wrote the values to HA via REST. |
| 12.10. | **ESP32 in operation at the boiler**, Pi removed. Bus overloaded (~21 reads/min requested, ~17 possible) → intervals reduced, queue 0–3. |
| 12.10. | HA: oil consumption from burner runtime (2.4 l/h, uncalibrated). Finding: `0x0842` is the **enable signal**, not the flame; 1–25 min until start → measurement of the start delay + start alarm after 45 min. |
| 12.10. | `0x7574` (controller's oil consumption) = 0 → not kept on this system. Hot-water setpoint filter (first value after restart was 5 instead of 55) and sensor "Neustart-Grund" (reset reason) added. |
| 13.10. | **Sammelstörung** (general fault) has been reporting "on" briefly about 20× since 04:17, burner fault off, burner running normally. The controller's display shows **no fault** at the same time; fault history: 10× d1 (tank empty at the beginning of October) → read error, filter `delayed_on: 30min`. |
| 13.10. | **DS18B20 "Zirkulation Rücklauf"** (circulation return) added on GPIO4 (4.7 kΩ soldered to the cable end, 3V3 shared via Wago), first value 46.6 °C. |
| 13.10. 18:07 | **Brennerstörung** (burner fault) falsely "on" for 4 min (burner running, display without fault). Alarm moved into its own automation with a plausibility check: enable signal ≥ 30 min, burner hours or boiler temperature over 5 min. |
| 14.10. | **False alarms resolved** (debug capture 17:34–18:24, 266 requests): 47 bus suspensions in 50 min; the first request afterwards returns the sync byte **0x05** as payload for 1-byte data points (21/21) → general fault, HC pump M2, **burner** (twice ~15 s falsely "on" in HA), operating mode. 2/4-byte requests then time out (stale bytes in the buffer). 18:28 OTA: switch states accept only 0/1, operating mode/room setpoint range-filtered, log back to INFO. **Open:** cause of the frequent timeouts; the component does not re-sync after resuming. Circulation: `0x0846` read only 6× in 50 min (expected 25) – explains the lag to the return temperature at most partly. |
