#!/usr/bin/env python3
# Belegungsblatt ESP32 heizung-optolink: Lesekopf + DS18B20 (A4). Stand 13.10.2026.
# Aufruf im Zielordner: python3 esp32_belegung_plan.py  → esp32-belegung.pdf
import sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle

ROT, SCHW, GELB, GRUEN, FUEHLER = "#ff5a5a", "#333333", "#ffd92f", "#1fb894", "#8a5cc7"
fig = plt.figure(figsize=(8.27, 11.69)); ax = fig.add_axes((0, 0, 1, 1))
ax.set_xlim(0, 210); ax.set_ylim(0, 297); ax.axis("off")
T = lambda x, y, s, **k: ax.text(x, y, s, **{"fontsize": 8, "va": "center", **k})

T(105, 287, "ESP32 – Optolink-Lesekopf + Zirkulationsfühler", fontsize=15, fontweight="bold", ha="center")
T(105, 280, "ESP32-WROOM-32U DevKitC · heizung-optolink (192.168.178.193) · Stand 13.10.2026 (DS18B20 ergänzt)", fontsize=7.5, ha="center")
T(105, 275, "Board so hinlegen: Bauteilseite nach OBEN, Antennenbuchse/Modul OBEN, USB-C UNTEN.", fontsize=8.5, ha="center")

# Board
bx, by, bw, bh = 72, 105, 66, 160
ax.add_patch(FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.8", fc="#1f4e79", ec="black"))
ax.add_patch(Rectangle((bx + 13, by + bh - 34), 40, 30, fc="#bbbbbb", ec="black"))
T(bx + 33, by + bh - 20, "ESP32-WROOM-32U\n(Modul)", fontsize=6.5, ha="center")
ax.add_patch(Circle((bx + 45, by + bh - 8), 2.3, fc="gold", ec="black")); T(bx + 48.5, by + bh - 8, "Antenne", fontsize=5.5, color="white")
ax.add_patch(Rectangle((bx + 27, by - 6), 12, 7, fc="#aaaaaa", ec="black")); T(bx + 33, by - 9, "USB-C", fontsize=6.5, ha="center")
T(bx + 33, by + bh - 38, "Stiftleisten", fontsize=5.5, ha="center", color="white")
links = ["3V3", "EN", "VP 36", "VN 39", "34", "35", "32", "33", "25", "26", "27", "14", "12", "GND", "13", "D2", "D3", "CMD", "5V"]
rechts = ["GND", "23", "22", "TX 1", "RX 3", "21", "GND", "19", "18", "5", "17", "16", "4", "0", "2", "15", "D1", "D0", "CLK"]
y0, dy = by + bh - 44, 6.0
def py(i): return y0 - i * dy
farbe_l = {0: ROT}; farbe_r = {0: SCHW, 6: SCHW, 10: GELB, 11: GRUEN, 12: FUEHLER}
fett = {"3V3", "GND", "17", "16", "4", "TX 1", "RX 3", "5V"}
for i, (l, r) in enumerate(zip(links, rechts)):
    ax.add_patch(Circle((bx + 4, py(i)), 1.6, fc=farbe_l.get(i, "white"), ec="black"))
    ax.add_patch(Circle((bx + bw - 4, py(i)), 1.6, fc=farbe_r.get(i, "white"), ec="black"))
    T(bx + 7, py(i), l, fontsize=6, color="white", fontweight="bold" if l in fett else "normal")
    T(bx + bw - 7, py(i), r, fontsize=6, color="white", ha="right", fontweight="bold" if r in fett else "normal")
T(bx + bw + 4, py(3), "← NICHT!", fontsize=6.5, color="firebrick", fontweight="bold")
T(bx + bw + 4, py(4), "← NICHT!", fontsize=6.5, color="firebrick", fontweight="bold")

def kasten(x, y, txt, fc, tc="black", w=36, h=11):
    ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h, boxstyle="round,pad=0.6", fc=fc, ec="black"))
    T(x + w / 2, y, txt, fontsize=6.8, ha="center", fontweight="bold", color=tc)
def leitung(x1, y1, x2, y2, c, lw=2.2): ax.plot([x1, x2], [y1, y2], color=c, lw=lw, solid_capstyle="round")

# links: Wago 3,3 V
wy = py(0) + 2
ax.add_patch(FancyBboxPatch((40, wy - 7), 18, 14, boxstyle="round,pad=0.5", fc="#f2f2f2", ec="black"))
T(49, wy + 3, "WAGO", fontsize=6.5, ha="center", fontweight="bold"); T(49, wy - 2.5, "3,3 V", fontsize=6.5, ha="center")
leitung(58, wy, bx + 4, py(0), ROT)
kasten(3, wy + 9, "ROT Kopf\n3,3 V", ROT, w=30); leitung(33, wy + 9, 40, wy + 3, ROT)
kasten(3, wy - 9, "ROT Fühler\n3,3 V", ROT, w=30); leitung(33, wy - 9, 40, wy - 3, ROT)
# rechts
kasten(166, py(0), "SCHWARZ Kopf\nGND", SCHW, tc="white", w=40); leitung(bx + bw - 4, py(0), 166, py(0), SCHW)
kasten(166, py(6), "SCHWARZ Fühler\nGND", SCHW, tc="white", w=40); leitung(bx + bw - 4, py(6), 166, py(6), SCHW)
kasten(166, py(10) + 5, "GELB Kopf\nLED (Senden)", GELB, w=40); leitung(bx + bw - 4, py(10), 166, py(10) + 5, GELB)
kasten(166, py(11) - 4, "GRÜN Kopf\nFototransistor", GRUEN, w=40); leitung(bx + bw - 4, py(11), 166, py(11) - 4, GRUEN)
kasten(166, py(12) - 14, "GELB Fühler (markiert)\nDaten DS18B20", FUEHLER, tc="white", w=40); leitung(bx + bw - 4, py(12), 166, py(12) - 14, FUEHLER)

# Tabelle
rows = [("Kabel", "Funktion", "ESP32-Pin (Aufdruck)", None),
        ("rot Kopf", "3,3 V Lesekopf", "3V3 über Wago (links, ganz oben)", ROT),
        ("schwarz Kopf", "GND Lesekopf", "GND (rechts, ganz oben)", SCHW),
        ("gelb Kopf", "IR-LED – Senden (TX)", "17 (rechts, 11. von oben)", GELB),
        ("grün Kopf", "Fototransistor – Empfangen (RX)", "16 (rechts, 12. von oben)", GRUEN),
        ("rot Fühler", "3,3 V DS18B20", "3V3 über Wago", ROT),
        ("schwarz Fühler", "GND DS18B20", "GND (rechts, 7. von oben)*", SCHW),
        ("gelb Fühler", "Daten DS18B20 (4,7 kΩ nach rot)", "4 (rechts, 13. von oben)", FUEHLER)]
tx, ty, rh = 20, 88, 6.2
cw = [32, 62, 76]
for r, (a, b, c, col) in enumerate(rows):
    y = ty - r * rh; x = tx
    for k, txt in enumerate((a, b, c)):
        fc = "#e6e6e6" if r == 0 else (col if k == 0 else "white")
        ax.add_patch(Rectangle((x, y - rh / 2), cw[k], rh, fc=fc, ec="black", lw=0.6))
        tc = "white" if (k == 0 and col in (SCHW, FUEHLER)) else "black"
        T(x + cw[k] / 2, y, txt, fontsize=6.6, ha="center", color=tc, fontweight="bold" if (r == 0 or k == 2) else "normal")
        x += cw[k]

notes = ["* Jeder GND-Pin geht (auch links, 6. von unten). 5V bleibt FREI – Kopf und Fühler laufen nur mit 3,3 V.",
         "Der DevKitC hat nur EINEN 3V3-Pin → Lesekopf und Fühler teilen ihn über die Wago-Klemme.",
         "Fühler: 4,7-kΩ-Widerstand zwischen gelb und rot ist am Kabelende eingelötet (nicht am ESP).",
         "ACHTUNG: zwei gelbe Adern! Kopf-Gelb → 17, Fühler-Gelb → 4. Fühlerkabel markieren.",
         "ACHTUNG: „TX“/„RX“ (GPIO1/3) sind die USB-Leitungen – NICHT benutzen.",
         "Kopf an der Regelung: LED vor der linken roten Lampe, Fototransistor vor der rechten grünen. Kopf nicht verschieben.",
         "Pin-Lage = Standard DevKitC V4 (38 Pins). Bei Abweichung zählt der AUFDRUCK auf der Platine, nicht die Position."]
for i, n in enumerate(notes):
    T(20, 34 - i * 4.4, n, fontsize=6.6, color="firebrick" if n.startswith("ACHTUNG") else "black",
      fontweight="bold" if n.startswith("ACHTUNG") else "normal")

fig.savefig(sys.argv[1] if len(sys.argv) > 1 else "esp32-belegung.pdf")
if len(sys.argv) > 2: fig.savefig(sys.argv[2], dpi=75)
