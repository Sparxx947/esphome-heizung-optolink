// Optolink-Lesekopf + ESP32-Gehaeuse fuer Vitotronic 200 KW2 (Viessmann Vitola 111)
// Stand 04.10.2026 — Notiz project_oeltank_fuellstandsensor
//
// Teile (Auswahl ueber TEIL, oder alle nebeneinander mit TEIL="alle"):
//   "kopf"        Lesekopf (Front nach unten drucken)
//   "v_schluessel" Fuehrungs-V, wird in die Front gesteckt/geklebt und greift ins „Viessmann-V“
//   "kopf_deckel" Rueckdeckel des Lesekopfs mit Kabelauslass
//   "esp"         Gehaeuse fuer ESP32-DevKitC V4 (WROOM-32U), Magnete hinten fuer das Kesselblech
//   "esp_deckel"  Deckel dazu
//
// Optolink-Geometrie aus dem openv-Wiki (files/vito.scad): Optik-Fenster 14 mm auseinander
// (±7 mm), runde Auflageflaeche Ø34 mm, Fuehrungs-„V“ ragt hoechstens 8 mm in die Regelung.
// Vitotronic: LINKE Lampe (rot, Stoerung) = IR-Empfaenger → dort sitzt UNSERE IR-LED;
//             RECHTE Lampe (gruen, Betrieb) = IR-Sender → dort sitzt UNSER Fototransistor.
// „Links/rechts“ gilt mit Blick AUF die Regelung. Blickt man beim Aufsetzen auf die Rueckseite des
// Kopfs, stimmt die Seite ueberein: LED links, FT rechts (innen eingepraegt, „OBEN“ nach oben).
//
// VOR DEM DRUCK MESSEN (Messschieber) und unten anpassen:
//   - Abstand der beiden Lampen-Mitten an der Regelung   → fenster_abstand (Wiki: 14)
//   - ESP32-Platine Laenge x Breite                         → esp_l, esp_b (DevKitC V4 meist ~55 x 28)
// Material: PETG (Kesselnaehe), 0,2 mm Schicht, 3 Waende, ohne Stuetzen.
// Platine im ESP-Gehaeuse: liegt an beiden Stirnseiten auf je zwei Stuetzen ZWISCHEN den Stiftleisten
// (links/rechts der Mitte, Mitte frei fuer USB-Loetlaschen bzw. SMA-Mutter), bei Bedarf mit Heisskleber fixieren.

TEIL = "alle";

$fn = 64;

// ---------- Lesekopf ----------
kopf_d          = 34;     // Auflageflaeche
platte          = 4;      // Frontplatte; 3-mm-LED/FT liegen mit der Linse buendig
fenster_abstand = 14.4;   // Mitte-Mitte der Lampen, Jens gemessen 06.10. (Wiki: 14)
loch_d          = 3.2;    // 3 mm Bauteil + Spiel
kragen_d        = 4.1;    // Kragen am Bauteilfuss (3-mm-LEDs: ~3,8 mm)
kragen_t        = 1.2;    // Kragen-Anschlag von hinten
v_hoehe         = 6;      // wie weit der Fuehrungs-V-Steg vorsteht (max. 8)
v_breite        = 6.5;
v_dicke         = 1.6;    // Stegstaerke des V
v_versatz_y     = -1.5;   // V liegt minimal unter der Fensterlinie (wie vito.scad)
v_zapfen        = 2;      // Zapfen des V-Schluessels in der Front
wand            = 1.6;
kopf_tiefe      = 12;     // Hohlraum fuer Widerstaende + Loetstellen
magnet_d        = 10.3;   // Neodym 10 x 3 mm + Spiel
magnet_h        = 3.2;
magnet_haut     = 0.6;    // Restwand zur Front (Magnet haelt durch)
magnet_y        = 10.5;   // ober- und unterhalb der Fensterlinie
kabel_b         = 7;      // Auslass fuer 4 Litzen
kabel_h         = 4;

// ---------- ESP32-Gehaeuse ----------
esp_l   = 49.9;   // Platine 48,24 + USB-C-Ueberstand 1,6 (Jens gemessen 06.10.)
esp_b   = 28.2;   // Platine 28,15 (Jens gemessen 06.10.)
spiel   = 0.8;    // rundum
ew      = 2.0;    // Wandstaerke
boden   = 4.0;    // 07.10.: war 2,0 → Magnettaschen (3,2 tief) gingen DURCH den Boden; jetzt 0,8 mm Restwand
auflage_h = 17;   // Platinenunterkante ueber Boden: Stiftleisten + Dupont-Buchsen darunter
auflage_t = 4.5;  // wie weit die Auflagen unter die Platinen-Stirnseiten greifen
innen_h = 27;     // Innenhoehe bis Deckel
usb_b = 12; usb_h = 7;          // Ausschnitt fuer USB-C-Stecker (mit Tuelle)
usb_ueber_platte = 1.6;         // Mitte USB-C ueber Platinenoberseite (ca.)
sma_d = 6.6;                    // SMA-Buchse der Antennen-Kit-Pigtail (1/4"-Gewinde)
sma_z = 8;                      // Mitte SMA ueber Boden (unter der Platine)
sma_luecke = 12;                // freie Breite zwischen den Stuetzen: SMA-Mutter (SW 8, ueber Ecken ~9,2) bzw. Loetlaschen der USB-C-Buchse
stift_rand = 3.2;               // 07.10.: Stiftleisten laufen ueber die GANZE Platinenlaenge (19 x 2,54 = 48,3) —
                                // Reihen 1,4 mm vom Rand, Kunststoff + Dupont bis ~2,7 mm → Stuetzen bleiben 3,2 mm vom Laengsrand weg
dup_b = 12; dup_h = 6;          // Auslass fuer die 4 Dupont-Leitungen (seitlich unten)

iL = esp_l + 2*spiel;
iB = esp_b + 2*spiel;
aL = iL + 2*ew;
aB = iB + 2*ew;
aH = boden + innen_h;

// ===================================================================
module text_flach(t, s=3) {
    linear_extrude(0.6) text(t, size=s, font="Liberation Sans:style=Bold", halign="center", valign="center");
}

module v_steg(h, d) {
    // „V“ aus zwei Stegen, Spitze nach unten (-y)
    for (s=[-1,1])
        hull() {
            translate([0, -v_breite*0.55, 0]) cylinder(d=d, h=h, $fn=24);
            translate([s*v_breite/2, v_breite*0.45, 0]) cylinder(d=d, h=h, $fn=24);
        }
}

module kopf() {
    // Front liegt auf z=0 (zur Regelung) und wird so auch gedruckt: Front aufs Bett.
    difference() {
        union() {
            cylinder(d=kopf_d, h=platte + kopf_tiefe);
        }
        // Hohlraum von hinten
        translate([0,0,platte]) cylinder(d=kopf_d-2*wand, h=kopf_tiefe+1);
        // Optik-Fenster durchgehend + Kragenanschlag von hinten
        for (x=[-fenster_abstand/2, fenster_abstand/2]) {
            translate([x,0,-1]) cylinder(d=loch_d, h=platte+2);
            translate([x,0,platte-kragen_t]) cylinder(d=kragen_d, h=kragen_t+1);
        }
        // Magnettaschen von hinten, vorn bleibt magnet_haut stehen
        for (y=[-magnet_y, magnet_y])
            translate([0,y,magnet_haut]) cylinder(d=magnet_d, h=magnet_h+5);
        // Kabelauslass oben in der Wand
        translate([-kabel_b/2, kopf_d/2-wand-1, platte+kopf_tiefe-kabel_h]) cube([kabel_b, wand+2, kabel_h+1]);
        // Tasche fuer den Zapfen des V-Schluessels (von vorn)
        translate([0, v_versatz_y, -0.01]) v_steg(v_zapfen+0.2, v_dicke+0.35);
        // Kennzeichnung innen auf der Frontplatte, lesbar von hinten
        translate([-fenster_abstand/2, -3.4, platte-0.4]) text_flach("LED", 2.0);
        translate([ fenster_abstand/2, -3.4, platte-0.4]) text_flach("FT", 2.0);
        translate([0, 3.6, platte-0.4]) text_flach("OBEN", 1.8);
    }
}

module v_schluessel() {
    v_steg(v_hoehe + v_zapfen, v_dicke);
}

module kopf_deckel() {
    d_innen = kopf_d - 2*wand - 0.4;   // Steckpassung
    difference() {
        union() {
            cylinder(d=kopf_d, h=1.6);
            translate([0,0,1.6]) difference() {
                cylinder(d=d_innen, h=3);
                translate([0,0,-1]) cylinder(d=d_innen-2.4, h=5);
            }
        }
        // Gegenstueck zum Kabelauslass im Steckkragen
        translate([-kabel_b/2, d_innen/2-3, 1.6]) cube([kabel_b, 4, 4]);
    }
}

// ===================================================================
module esp() {
    platte_ok = boden + auflage_h;           // Platinenunterkante
    usb_z = platte_ok + 1.6 + usb_ueber_platte;
    difference() {
        // Aussenkoerper mit abgerundeten Kanten
        hull() for (x=[2, aL-2], y=[2, aB-2]) translate([x,y,0]) cylinder(r=2, h=aH);
        // Innenraum
        translate([ew, ew, boden]) cube([iL, iB, innen_h+1]);
        // USB-C an der linken Stirnseite (x=0)
        translate([-1, aB/2-usb_b/2, usb_z-usb_h/2]) cube([ew+2, usb_b, usb_h]);
        // SMA-Antennenbuchse an der rechten Stirnseite, UNTER der Platine (dort ist Platz fuer die Mutter;
        // oben wuerde sie mit dem Steckrand des Deckels kollidieren)
        translate([aL-ew-1, aB/2, boden+sma_z]) rotate([0,90,0]) cylinder(d=sma_d, h=ew+2);
        // Dupont-Auslass seitlich unten (Langseite y=0), nahe der USB-Seite
        translate([ew+8, -1, boden+1]) cube([dup_b, ew+2, dup_h]);
        // Lueftungsschlitze in der Gegenseite
        for (i=[0:5]) translate([ew+10+i*6, aB-ew-1, boden+6]) cube([2.4, ew+2, 12]);
        // Magnettaschen im Boden (von unten), fuer das Stahlblech des Kessels
        for (x=[aL*0.25, aL*0.75]) translate([x, aB/2, -0.01]) cylinder(d=magnet_d, h=magnet_h);
        // Kennzeichnung
        translate([aL/2, aB/2, -0.01]) mirror([1,0,0]) linear_extrude(0.5)
            text("HEIZUNG", size=4, font="Liberation Sans:style=Bold", halign="center", valign="center");
    }
    // Stuetzen fuer die Platinen-Stirnseiten: je Stirnseite zwei, zwischen Stiftleiste und Mitte.
    // 07.10.: vorher durchgehende Auflage → die nach unten zeigenden Stifte sassen darauf auf.
    st_b = esp_b/2 - stift_rand - sma_luecke/2;      // Breite je Stuetze (~4,9 mm)
    for (x=[ew, ew+iL-auflage_t], s=[-1,1])
        translate([x, aB/2 + (s>0 ? sma_luecke/2 : -sma_luecke/2 - st_b), boden])
            cube([auflage_t, st_b, auflage_h]);
}

module esp_deckel() {
    difference() {
        union() {
            hull() for (x=[2, aL-2], y=[2, aB-2]) translate([x,y,0]) cylinder(r=2, h=1.8);
            // Steckrand
            translate([ew+0.25, ew+0.25, 1.8]) difference() {
                cube([iL-0.5, iB-0.5, 3]);
                translate([1.4,1.4,-1]) cube([iL-0.5-2.8, iB-0.5-2.8, 5]);
            }
        }
    }
}

// ===================================================================
if (TEIL == "kopf")        kopf();
if (TEIL == "v_schluessel") v_schluessel();
if (TEIL == "kopf_deckel") kopf_deckel();
if (TEIL == "esp")         esp();
if (TEIL == "esp_deckel")  esp_deckel();
if (TEIL == "alle") {
    kopf();
    translate([45,0,0]) kopf_deckel();
    translate([30,-28,0]) v_schluessel();
    translate([-40,30,0]) esp();
    translate([-40,-50,0]) esp_deckel();
}
