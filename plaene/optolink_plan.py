import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch
fig = plt.figure(figsize=(8.27, 11.69)); ax = fig.add_axes([0,0,1,1]); ax.set_xlim(0,210); ax.set_ylim(0,297); ax.axis("off")
L = dict(color="black", lw=1.4)
def line(*pts, **kw): ax.plot([p[0] for p in pts],[p[1] for p in pts], **{**L, **kw})
def dot(x,y): ax.add_patch(Circle((x,y),0.9,color="black"))
def res(x,y1,y2,label):  # senkrechter Widerstand
    m=(y1+y2)/2; line((x,y1),(x,m+6)); line((x,m-6),(x,y2)); ax.add_patch(Rectangle((x-2.5,m-6),5,12,fill=False,lw=1.4))
    ax.text(x+4.5,m,label,va="center",fontsize=11,fontweight="bold")
def pfeile(x,y,richtung):
    for d in (0,4):
        if richtung=="raus": ax.add_patch(FancyArrowPatch((x+3,y+d),(x+10,y+d+5),arrowstyle="-|>",mutation_scale=9,color="crimson",lw=1.1))
        else: ax.add_patch(FancyArrowPatch((x-10,y+d+5),(x-3,y+d),arrowstyle="-|>",mutation_scale=9,color="crimson",lw=1.1))
T=lambda x,y,s,**k: ax.text(x,y,s,**{"fontsize":10,**k})
T(15,282,"Optolink-Lesekopf – Schaltplan",fontsize=18,fontweight="bold")
T(15,274,"Vitotronic 200 KW2 · ESP32-WROOM-32U DevKitC · ESPHome heizung-optolink (192.168.178.193) · Stand 06.10.2026",fontsize=8.5)

# Schienen
y3, yg = 240, 150
T(12,y3+2,"3V3",fontsize=12,fontweight="bold",color="firebrick"); line((25,y3),(170,y3),color="firebrick",lw=2)
T(12,yg-1,"GND",fontsize=12,fontweight="bold"); line((25,yg),(170,yg),lw=2)

# --- Sender: 3V3 - 220 - LED - GPIO17
xs=60; dot(xs,y3); res(xs,y3,212,"220 Ω")
# LED (Anode oben, Kathode unten), Dreieck nach unten
line((xs,212),(xs,203)); ax.add_patch(Polygon([(xs-5,203),(xs+5,203),(xs,195)],closed=True,fill=False,lw=1.4)); line((xs-5,195),(xs+5,195)); line((xs,195),(xs,180))
pfeile(xs+4,197,"raus")
T(xs-36,201,"IR-LED 940 nm\n(Chanzon 3 mm)",fontsize=8.5)
T(xs+8,207,"Anode (langes Bein)",fontsize=8); T(xs+8,190,"Kathode (kurz, flache Seite)",fontsize=8)
line((xs,180),(xs,170)); ax.add_patch(Rectangle((xs-14,162),28,8,fill=False,lw=1.4)); T(xs-12,164.5,"GPIO17 (TX)",fontsize=9,fontweight="bold")
T(xs-30,154,"SENDEN → zur LINKEN Lampe",fontsize=8.5,color="crimson")

# --- Empfaenger: 3V3 - 10k - Knoten - GPIO16 ; Knoten - Kollektor FT - Emitter - GND
xr=140; dot(xr,y3); res(xr,y3,212,"10 kΩ")
line((xr,212),(xr,200)); dot(xr,200); line((xr,200),(xr-25,200),(xr-25,176))
ax.add_patch(Rectangle((xr-39,168),28,8,fill=False,lw=1.4)); T(xr-37,170.5,"GPIO16 (RX)",fontsize=9,fontweight="bold")
# Fototransistor (Kreis, Basis-Pfeile)
cx,cy=xr,183; ax.add_patch(Circle((cx,cy),7,fill=False,lw=1.4))
line((xr,200),(xr,190)); line((cx-2,190),(cx-2,176)) # Basisbalken
line((xr,190),(cx-2,186)); line((cx-2,180),(xr,176)); line((xr,176),(xr,yg)); dot(xr,yg)
ax.add_patch(FancyArrowPatch((cx-2,180),(xr+0.3,176.3),arrowstyle="-|>",mutation_scale=8,color="black",lw=1))
pfeile(cx-7,186,"rein")
T(xr+9,190,"Kollektor (meist kurzes\nBein – prüfen!)",fontsize=8); T(xr+9,173,"Emitter (meist langes Bein)",fontsize=8)
T(xr+9,182,"Fototransistor\nKingbright L-93DP3C",fontsize=8.5)
T(xr-30,154,"EMPFANGEN ← von der RECHTEN Lampe",fontsize=8.5,color="crimson")

# Hinweis Beinchen
T(15,135,"Achtung Beinchen: Bei der LED ist das LANGE Bein die Anode (+). Beim Fototransistor ist meist das LANGE Bein der Emitter (−)\n"
        "→ vor dem Löten am Datenblatt bzw. mit dem Multimeter (Diodentest) prüfen. Falsch herum: nichts kaputt, aber keine Daten.",fontsize=8.3)

# Tabelle Anschluesse
T(15,118,"Verbindung Lesekopf ↔ ESP32 (4 Dupont-Leitungen, Buchse–Buchse)",fontsize=11,fontweight="bold")
rows=[("Leitung","ESP32-Pin","Im Lesekopf an","Farbvorschlag"),
      ("1","3V3","220 Ω (LED) + 10 kΩ (FT)","rot"),
      ("2","GND","Emitter Fototransistor","schwarz"),
      ("3","GPIO17 / „TX2“ / „17“","Kathode IR-LED","gelb"),
      ("4","GPIO16 / „RX2“ / „16“","Kollektor FT + 10 kΩ","grün")]
x0=[15,35,85,155]; yy=110
for i,r in enumerate(rows):
    for j,c in enumerate(r): T(x0[j],yy-i*7,c,fontsize=9,fontweight="bold" if i==0 else "normal")
    line((15,yy-i*7-2.5),(195,yy-i*7-2.5),lw=0.6)

# Kopf-Ansicht
T(15,68,"Lage im Lesekopf (Blick AUF die Regelung = Blick auf die Rückseite des Kopfs)",fontsize=11,fontweight="bold")
ax.add_patch(Circle((60,40),17,fill=False,lw=1.4)); ax.add_patch(Circle((52.8,40),1.6,color="crimson")); ax.add_patch(Circle((67.2,40),1.6,color="seagreen"))
T(44,33,"LED",fontsize=9); T(64,33,"FT",fontsize=9); T(55,55,"OBEN",fontsize=8); line((52.8,44),(67.2,44),lw=0.6); T(53.5,45.2,"14,4 mm",fontsize=7.5)
T(85,49,"• LINKE Lampe (rot, Störung) = Empfänger der Regelung\n   → dort unsere IR-LED",fontsize=8.8)
T(85,39,"• RECHTE Lampe (grün, Betrieb) = Sender der Regelung\n   → dort unser Fototransistor",fontsize=8.8)
T(85,31,"• Abstand Mitte–Mitte 14,4 mm (gemessen 06.10.), Kopf-STL ist angepasst",fontsize=8.8)
T(85,25,"• Widerstände sitzen im Kopf, nur 4 Leitungen zum ESP-Gehäuse",fontsize=8.8)
T(15,4,"Quelle: Schaltung nach VitoWiFi/openv-Wiki („Die Optolink-Schnittstelle“, „ESPHome-Optolink“), festgelegt 04.10.\nin ~/esphome/heizung-optolink.yaml. "
        "UART 4800 8E2, Protokoll KW. Inbetriebnahme: optolink → logger: true,\nWerte mit der Anzeige der Regelung vergleichen.",fontsize=7.5,color="dimgray")
fig.savefig("optolink-schaltplan.pdf")
