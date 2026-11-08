# Intelligenter Wochen-Einkaufsassistent (Langelsheim)

Ein vollautomatischer Einkaufs- und Angebotsassistent für Familien in **Langelsheim (Niedersachsen)**. Er prüft wöchentlich die aktuellen Angebote, lädt verifizierte Originalprospekte herunter, extrahiert Grundpreise (€/kg, €/L) und erstellt einen interaktiven Wochenbericht mit Essensplanung.

---

## 🛒 Berücksichtigte Supermärkte (Region Langelsheim, PLZ 38685)
1. **Netto Marken-Discount** (Harzstraße / Lange Str., Langelsheim)
2. **ALDI Nord** (Filiale Langelsheim / Umkreis Goslar)
3. **PENNY** (Filiale Langelsheim / Umkreis)
4. **REWE** (Filiale Langelsheim / Goslar)

---

## 👨‍👩‍👦 Familien-Rahmenbedingungen
- **Haushalt:** 2 Erwachsene, 1 Kind (4 Jahre).
- **Wochenbudget:** ca. 100 Euro.
- **Küche:** Abwechslungsreiche Familienküche, kaum Fisch (Fischstäbchen erlaubt), Lieblingsgerichte: Bolognese & Tomatensoße, Vorratskochen & Einfrieren.

---

## 🚀 Schnellstart & Nutzung

### 1. Manuelle Ausführung (Testlauf)
```bash
# Prospekte für die aktuelle Woche herunterladen & prüfen
python scripts/download_prospekte.py

# Angebote & Grundpreise extrahieren
python scripts/extract_deals.py

# Visuellen HTML-Wochenbericht generieren
python scripts/generate_report.py
```

### 2. Projektstruktur
```
einkaufsassistent/
├── README.md                  # Projektübersicht & Anleitung
├── CHANGELOG.md               # Versionen & Änderungen
├── TODO.md                    # Aufgabenliste & Fortschritt
├── scripts/
│   ├── download_prospekte.py  # Autonomer Prospekt-Downloader
│   ├── extract_deals.py       # Extraktion von Produkten & Grundpreisen
│   └── generate_report.py     # HTML-Dashboard mit Produktbildern
└── Prospekte/
    └── 2026/
        └── KW_46/             # Lokale Originalprospekte & Wochenbericht
```
