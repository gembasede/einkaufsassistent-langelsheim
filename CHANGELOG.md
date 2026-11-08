# Changelog

Alle relevanten Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

## [Unreleased]
### Added
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
