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
- [ ] Mindestens 20 echte Lebensmittelangebote aus den Prospekten extrahieren
- [ ] Grundpreise (€/kg bzw. €/L) mathematisch berechnen
- [ ] Angebote gegen Referenzpreise einstufen (SEHR GUTES SCHNÄPPCHEN, GUTES ANGEBOT, NORMALER PREIS)
- [ ] JSON-Datenstruktur absichern (`angebote.json`)

## Phase 3: Bildextraktion & Visueller Wochenbericht
- [ ] Bildausschnitte für die Top-Angebote sauber aus den PDFs ausschneiden
- [ ] Responsives HTML-Dashboard bauen (Übersicht, Top-Deals, Händlervergleich, Essensplan, Budget)
- [ ] Verifikation: Alle Bilder vorhanden, Prospekte direkt verlinkt und aufrufbar

## Phase 4: Automatisierung
- [ ] Erstellung der `sidecar.json` für den automatischen Sonntagsablauf
- [ ] Testlauf und Berechtigungskonfiguration
