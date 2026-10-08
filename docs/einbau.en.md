🇩🇪 [Deutsche Version](einbau.md)

# Assembly and installation

Step by step from the components to the attached read head. Circuit diagram to keep at hand:
[`../plaene/optolink-schaltplan.pdf`](../plaene/optolink-schaltplan.pdf).

## Prepare beforehand

- printed parts: `kopf` (head), `kopf_deckel` (head lid), `v_schluessel` (V key), `esp`, `esp_deckel` (ESP lid) (PETG)
- IR LED Chanzon 940 nm, phototransistor Kingbright L-93DP3C, 220 Ω, 10 kΩ
- 4 neodymium magnets 10 × 3 mm
- 4 Dupont wires female–female (red, black, yellow, green)
- ESP32-WROOM-32U DevKitC (already flashed) with antenna + IPEX→SMA pigtail
- Soldering iron, multimeter, heat-shrink tubing/insulating tape, hot glue if needed

## 1. Check the components

1. **IR LED:** long leg = anode (+), short leg/flat side = cathode.
   Diode test: red on the anode, black on the cathode → the forward voltage is displayed.
2. **Phototransistor L-93DP3C:** according to the datasheet **collector = short leg**, emitter = long leg.
   Double-check with the multimeter (resistance collector→emitter drops significantly with light or remote-control IR).
3. Installing it the wrong way round destroys nothing – you just get no data.

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
5. **Two magnets** from behind into the pockets above and below the windows (0.6 mm remaining wall to the front – they hold
   through it). Polarity such that the head sticks to the controller.
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

1. Place the read head with the V key into the "V" cut-out of the Vitotronic (front left); the magnets hold it.
   The V web protrudes 6 mm, the controller allows at most 8 mm.
2. Attach the ESP enclosure magnetically to the boiler sheet metal within reach of the strands.
3. Screw the antenna onto the SMA socket.
4. Connect USB-C power (power supply/cable route not yet defined in the notes).
5. Continue with [`einmessen.en.md`](einmessen.en.md).

## Notes

- The "Entsperrung" (unlock) button on the controller is the **STB** (safety temperature limiter), not the burner reset. The burner reset is the red
  reset button on the burner control unit (Landis & Gyr LOA24). For this project neither needs to be pressed.
- Do not touch the AFRISO leak detector on the tank gauge (belongs to the tank, not to this project).
