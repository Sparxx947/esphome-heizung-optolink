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
| **09.10. 18:00** | planned: solder the read head, attach, commissioning with `logger: true`, check addresses. |
