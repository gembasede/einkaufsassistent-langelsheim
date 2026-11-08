# Intelligenter Wochen-Einkaufsassistent (Langelsheim)

Ein vollautomatischer Einkaufs- und Angebotsassistent für Familien in **Langelsheim (Niedersachsen)**. Er prüft wöchentlich die aktuellen Angebote, lädt verifizierte Originalprospekte herunter, extrahiert Grundpreise (€/kg, €/L), generiert eine mobile Web-App mit Blätterkatalog & Einkaufsliste und integriert sich in die **FamilienZentrale**.

---

## 🛒 Berücksichtigte Supermärkte (Region Langelsheim, PLZ 38685)
1. **Netto Marken-Discount** (Ringstraße 34a, Langelsheim)
2. **ALDI Nord** (Lange Straße 62, Langelsheim)
3. **PENNY** (Lange Straße 64, Langelsheim)
4. **REWE** (Lange Str. 60, Langelsheim)

---

## 👨‍👩‍👦 Familien-Rahmenbedingungen
- **Haushalt:** 2 Erwachsene, 1 Kind (4 Jahre).
- **Wochenbudget:** ca. 100 Euro.
- **Küche:** Abwechslungsreiche Familienküche, kaum Fisch (Fischstäbchen erlaubt), Lieblingsgerichte: Bolognese & Tomatensoße, Vorratskochen & Einfrieren.

---

## 📱 Mobile Web-App (PWA)
Die Web-App im Ordner `web/` ist speziell für Smartphones optimiert:
1. **🔥 Angebote:** Schnäppchen mit Originalbildern, Grundpreisen und Marktfiltern.
2. **🛒 Interaktive Einkaufsliste:** Deals mit 1 Klick hinzufügen, nach Supermarkt sortiert abhaken und Live-Gesamtsumme sehen (gespeichert in `localStorage`).
3. **📖 Prospekt-Blätterkatalog:** Schnelles, flüssiges Durchblättern aller 195 Prospektseiten direkt im Browser ohne 10-MB-Downloads.
4. **🍳 Essensplan:** 4-Tage-Plan mit automatischer Zutatenauswahl für die Einkaufsliste.

### Schneller Start der Web-App
```bash
# Lokale Ansicht direkt im Browser öffnen
start web/index.html

# Oder als lokaler Server (für Zugriff im Heim-WLAN):
python -m http.server 8080 --directory web
```

### Vercel Deployment & GitHub Repository
- **GitHub Repository:** `https://github.com/gembasede/einkaufsassistent-langelsheim`
- **Vercel Standalone Projekt:** `einkaufsassistent-langelsheim`
- **Live-URL:** `https://einkaufsassistent-langelsheim.vercel.app`
- **Routing:** Automatische Weiterleitung via `vercel.json` im Hauptverzeichnis direkt auf `web/index.html`.
- Deployment via Git: Ein `git push` zu GitHub triggert automatisch den Vercel-Livebuild.

---

## 🚀 Skripte & Automatisierung

```bash
# 1. Prospekte herunterladen & verifizieren
python scripts/download_prospekte.py

# 2. Angebote & Grundpreise extrahieren
python scripts/extract_deals.py

# 3. Produktbilder zuschneiden
python scripts/extract_images.py

# 4. Wochenbericht (HTML & PDF) erstellen
python scripts/generate_report.py

# 5. Mobile Web-App aktualisieren
python scripts/generate_web_app.py
```

---

## 📁 Projektstruktur
```
einkaufsassistent/
├── README.md                  # Projektübersicht & Anleitung
├── CHANGELOG.md               # Versionen & Änderungen
├── TODO.md                    # Aufgabenliste & Fortschritt
├── web/                       # Mobile Web-App (PWA)
│   ├── index.html             # App mit Tabs (Deals, Liste, Viewer, Rezepte)
│   ├── manifest.json          # PWA-Konfiguration (Home-Screen-Installation)
│   ├── vercel.json            # Vercel Deployment Konfiguration
│   ├── images/                # 15 zugeschnittene Original-Produktbilder
│   └── brochures/             # 195 optimierte Blätterseiten + Original-PDFs
├── scripts/
│   ├── download_prospekte.py  # Autonomer PDF-Downloader
│   ├── extract_deals.py       # Extraktion & Grundpreisberechnung
│   ├── extract_images.py      # Zuschneiden der Produktbilder
│   ├── generate_report.py     # HTML & PDF Wochenbericht
│   └── generate_web_app.py    # Generator für die Web-App & Blätterseiten
└── Prospekte/
    └── 2026/
        └── KW_46/             # Lokales Archiv der Original-PDFs & Berichte
```
