🇩🇪 [Deutsche Version](einbau.md)

# Assembly and installation

Step by step from the components to the attached read head. Circuit diagram to keep at hand:
[`../plaene/optolink-schaltplan.pdf`](../plaene/optolink-schaltplan.pdf).

## Prepare beforehand

- printed parts: `kopf` (head), `kopf_deckel` (head lid), `v_schluessel` (V key), `esp`, `esp_deckel` (ESP lid) (PETG)
- IR LED Chanzon 940 nm, phototransistor Osram SFH 309 (or Kingbright L-93DP3C), 220 Ω, 10 kΩ
- 4 neodymium magnets 10 × 3 mm
- 4 Dupont wires female–female (red, black, yellow, green)
- ESP32-WROOM-32U DevKitC (already flashed) with antenna + IPEX→SMA pigtail
- Soldering iron, multimeter, heat-shrink tubing/insulating tape, hot glue if needed

## 1. Check the components

1. **IR LED:** long leg = anode (+), short leg/flat side = cathode.
   Diode test: red on the anode, black on the cathode → the forward voltage is displayed.
2. **Phototransistor SFH 309** (likewise L-93DP3C): **collector = short leg** on the flattened side, emitter = long leg.
   Cross-check: multimeter on 2 MΩ, red on the collector, black on the emitter, shine a phone torch on it → the value drops significantly;
   covered → very high resistance.
3. **Measure the resistors:** 220 Ω is red-red-**brown** – red-red-**yellow** would be 220 kΩ (exactly what happened on 10.10.).
4. Installing it the wrong way round destroys nothing – you just get no data.

## 2. Solder the read head

1. Hold the head with its back towards you, embossing **"OBEN" (top) facing up**.
   Then the same side applies as when looking at the controller:
   - **left ("LED")** → IR LED (transmits into the controller's red receiving lamp)
   - **right ("FT", phototransistor)** → phototransistor (receives from the green transmitting lamp)
2. Insert both components from behind into the windows until the component base rests against the collar; the lens is
   flush with the front (4 mm). Secure with a drop of glue if needed.
3. Wire up in the cavity (12 mm deep):

   | From | To |
   |---|---|
   | red (3V3) | 220 Ω → LED anode **and** 10 kΩ → PT collector |
   | yellow (GPIO17) | LED cathode |
   | green (GPIO16) | PT collector (together with the 10 kΩ) |
   | black (GND) | PT emitter |

4. Insulate the solder joints, route the four strands out through the cable outlet at the top (7 × 4 mm).
5. **Two magnets** from behind into the pockets above and below the windows. **Caution:** on the Vitotronic 200 KW2
   the front is made of plastic – the magnets do not hold there. Secure the head with adhesive tape (step 4.1).
6. Plug the **V key** with its 2 mm peg into the pocket in the front (tip pointing down), glue if needed.
7. Push on `kopf_deckel` (head lid); the cable outlet in the push-fit collar must be above the one in the head.

## 3. Fit out the ESP enclosure

1. One magnet each from below into the two floor pockets (0.8 mm remaining wall).
2. SMA socket of the pigtail from the inside through the hole at the bottom right (Ø 6.6 mm), tighten the nut on the outside.
   The hole is deliberately **below** the board.
3. Press the pigtail onto the ESP32's IPEX connector.
4. Plug the Dupont wires onto the pins `3V3`, `GND`, `GPIO17`, `GPIO16` (see the table in the README).
5. Place the board with **USB-C towards the left end face** on the four supports. The supports stand between the
   pin rows; below them there is room for pins and Dupont sockets. Fix with hot glue if needed.
6. Route the Dupont wires through the side outlet (12 × 6 mm, near the USB side).
7. Push on the lid.

## 4. Mounting on the boiler

1. Place the read head with the V key into the "V" cut-out of the Vitotronic (front left) and **fix it with adhesive
   tape**. The V web protrudes 6 mm, the controller allows at most 8 mm. If the controller does not respond, move the head
   vertically until it responds, and only then tape it in place.
2. Attach the ESP enclosure magnetically to the boiler sheet metal within reach of the strands.
3. Screw the antenna onto the SMA socket.
4. Connect USB-C power via a 5 V USB power supply.
5. Continue with [`einmessen.en.md`](einmessen.en.md).

## 5. Addition: circulation sensor DS18B20

Plan: [`../plaene/ds18b20-zirkulation-plan.pdf`](../plaene/ds18b20-zirkulation-plan.pdf).

1. Unplug USB from the ESP32, do **not** move the read head.
2. At the cable end of the sensor, first slide on heat-shrink tubing, then solder the **4.7 kΩ resistor between red and yellow**;
   at the same time solder a jumper wire with a female connector to yellow, and likewise to black.
3. Check with the multimeter: red ↔ yellow ≈ 4.7 kΩ, red ↔ black and yellow ↔ black no continuity.
4. **Wago "3.3 V":** new wire to the `3V3` pin, red wire of the read head, red wire of the sensor.
5. Yellow to `GPIO4` (right row, directly below 16), black to a free `GND`.
6. Lay the sensor lengthwise flat on the circulation pipe, two cable ties, pipe insulation over it.
7. Plug USB back in; upload the firmware with `one_wire` + `dallas_temp` via OTA. A value of 85 °C or
   −127 °C indicates a wiring fault.

## Notes

- The "Entsperrung" (unlock) button on the controller is the **STB** (safety temperature limiter), not the burner reset. The burner reset is the red
  reset button on the burner control unit (Landis & Gyr LOA24). For this project neither needs to be pressed.
- Do not touch the AFRISO leak detector on the tank gauge (belongs to the tank, not to this project).
