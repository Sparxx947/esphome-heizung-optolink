🇩🇪 [Deutsche Version](einmessen.md)

# Commissioning and calibration

With Optolink there is nothing analogue to calibrate – the controller delivers finished values. "Calibration" here means:

1. proving **communication**,
2. checking the **addresses** against the controller's display (they come from the openv table – here three did not match),
3. calibrating the **oil consumption** from the burner hours against real delivered or dipped quantities.

## 1. Prove communication

1. In the ESPHome Builder in `heizung-optolink.yaml`:
   ```yaml
   optolink:
     logger: true      # war false
   ```
   (`# war false` = "was false".) If necessary, additionally set `logger: level: DEBUG` in case no Optolink lines appear at `INFO`
   (whether this is needed has **not been checked**).
2. **INSTALL → Wirelessly**, then open **LOGS** in the Builder.
3. Expected:
   - Responses to the requests appear in the log.
   - Text sensor **"Optolink-Status"** changes away from `communication state unknown`.
   - **"Gerätekennung"** (device ID) should identify the V200KW2 (device ID according to openv `0x2098` or identifier `0x00F8`
     in the address table; which format exactly the sensor outputs is open).
   - **"Optolink-Warteschlange"** (Optolink queue) stays small and does not grow steadily.
4. If nothing comes: [`fehlersuche.en.md`](fehlersuche.en.md).

**Result on this system (11./12.10.):** response only after correcting the head height; "Gerätekennung" (device ID) shows
`Device ID: 2098|Hardware Revision: 00|Software Index: 01`. Then `logger: false` and logger set to `INFO`.

## 2. Check addresses against the display

Compare the values in HA (or in the log) with the Vitotronic's display. Deviations ≤ 0.5 K are rounding.

| Check | HA entity | Address | Comparison on the display | Expectation |
|---|---|---|---|---|
| Outdoor temperature | Außentemperatur | `0x0800` | query outdoor temperature | equal; **negative** in frost (min_value −60 forces signed reading) |
| Boiler | Kesseltemperatur | `0x0802` | boiler temperature | equal |
| Hot water | Warmwassertemperatur | `0x0804` | tank temperature | equal |
| Flow | Vorlauftemperatur | `0x080C` | only if sensor 17B is present | otherwise implausible/constant |
| Flue gas | Abgastemperatur | `0x0808` | only if a flue gas sensor is installed | otherwise implausible → disable entity |
| Burner | Brenner | `0x0842` | enable signal from the controller | **Result:** enable signal, not flame – the burner starts 1–25 min later |
| Boiler setpoint | Kesselsolltemperatur | `0x5502` | boiler setpoint | **Result:** `0x555A` from the table returns FF FF, `0x5502` matches |
| Hot-water setpoint | Warmwasser-Solltemperatur | `0x6300` | set hot-water setpoint | **Result:** 55 °C ✅ |
| Pumps | Speicherlade-, Zirkulations-, Heizkreispumpe A1 / M2 (tank charging, circulation, heating circuit pump A1 / M2) | `0x0845`, `0x0846`, `0x2906` / `0x3906` | pump audible/palpable | **Result:** A1 always off, **M2** is the one in use |
| Burner hours | Brennerstunden | `0x08A7` | operating hours in the controller | equal (seconds ÷ 3600) |
| Burner starts | Brennerstarts | `0x088A` | burner starts | equal |
| Fault | Brennerstörung / Sammelstörung (burner fault / general fault) | `0x0883` / `0x0847` | fault display | `off` in normal operation |
| Operating mode | Betriebsart (Rohwert) | `0x2301` | set operating mode | note the raw value, observe the mapping |
| Oil consumption controller | Ölverbrauch Regelung | `0x7574` | – | **Result:** always 0 – not kept by this KW2 |
| Flow setpoint | – | `0x2544` / `0x3544` | – | **Result:** FF FF – removed |

Correct addresses that do not match in the YAML or disable the entity; record the result in [`verlauf.en.md`](verlauf.en.md).
Then `optolink: logger: false` and OTA again.

## 3. Calibrate oil consumption from burner hours

### Basic formula

```
Verbrauch [l] = (Brennerstunden_Ende − Brennerstunden_Anfang) [h] × q [l/h]
```

(Consumption [l] = (burner hours at end − burner hours at start) [h] × q [l/h].)

**Starting value for q:** The burner (VEA I-2) is rated at max. **2.0 kg/h**. With heating oil EL ρ ≈ 0.84 kg/l:

```
q_max = 2,0 kg/h ÷ 0,84 kg/l ≈ 2,38 l/h   (≈ 2,4 l/h)
```

That is the **maximum value**; the actual nozzle is not documented, so q is more likely lower.

### Calibrating against delivered and dipped quantities

Between two points in time with known tank content (dipping or full delivery):

```
q = (Inhalt_Anfang + Lieferungen_dazwischen − Inhalt_Ende) [l]
    ÷ (Brennerstunden_Ende − Brennerstunden_Anfang) [h]
```

(q = (content at start + deliveries in between − content at end) [l] ÷ (burner hours at end − burner hours at start) [h].)

Procedure:

1. **Set the starting point:** dip the tank (dipstick in the manhole) and at the same time note the "Brennerstunden" (burner hours) reading.
   Since the delivery on 05.10. (1,500 l) the content according to the gauge is ~1,900 l – this is **not confirmed**
   (the old pneumatic gauge was silted up). Dipping reference values (horizontal cylinder Ø 1.6 m, ends neglected):
   1,500 l ≈ 42.7 cm, 1,700 l ≈ 46.7 cm, 1,900 l ≈ 50.6 cm.
2. **End point:** at the next delivery or after a few weeks, dip again + note the burner hours.
3. Calculate q using the formula and store it in HA as a factor (`input_number` "Öl-Düsendurchsatz" (oil nozzle throughput)). **Calibrate
   only once:** the template sensor recalculates the entire total since the start of measurement with the new factor – a change
   creates a jump in the statistics.
4. Plausibility: previous deliveries (3,000 l on 20.09.2024, 3,000 l on 04.08.2025) lasted ~14 months;
   annual consumption ~2,800 l. With q = 2.38 l/h this would be ~1,180 burner hours/year (**derived**, not measured) –
   an annual value of burner hours from the controller immediately shows whether q is in the right order of magnitude.

### Implementation in Home Assistant (since 12.10.)

| Helper | Kind | Content |
|---|---|---|
| Öl-Düsendurchsatz (oil nozzle throughput) | `input_number` | 2.4 l/h (nameplate maximum, **not calibrated**) |
| Brennerstunden seit Messbeginn (burner hours since start of measurement) | utility meter on "Brennerstunden" | counts only increments – ESP outages lose nothing |
| Heizöl verbraucht (Brennerlaufzeit) (heating oil consumed, burner runtime) | template | burner hours since start of measurement × nozzle throughput, litres, `total_increasing` |
| Heizöl heute (heating oil today) | utility meter (daily) | on the template sensor |

The nozzle cannot be read off the burner, and the controller does not know it (`0x7574` = 0). Calibration is therefore done against
the separate tank measurement – using **weekly totals**, because its daily values are noisier than the daily consumption.
Tank forecast and warning thresholds (early warning 1,500 l, urgent 800 l) are handled by the tank measurement.
