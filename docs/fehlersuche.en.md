🇩🇪 [Deutsche Version](fehlersuche.md)

# Troubleshooting

## Failure patterns that have already occurred

| Symptom | Cause | Solution | Date |
|---|---|---|---|
| Fallback hotspot does not accept the password | The **test build with dummy secrets** was flashed (wrong hotspot password, wrong API key) | Never flash a test build; reflash with real secrets and verify via the API | 06.10. |
| Second flash attempt uploads the old firmware again | `esphome upload` does **not** recompile, it takes the last build from `.esphome/` | For real firmware always use `esphome run …`; watch for "Successfully compiled" | 06.10. |
| USB port locked after replugging (Linux) | `/dev/ttyUSB0` is recreated every time it is plugged in, a `setfacl` permission is lost | Since 07.10. udev rule on the PC (`70-esp-seriell.rules`, CP210x/CH340/Espressif, `uaccess`) – no more `setfacl` needed | 06./07.10. |
| SMA hole not usable in the print | Hole was behind the right-hand board support | Hole moved below the board (`sma_z = 8`), 12 mm gap | 06.10. |
| Magnet pockets go through the floor | Pocket depth 3.2 mm > floor thickness 2.0 mm | `boden = 4.0` | 07.10. |
| Board does not sit flat, pins hit the supports | Pin headers run along the entire board length; continuous supports | 4 individual supports between the pin rows (3.2 mm from the edge, 12 mm free in the middle) | 07.10. |

Another flashing error ("No more data to read" at 460800 baud) occurred on the **tank-level ESP32**, not on this
device. If it occurs here: write the finished `firmware.factory.bin` with `esptool … --baud 115200`.

## Expected failure patterns during commissioning (not yet occurred)

| Symptom | Possible cause | Check / solution |
|---|---|---|
| All Optolink values `unknown`, "Optolink-Status" stays `communication state unknown` | Head not attached / rotated; LED and PT swapped; legs wrong | Check position: LED left (red lamp), PT right (green lamp), "OBEN" (top) at the top; polarity via diode test |
| No responses in the log, but the LED transmits | Phototransistor wrong polarity or 10 kΩ missing | Collector (short leg) to GPIO16 + 10 kΩ to 3V3, emitter to GND |
| LED does not transmit | LED reversed (cathode must go to GPIO17), 220 Ω open | Point a phone camera (without IR filter) at the LED – IR flicker visible during requests (general trick, not tried here) |
| Sporadic dropouts | Head not sitting flat, ambient light | Press the head on, check the V key; if necessary replace components with SFH487 / SFH309FA |
| Values plausible, but one quantity wrong | openv address does not match this system | Check the address using [`einmessen.en.md`](einmessen.en.md), correct or disable the entity |
| Outdoor temperature in winter 6000 °C or similar | Value read without sign | `min_value: -60` must be in the YAML (is set) |
| Device `unavailable` in HA | Wi-Fi, power | "WLAN-Signal" (Wi-Fi signal; measured at the boiler on 04.10. −41/−42 dBm), check the USB power supply; fallback hotspot `Heizung-Fallback` |

## Important for automations

Without a connection, the Optolink binary sensors report **`unknown`**, not `off`. "Brennerstörung (burner fault) = off" is therefore
no proof of fault-free operation – a permanent `unknown` must itself be treated as a problem.

## Distinction: heating reports D1

D1 = **burner fault**. On 03./04.10. the cause was an empty tank. After refilling on 05.10. the burner only ran
again after bleeding (filter, port P on the Danfoss pump BFP 21 L3) and a reset on the burner control unit LOA24
(red button). The "Entsperrung" (unlock) button on the controller is the **STB** (safety temperature limiter), not the burner reset.
