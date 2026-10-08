🇬🇧 [English version](einmessen.en.md)

# Inbetriebnahme und Einmessen

Beim Optolink gibt es nichts analog zu kalibrieren – die Regelung liefert fertige Werte. „Einmessen“ heißt hier:

1. **Kommunikation** nachweisen,
2. **Adressen** gegen das Display der Regelung prüfen (sie stammen ungeprüft aus der openv-Tabelle),
3. den **Ölverbrauch** aus den Brennerstunden an echten Liefer- bzw. Peilmengen eichen.

## 1. Kommunikation nachweisen

1. Im ESPHome Builder in `heizung-optolink.yaml`:
   ```yaml
   optolink:
     logger: true      # war false
   ```
   Ggf. zusätzlich `logger: level: DEBUG` setzen, falls bei `INFO` keine Optolink-Zeilen erscheinen
   (ob nötig, ist **nicht geprüft**).
2. **INSTALL → Wirelessly**, danach im Builder **LOGS** öffnen.
3. Erwartung:
   - Im Log erscheinen Antworten auf die Anfragen.
   - Text-Sensor **„Optolink-Status“** wechselt weg von `communication state unknown`.
   - **„Gerätekennung“** sollte die V200KW2 ausweisen (Geräte-ID laut openv `0x2098` bzw. Kennung `0x00F8`
     in der Adressen-Tabelle; welches Format der Sensor genau ausgibt, ist offen).
   - **„Optolink-Warteschlange“** bleibt klein und läuft nicht stetig hoch.
4. Kommt nichts: [`fehlersuche.md`](fehlersuche.md).

## 2. Adressen gegen das Display prüfen

Werte in HA (oder im Log) mit der Anzeige der Vitotronic vergleichen. Abweichungen ≤ 0,5 K sind Rundung.

| Prüfen | HA-Entität | Adresse | Vergleich am Display | Erwartung |
|---|---|---|---|---|
| Außentemperatur | Außentemperatur | `0x0800` | Abfrage Außentemperatur | gleich; bei Frost **negativ** (min_value −60 erzwingt vorzeichenbehaftetes Lesen) |
| Kessel | Kesseltemperatur | `0x0802` | Kesseltemperatur | gleich |
| Warmwasser | Warmwassertemperatur | `0x0804` | Speichertemperatur | gleich |
| Vorlauf | Vorlauftemperatur | `0x080C` | nur falls Fühler 17B vorhanden | sonst unplausibel/konstant |
| Abgas | Abgastemperatur | `0x0808` | nur falls Abgasfühler verbaut | sonst unplausibel → Entität deaktivieren |
| Brenner | Brenner | `0x0842` | Flamme / Brenner läuft | `on` während der Brenner läuft |
| Pumpen | Speicherlade-, Zirkulations-, Heizkreispumpe | `0x0845`, `0x0846`, `0x2906` | Pumpe hörbar/fühlbar | passt zum Betrieb |
| Brennerstunden | Brennerstunden | `0x08A7` | Betriebsstunden in der Regelung | gleich (Sekunden ÷ 3600) |
| Brennerstarts | Brennerstarts | `0x088A` | Brennerstarts | gleich |
| Störung | Brennerstörung / Sammelstörung | `0x0883` / `0x0847` | Störungsanzeige | im Normalbetrieb `off` |
| Betriebsart | Betriebsart (Rohwert) | `0x2301` | eingestellte Betriebsart | Rohwert notieren, Zuordnung beobachten |
| Ölverbrauch Regelung | Ölverbrauch Regelung | `0x7574` | – | **Funktion unklar** – nur beobachten |

Nicht passende Adressen in der YAML korrigieren oder die Entität deaktivieren; das Ergebnis in [`verlauf.md`](verlauf.md)
nachtragen. Danach `optolink: logger: false` und erneut OTA.

## 3. Ölverbrauch aus Brennerstunden eichen

### Grundformel

```
Verbrauch [l] = (Brennerstunden_Ende − Brennerstunden_Anfang) [h] × q [l/h]
```

**Startwert für q:** Der Brenner (VEA I-2) ist mit max. **2,0 kg/h** angegeben. Mit Heizöl EL ρ ≈ 0,84 kg/l:

```
q_max = 2,0 kg/h ÷ 0,84 kg/l ≈ 2,38 l/h   (≈ 2,4 l/h)
```

Das ist der **Höchstwert**; die tatsächliche Düse ist nicht dokumentiert, q liegt also eher darunter.

### Eichen an Liefer- und Peilmengen

Zwischen zwei Zeitpunkten mit bekanntem Tankinhalt (Peilung oder volle Lieferung):

```
q = (Inhalt_Anfang + Lieferungen_dazwischen − Inhalt_Ende) [l]
    ÷ (Brennerstunden_Ende − Brennerstunden_Anfang) [h]
```

Ablauf:

1. **Anfangspunkt setzen:** Tank peilen (Peilstab im Domschacht) und gleichzeitig den Stand „Brennerstunden“ notieren.
   Seit der Lieferung am 05.10. (1.500 l) liegt der Inhalt laut Anzeige bei ~1.900 l – das ist **nicht bestätigt**
   (die alte pneumatische Anzeige war verschlammt). Peil-Richtwerte (liegender Zylinder Ø 1,6 m, Böden vernachlässigt):
   1.500 l ≈ 42,7 cm, 1.700 l ≈ 46,7 cm, 1.900 l ≈ 50,6 cm.
2. **Endpunkt:** bei der nächsten Lieferung bzw. nach einigen Wochen erneut peilen + Brennerstunden notieren.
3. q nach der Formel rechnen und in HA als Faktor hinterlegen.
4. Plausibilität: Bisherige Lieferungen (3.000 l am 20.09.2024, 3.000 l am 04.08.2025) reichten ~14 Monate;
   Jahresverbrauch ~2.800 l. Bei q = 2,38 l/h wären das ~1.180 Brennerstunden/Jahr (**abgeleitet**, nicht gemessen) –
   ein Jahreswert der Brennerstunden aus der Regelung zeigt sofort, ob q in der richtigen Größenordnung liegt.

### Tankprognose (geplant)

```
Restinhalt = Inhalt_Anfang + Lieferungen − q × (Brennerstunden_jetzt − Brennerstunden_Anfang)
```

Warnschwellen laut Plan: **Vorwarnung 1.500 l**, **dringend 800 l**. Ein Vorschlag für einen HA-Template-Sensor,
noch **nicht eingerichtet** und mit **ungeprüfter** Entity-ID:

```yaml
template:
  - sensor:
      - name: Heizöl Restinhalt (Brennerstunden)
        unit_of_measurement: l
        state: >
          {% set h = states('sensor.heizung_brennerstunden') | float(none) %}
          {% if h is none %}{{ none }}{% else %}
          {{ (1900 - 2.38 * (h - BRENNERSTUNDEN_BEI_PEILUNG)) | round(0) }}
          {% endif %}
```

`1900`, `2.38` und `BRENNERSTUNDEN_BEI_PEILUNG` sind Platzhalter – besser als `input_number`-Helfer anlegen, damit
Peilung und Lieferungen ohne YAML-Änderung nachgetragen werden können.
