# Projekt-Aufgaben (TODO)

## Phase 1: Prospekt-Recherche & Downloadtest (KW 46 / Langelsheim)
- [x] Projektstruktur und Dokumentation anlegen
- [x] PyMuPDF und Pillow installieren
- [x] Netto Marken-Discount Prospekt finden, herunterladen & verifizieren (10.55 MB, 75 S.)
- [x] ALDI Nord Prospekt finden, herunterladen & verifizieren (6.16 MB, 44 S.)
- [x] PENNY Prospekt finden, herunterladen & verifizieren (6.81 MB, 48 S.)
- [x] REWE Prospekt finden, herunterladen & verifizieren (3.83 MB, 28 S.)
- [x] Downloadstatus-Matrix erstellen und in `download_status.json` dokumentieren

## Phase 2: Preiserkennung & Grundpreis-Berechnung
- [x] 31 echte Lebensmittelangebote aus den Prospekten extrahieren
- [x] Grundpreise (€/kg bzw. €/L) mathematisch berechnen und validieren
- [x] Angebote gegen Referenzpreise einstufen (15x SEHR GUTES SCHNÄPPCHEN, 13x GUTES ANGEBOT, etc.)
- [x] JSON-Datenstruktur absichern (`angebote.json`)

## Phase 3: Bildextraktion & Visueller Wochenbericht
- [x] Bildausschnitte für die Top-Angebote sauber aus den PDFs zuschneiden (`extract_images.py`)
- [x] Responsives HTML-Dashboard bauen (`wochenbericht.html`)
- [x] Druckfertigen PDF-Bericht generieren (`wochenbericht.pdf` via Chrome Headless)
- [x] Direkter Händlervergleich, 4-Tage-Familienessensplan und Budget-Kalkulation integriert

## Phase 4: Automatisierung
- [x] Konfiguration der Automatisierung `Wöchentlicher Einkaufsassistent (Langelsheim)`
- [x] Verknüpfung im Automations-Dashboard zur manuellen Aktivierung

## Phase 5: Mobile Web-App (PWA) & FamilienZentrale Integration
- [x] Mobile Web-App mit 4 Tabs (Deals, Checkliste, Blätterkatalog, Essensplan) in `web/index.html`
- [x] Vorgerenderte Produktkarten (SSR-Style) für schnelles Laden
- [x] Interaktive Einkaufsliste mit Checkboxen, Summenrechner und `localStorage`-Speicherung
- [x] Mobiler Prospekt-Blätterkatalog (195 optimierte Web-Seiten für ALDI, PENNY, Netto, REWE)
- [x] PWA-Manifest (`manifest.json`) und Vercel-Konfiguration (`vercel.json`)
- [x] Nahtlose Verlinkung als Hero-Banner in `FamilienZentrale` (`src/app/prospekte/page.tsx`)
- [x] Vollständiger TypeScript-Typcheck fehlerfrei bestanden
- [x] Live-Bereitstellung in `public/angebots-radar/` für Vercel-Hosting via `git push`
- [x] Vercel-Projekt `einkaufsassistent-langelsheim` angelegt und Team-Autorisierung abgeschlossen
