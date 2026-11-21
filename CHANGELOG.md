# Changelog

Alle relevanten Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

## [Unreleased]
### Added
- **Schnell-Eingabe direkt im Prospekt-Blätterkatalog (Floating `+`-Button & Bottom Sheet):**
  - Über jeder Prospektseite schwebt unten rechts ein grüner `+`-Knopf, der ein kleines Eingabefenster von unten über den Prospekt schiebt, ohne den Tab zu wechseln.
  - Felder für freien Artikelnamen, vorausgewählten Markt (passend zum gerade offenen Prospekt, frei änderbar) und optionalen Preis (rechnet direkt ins 100-€-Budget mit ein).
  - Nach dem Tippen auf „+ Hinzufügen“ bleibt das Fenster offen, leert Artikel & Preis für den nächsten Eintrag und zeigt kurz eine Bestätigung an.
  - **Prospekt-Leseposition merken:** Die App speichert die zuletzt gelesene Seite pro Markt dauerhaft im Browser (`localStorage`) und startet bei einer neuen Kalenderwoche automatisch wieder bei Seite 1.
  - Dynamische Kopfzeile (`KW` & Gültigkeitszeitraum) und echte Seitenzahlen in der Markt-Auswahl (kein Hardcoding mehr).
- **Dynamische Wochenberechnung & Brandneue Prospekte (KW 48, 23.11.2026 – 28.11.2026):**
  - Alle Skripte (`download_prospekte.py`, `extract_deals.py`, `extract_images.py`, `generate_report.py`, `generate_web_app.py`) von starrem Hardcoding auf automatische Wochenberechnung umgestellt.
  - An Samstagen/Sonntagen wird automatisch der kommende Montag für die neue Einkaufswoche berechnet.
  - Brandneue Originalprospekte für KW 48 heruntergeladen und physisch verifiziert:
    - ALDI Nord: 49 Seiten (7.01 MB)
    - PENNY: 17 Seiten (2.53 MB)
    - Netto Marken-Discount: 36 Seiten (5.26 MB)
    - REWE: 32 Seiten (5.12 MB)
  - 27 aktuelle Angebote validiert und mathematische Grundpreise nachgerechnet (u. a. Bärenmarke Milch 0,88 €, Minutensteaks 5,73 €/kg, Netto Hackfleisch 6,98 €/kg, Bauer Joghurt 0,39 €).
  - 14 hochauflösende Original-Produktbilder für die Highlights zugeschnitten.
  - Neuer visueller Wochenbericht (`wochenbericht.html`, `wochenbericht.pdf`) für KW 48 erstellt.
  - Mobile PWA Web-App (`web/index.html`) und 134 Blätterseiten für den Live-Betrieb auf Vercel synchronisiert.
- Wöchentlicher Sonntags-Einkaufscheck für Langelsheim erfolgreich und vollständig automatisiert durchlaufen:
  - Download & Verifikation aller 4 Händler-Originalprospekte (ALDI Nord, PENNY, Netto Marken-Discount, REWE).
  - Validierung von 31 Angeboten inklusive mathematischer Grundpreisprüfung.
  - Automatischer Zuschnitt von 15 hochauflösenden Produktbildern (200 DPI).
  - Neuer visueller Wochenbericht als interaktives HTML und druckfertiges PDF (`wochenbericht.html`, `wochenbericht.pdf`).
  - Mobile PWA Web-App (`web/index.html`) und Blätterkatalog-Rendern aller Seiten synchronisiert.
- `.gitignore` um temporäre Download-Verzeichnisse (`_temp_pages/`) ergänzt.
- Initiales Projekt-Setup im Verzeichnis `einkaufsassistent`.
- Grundstruktur mit `scripts/` und `Prospekte/`.
- Dokumentation (`README.md`, `CHANGELOG.md`, `TODO.md`).
- Paketinstallation für `PyMuPDF` und `Pillow` zur PDF- und Bildverarbeitung.
- Skript `scripts/download_prospekte.py` für automatischen Download, Assemblierung und Verifikation.
- Phase 1 erfolgreich abgeschlossen: Alle 4 Prospekte für KW 46 (09.11.2026 - 14.11.2026) für Langelsheim heruntergeladen und verifiziert (`ALDI_Nord.pdf`, `PENNY.pdf`, `Netto_Marken_Discount.pdf`, `REWE.pdf`).
- Phase 2 erfolgreich abgeschlossen: Skript `scripts/extract_deals.py` zur Validierung von 31 Angeboten und mathematischer Grundpreisprüfung in `angebote.json`.
- Phase 3 erfolgreich abgeschlossen: Skript `scripts/extract_images.py` zum hochauflösenden Zuschneiden von 15 Produktbildern und `scripts/generate_report.py` zur Erstellung des visuellen Wochenberichts als `wochenbericht.html` und `wochenbericht.pdf`.
- Phase 4 abgeschlossen: Einrichtung der wöchentlichen Antigravity-Automatisierung für Sonntags um 08:00 Uhr (`sidecar.json`).
- Phase 5 abgeschlossen: Mobile Web-App (PWA) in `web/` mit interaktiver Einkaufsliste, 195 gerenderten Blätterseiten für alle 4 Märkte, Essensplan-Übernahme, Vercel-Konfiguration und eleganter Einbindung als Hero-Banner in der bestehenden `FamilienZentrale` (`src/app/prospekte/page.tsx`).
- Live-Deployment & Integration: Bereitstellung der modernen Angebots-Radar-App unter `public/angebots-radar/` in der Next.js-FamilienZentrale, Vercel-Team-Autorisierung eingerichtet und Routing direkt auf `/angebots-radar/` umgestellt.
- Eigenständiges GitHub-Repository angelegt: `https://github.com/gembasede/einkaufsassistent-langelsheim` mit vollständiger Konfiguration für 100% autonomes, unabhängiges Hosting auf Vercel.
