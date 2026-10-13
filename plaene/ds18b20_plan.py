#!/usr/bin/env python3
# DS18B20 „Zirkulation Rücklauf“ an heizung-optolink — Löt- und Anschlussplan (A4), 13.10.2026
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle

fig = plt.figure(figsize=(8.27, 11.69)); ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 210); ax.set_ylim(0, 297); ax.axis("off")
T = lambda x, y, s, **k: ax.text(x, y, s, **{"fontsize": 9.5, "va": "center", **k})
def line(*p, **k): ax.plot([q[0] for q in p], [q[1] for q in p], **{"color": "black", "lw": 1.4, **k})
ROT, GELB, SCHW, GRUEN = "#d62728", "#e6b800", "black", "#2ca02c"

T(12, 284, "DS18B20 „Zirkulation Rücklauf“ – Löt- und Anschlussplan", fontsize=16, fontweight="bold")
T(12, 277, "ESP32 heizung-optolink (192.168.178.193) · GPIO4 · 4,7-kΩ-Pull-up · Stand 13.10.2026", fontsize=8.5)

# ---------- 1. Kabelende löten ----------
T(12, 266, "1  Widerstand ans Kabelende löten (ESP-Seite, NICHT am Fühler)", fontsize=12, fontweight="bold")
x0 = 20
ax.add_patch(Rectangle((x0 - 8, 222), 10, 34, color="#bbb")); T(x0 - 7, 218, "Kabel\nzum Fühler", fontsize=7.5, va="top")
ys = {"rot": 251, "gelb": 237, "schwarz": 226}
for name, y in ys.items():
    c = {"rot": ROT, "gelb": GELB, "schwarz": SCHW}[name]
    line((x0, y), (120, y), color=c, lw=3)
    T(x0 + 3, y + 3, name, fontsize=8, color=c if name != "gelb" else "#9a7a00", fontweight="bold")
# Widerstand zwischen rot und gelb
xr = 80
line((xr, ys["rot"]), (xr, 247)); line((xr, 241), (xr, ys["gelb"]))
ax.add_patch(Rectangle((xr - 2.2, 241), 4.4, 6, fill=True, color="#d9c7a0", ec="black", lw=1.2))
for yy, cc in ((246, "yellow"), (244.5, "purple"), (243, "red")): line((xr - 2.2, yy), (xr + 2.2, yy), color=cc, lw=1.5)
ax.add_patch(Circle((xr, ys["rot"]), 1.1, color="black")); ax.add_patch(Circle((xr, ys["gelb"]), 1.1, color="black"))
T(xr + 4, 244, "4,7 kΩ\n(gelb-violett-rot)", fontsize=8)
T(xr - 26, 260, "Lötstellen  ●", fontsize=8)
# Enden
T(124, ys["rot"], "→ Wago „3,3 V“", fontsize=9, color=ROT, fontweight="bold")
T(124, ys["gelb"], "→ Pin 4", fontsize=9, color="#9a7a00", fontweight="bold")
T(124, ys["schwarz"], "→ GND", fontsize=9, fontweight="bold")
T(12, 207, "So geht’s:", fontsize=9.5, fontweight="bold")
schritte = [
    "a) ERST Schrumpfschläuche aufs Kabel schieben: 1 dicker übers Ganze, 2 dünne für die Lötstellen.",
    "b) Rot, gelb, schwarz am Ende je ca. 5 mm abisolieren und verzinnen.",
    "c) Widerstand: ein Bein an ROT, das andere an GELB löten (an GELB zusammen mit dem Jumperkabel).",
    "    Richtung egal, Beine kurz halten. Rot bleibt ein blankes Ende für den Wago.",
    "d) Lötstellen einzeln isolieren, dann den dicken Schlauch über Widerstand + beide Stellen.",
    "e) Kabelenden für den ESP: Jumperkabel mit BUCHSE anlöten (gelb, schwarz) – rot kommt in den Wago.",
    "f) Mit dem Multimeter prüfen: rot ↔ gelb ≈ 4,7 kΩ. rot ↔ schwarz und gelb ↔ schwarz: KEIN Durchgang.",
]
for i, s in enumerate(schritte): T(14, 200 - i * 6, s, fontsize=8.6)

# ---------- 2. Anschluss am ESP32 ----------
T(12, 152, "2  Anschluss am ESP32 (USB vorher ab, Lesekopf NICHT bewegen)", fontsize=12, fontweight="bold")
bx, by = 70, 60
ax.add_patch(FancyBboxPatch((bx, by), 50, 84, boxstyle="round,pad=1", fc="#eef3fa", ec="black"))
T(bx + 25, by + 80, "ESP32 DevKitC\nAntenne oben, USB unten", fontsize=7.5, ha="center")
links = ["3V3", "EN", "36", "39", "34", "35", "32", "33", "25", "26", "27", "14", "12", "GND"]
rechts = ["GND", "23", "22", "TX", "RX", "21", "GND", "19", "18", "5", "17", "16", "4", "0"]
for i, (l, r) in enumerate(zip(links, rechts)):
    y = by + 72 - i * 5
    ax.add_patch(Circle((bx + 3, y), 1.1, fc="white", ec="black")); ax.add_patch(Circle((bx + 47, y), 1.1, fc="white", ec="black"))
    T(bx + 6, y, l, fontsize=7.5); T(bx + 44, y, r, fontsize=7.5, ha="right")
def pin_y(i): return by + 72 - i * 5
# 3V3 → Wago
wx, wy = 34, pin_y(0) - 4
ax.add_patch(Rectangle((wx, wy - 6), 26, 14, fc="#f6f6f6", ec="black")); T(wx + 13, wy + 0.8, "Wago „3,3 V“", fontsize=8.5, ha="center", fontweight="bold")
line((bx + 3, pin_y(0)), (wx + 26, wy + 4), color=ROT, lw=2)
T(wx + 27, wy + 14, "neue Leitung\nzum 3V3-Pin", fontsize=7, color=ROT)
line((wx, wy + 4), (4, wy + 4), color=ROT, lw=2); T(4, wy + 11, "rot vom Lesekopf\n(vom 3V3-Pin abziehen)", fontsize=7, color=ROT)
line((wx, wy - 2), (4, wy - 2), color=ROT, lw=2); T(4, wy - 9, "rot vom Fühler (mit Widerstand)", fontsize=7, color=ROT)
# Pin 4 (rechts 13.), GND (rechts 7.)
line((bx + 47, pin_y(12)), (165, pin_y(12)), color=GELB, lw=2.5); T(167, pin_y(12), "gelb (mit Widerstand)\n→ Pin 4", fontsize=8, color="#9a7a00", fontweight="bold")
line((bx + 47, pin_y(6)), (165, pin_y(6)), color=SCHW, lw=2.5); T(167, pin_y(6), "schwarz → GND\n(rechts, 7. von oben)", fontsize=8, fontweight="bold")
line((bx + 47, pin_y(11)), (150, pin_y(11)), color=GRUEN, lw=1.2, ls="--"); T(152, pin_y(11), "grün Kopf (bleibt)", fontsize=7, color=GRUEN)
line((bx + 47, pin_y(10)), (150, pin_y(10)), color=GELB, lw=1.2, ls="--"); T(152, pin_y(10), "gelb Kopf (bleibt)", fontsize=7, color="#9a7a00")
T(bx + 25, by - 6, "Pin 4 = rechte Reihe, 13. von oben, direkt UNTER Pin 16 (grün). Es zählt der Aufdruck.", fontsize=8, ha="center")
T(bx + 25, by - 11, "Achtung: Kopf-Gelb (17) und Fühler-Gelb (4) nicht verwechseln – Fühler-Kabel markieren.", fontsize=8, ha="center", color="firebrick")

# ---------- 3. Am Rohr ----------
T(12, 38, "3  Am Rohr", fontsize=12, fontweight="bold")
for i, s in enumerate([
    "Zirkulationsleitung vom Haus zurück zum Speicher, nahe der Zirkulationspumpe, nicht direkt am Speicher.",
    "Metallhülse längs flach aufs blanke Rohr, 2 Kabelbinder, Alu-Klebeband drüber – dann Rohrisolierung DARÜBER.",
    "Danach: USB wieder ein, Firmware mit one_wire + dallas_temp per OTA aufspielen; prüfen: Wert kommt an, Optolink läuft weiter.",
]): T(14, 31 - i * 6, s, fontsize=8.6)

fig.savefig("ds18b20-zirkulation-plan.pdf")
