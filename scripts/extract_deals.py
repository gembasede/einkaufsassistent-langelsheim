"""
Modul zur Erfassung, mathematischen Grundpreisberechnung und
Schnäppchen-Klassifizierung der Lebensmittelangebote für Langelsheim (KW 48, 23.11.2026 – 28.11.2026).
"""

import os
import json
import datetime

DEALS_DATA_KW_48 = [
    # ================= ALDI NORD (Lange Straße 62, 38685 Langelsheim) =================
    {
        "id": "aldi_minutensteaks",
        "produkt": "Frische Minutensteaks aus dem Schweinerücken",
        "marke": "ALDI Frische / Deutsches Qualitätsfleisch",
        "haendler": "ALDI Nord",
        "preis": 2.29,
        "menge": "400 g",
        "menge_wert": 0.4,
        "menge_einheit": "kg",
        "grundpreis": 5.73,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-23% UVP 2.99 €, Haltungsform 2 (aus deutschem Schweinerücken)",
        "seite": 1,
        "kategorie": "Fleisch & Geflügel",
        "bewertung": "SEHR GUTES SCHNÄPPCHEN",
        "begruendung": "Mageres Schweinefleisch für 5,73 €/kg ist der absolute Fleisch-Preishit der Woche für die Familienküche.",
        "bild": "aldi_minutensteaks.jpg"
    },
    {
        "id": "aldi_baerenmarke_milch",
        "produkt": "Bärenmarke Haltbare Milch (1,5% oder 3,5% Fett)",
        "marke": "Bärenmarke",
        "haendler": "ALDI Nord",
        "preis": 0.88,
        "menge": "1 Liter",
        "menge_wert": 1.0,
        "menge_einheit": "l",
        "grundpreis": 0.88,
        "grundpreis_einheit": "€/L",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-40% UVP 1.49 €",
        "seite": 1,
        "kategorie": "Milch & Molkerei",
        "bewertung": "SEHR GUTES SCHNÄPPCHEN",
        "begruendung": "Premium-Markenmilch für 0,88 € ist günstiger als die billigsten Discounter-Eigenmarken (normal 0,99 €).",
        "bild": "aldi_baerenmarke_milch.jpg"
    },
    {
        "id": "aldi_clementinen",
        "produkt": "Süße Clementinen (Klasse 1)",
        "marke": "Spanische Ernte",
        "haendler": "ALDI Nord",
        "preis": 1.29,
        "menge": "1 kg",
        "menge_wert": 1.0,
        "menge_einheit": "kg",
        "grundpreis": 1.29,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-13% UVP 1.49 €, 1-kg-Netz",
        "seite": 1,
        "kategorie": "Obst & Gemüse",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "Wichtige Vitamine für den Winter: Frische kernarme Clementinen für 1,29 €/kg.",
        "bild": "aldi_clementinen.jpg"
    },
    {
        "id": "aldi_prinzenrolle",
        "produkt": "De Beukelaer Prinzenrolle (Schoko oder Vanille)",
        "marke": "De Beukelaer",
        "haendler": "ALDI Nord",
        "preis": 1.39,
        "menge": "400 g",
        "menge_wert": 0.4,
        "menge_einheit": "kg",
        "grundpreis": 3.48,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-46% UVP 2.59 €, 400-g-Rolle",
        "seite": 1,
        "kategorie": "Süßes & Snacks",
        "bewertung": "SEHR GUTES SCHNÄPPCHEN",
        "begruendung": "Fast 50% Rabatt auf den beliebten Doppelkeks-Klassiker fürs Kind.",
        "bild": "aldi_prinzenrolle.jpg"
    },
    {
        "id": "aldi_rougette_ofenkaese",
        "produkt": "Rougette Ofenkäse (versch. Sorten)",
        "marke": "Rougette",
        "haendler": "ALDI Nord",
        "preis": 3.79,
        "menge": "320 g",
        "menge_wert": 0.32,
        "menge_einheit": "kg",
        "grundpreis": 11.84,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-36% UVP 5.99 €",
        "seite": 1,
        "kategorie": "Milch & Molkerei",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "UVP knapp 6 Euro – bei ALDI für 3,79 € ideal für ein schnelles warmes Abendessen mit Baguette.",
        "bild": "aldi_rougette.jpg"
    },
    {
        "id": "aldi_mars_eisriegel",
        "produkt": "Mars / Snickers Ice Cream Riegel",
        "marke": "Mars Ice Cream",
        "haendler": "ALDI Nord",
        "preis": 1.99,
        "menge": "252 ml (6er Pack)",
        "menge_wert": 0.252,
        "menge_einheit": "l",
        "grundpreis": 7.9,
        "grundpreis_einheit": "€/L",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-46% UVP 3.69 €",
        "seite": 1,
        "kategorie": "Süßes & Snacks",
        "bewertung": "SEHR GUTES SCHNÄPPCHEN",
        "begruendung": "Original Markeneisriegel zum Discounterpreis.",
        "bild": None
    },
    {
        "id": "aldi_ueltje_erdnuesse",
        "produkt": "ültje Erdnüsse XXL geröstet & gesalzen",
        "marke": "ültje",
        "haendler": "ALDI Nord",
        "preis": 2.79,
        "menge": "450 g",
        "menge_wert": 0.45,
        "menge_einheit": "kg",
        "grundpreis": 6.2,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-40% UVP 4.69 €, XXL 450-g-Beutel",
        "seite": 1,
        "kategorie": "Vorrat & Teigwaren",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "Günstiger Knabberspaß für die Eltern auf der Couch.",
        "bild": None
    },
    {
        "id": "aldi_finish_caps",
        "produkt": "Finish Spülmaschinen-Caps Ultimate Plus XXL",
        "marke": "Finish",
        "haendler": "ALDI Nord",
        "preis": 9.99,
        "menge": "82 Stück",
        "menge_wert": 82.0,
        "menge_einheit": "Stück",
        "grundpreis": 0.12,
        "grundpreis_einheit": "€/Stk.",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-33% UVP 14.99 €, Sparpackung 82 Anwendungen",
        "seite": 1,
        "kategorie": "Haushalt",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "Günstiger Spültab-Vorrat für fast 3 Monate (12 Cent pro Spülgang).",
        "bild": None
    },

    # ================= PENNY (Lange Straße 64, 38685 Langelsheim) =================
    {
        "id": "penny_bauer_joghurt",
        "produkt": "Der Große Bauer Fruchtjoghurt (versch. Sorten)",
        "marke": "Bauer",
        "haendler": "PENNY",
        "preis": 0.39,
        "menge": "250 g",
        "menge_wert": 0.25,
        "menge_einheit": "kg",
        "grundpreis": 1.56,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-60% UVP 0.99 € mit PENNY App (ohne App 0.49 € = 1.96 €/kg)",
        "seite": 1,
        "kategorie": "Milch & Molkerei",
        "bewertung": "SEHR GUTES SCHNÄPPCHEN",
        "begruendung": "Großer 250g Markenbecher für 39 Cent – der billigste Fruchtjoghurt der Woche!",
        "bild": "penny_bauer_joghurt.jpg"
    },
    {
        "id": "penny_haribo",
        "produkt": "HARIBO Fruchtgummi (Pico-Balla, Phantasia etc.)",
        "marke": "HARIBO",
        "haendler": "PENNY",
        "preis": 0.69,
        "menge": "205 g",
        "menge_wert": 0.205,
        "menge_einheit": "kg",
        "grundpreis": 3.37,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-42% UVP 1.19 € mit App (ohne App 0.79 € = 3.85 €/kg)",
        "seite": 1,
        "kategorie": "Süßes & Snacks",
        "bewertung": "SEHR GUTES SCHNÄPPCHEN",
        "begruendung": "Haribo unter 0,70 € pro Packung mit App.",
        "bild": "penny_haribo.jpg"
    },
    {
        "id": "penny_avocado",
        "produkt": "Avocado Hass vorgereift (Klasse 1)",
        "marke": "PENNY Frische",
        "haendler": "PENNY",
        "preis": 0.69,
        "menge": "1 Stück",
        "menge_wert": 1.0,
        "menge_einheit": "Stück",
        "grundpreis": 0.69,
        "grundpreis_einheit": "€/Stk.",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "Aktion, verzehrreif",
        "seite": 1,
        "kategorie": "Obst & Gemüse",
        "bewertung": "SEHR GUTES SCHNÄPPCHEN",
        "begruendung": "Vorgereifte Hass-Avocado für 69 Cent ist Spitzenklasse (normal 1,29–1,49 €).",
        "bild": "penny_avocado.jpg"
    },
    {
        "id": "penny_gruenlaender",
        "produkt": "Grünländer Käsescheiben (mild & nussig / würzig)",
        "marke": "Grünländer",
        "haendler": "PENNY",
        "preis": 1.69,
        "menge": "156 g",
        "menge_wert": 0.156,
        "menge_einheit": "kg",
        "grundpreis": 10.83,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-43% UVP 2.99 € mit App (ohne App 1.79 €)",
        "seite": 1,
        "kategorie": "Milch & Molkerei",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "Ohne Gentechnik, beliebter Familien-Schnittkäse fürs Abendbrot.",
        "bild": None
    },
    {
        "id": "penny_milka_weihnachtsmann",
        "produkt": "Milka Alpenmilch Weihnachtsmann",
        "marke": "Milka",
        "haendler": "PENNY",
        "preis": 0.99,
        "menge": "45 g",
        "menge_wert": 0.045,
        "menge_einheit": "kg",
        "grundpreis": 22.0,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-47% UVP 1.89 €",
        "seite": 1,
        "kategorie": "Süßes & Snacks",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "Pünktlich zum Start der Adventszeit unter 1 Euro.",
        "bild": None
    },
    {
        "id": "penny_lavazza_kaffee",
        "produkt": "Lavazza Espresso Crema e Aroma Ganze Bohnen",
        "marke": "Lavazza",
        "haendler": "PENNY",
        "preis": 12.99,
        "menge": "1000 g (1 kg)",
        "menge_wert": 1.0,
        "menge_einheit": "kg",
        "grundpreis": 12.99,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-40% UVP 21.99 € mit App (ohne App 13.99 €)",
        "seite": 1,
        "kategorie": "Vorrat & Teigwaren",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "Günstiger Kilopreis für Marken-Kaffeebohnen.",
        "bild": None
    },

    # ================= NETTO MARKEN-DISCOUNT (Ringstraße 34a, 38685 Langelsheim) =================
    {
        "id": "netto_hackfleisch",
        "produkt": "Frisches Hackfleisch gemischt (50% Rind, 50% Schwein)",
        "marke": "Gut Ponholz",
        "haendler": "Netto Marken-Discount",
        "preis": 3.49,
        "menge": "500 g",
        "menge_wert": 0.5,
        "menge_einheit": "kg",
        "grundpreis": 6.98,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-22% UVP 4.49 €, aus Selbstbedienung",
        "seite": 1,
        "kategorie": "Fleisch & Geflügel",
        "bewertung": "SEHR GUTES SCHNÄPPCHEN",
        "begruendung": "6,98 €/kg ist die günstigste Hackfleisch-Aktion der Region! Ideal für Bolognese und Frikadellen.",
        "bild": "netto_hackfleisch.jpg"
    },
    {
        "id": "netto_mueller_ecke",
        "produkt": "Müller Joghurt mit der Ecke (versch. Sorten)",
        "marke": "Müller",
        "haendler": "Netto Marken-Discount",
        "preis": 0.29,
        "menge": "150 g",
        "menge_wert": 0.15,
        "menge_einheit": "kg",
        "grundpreis": 1.93,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-67% UVP 0.89 € mit Netto App (ohne App 0.33 € = 2.20 €/kg)",
        "seite": 1,
        "kategorie": "Milch & Molkerei",
        "bewertung": "SEHR GUTES SCHNÄPPCHEN",
        "begruendung": "Mit 29 Cent Rekord-Tiefpreis für den Kultjoghurt.",
        "bild": "netto_mueller_ecke.jpg"
    },
    {
        "id": "netto_fol_epi",
        "produkt": "Fol Epi Käsescheiben (Classic / Caractère)",
        "marke": "Fol Epi",
        "haendler": "Netto Marken-Discount",
        "preis": 1.49,
        "menge": "150 g",
        "menge_wert": 0.15,
        "menge_einheit": "kg",
        "grundpreis": 9.93,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-44% UVP 2.69 €",
        "seite": 1,
        "kategorie": "Milch & Molkerei",
        "bewertung": "SEHR GUTES SCHNÄPPCHEN",
        "begruendung": "Französischer Markenkäse unter 1,50 € pro Packung.",
        "bild": "netto_fol_epi.jpg"
    },
    {
        "id": "netto_clementinen_xxl",
        "produkt": "Clementinen XXL Holzkiste",
        "marke": "Netto Frische",
        "haendler": "Netto Marken-Discount",
        "preis": 3.49,
        "menge": "2.3 kg",
        "menge_wert": 2.3,
        "menge_einheit": "kg",
        "grundpreis": 1.52,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-30% UVP 4.99 €, 2.3-kg-Kiste",
        "seite": 1,
        "kategorie": "Obst & Gemüse",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "Riesige 2,3-kg-Kiste für 3,49 € reicht locker die ganze Woche für die Familie.",
        "bild": None
    },
    {
        "id": "netto_kaefer_kaffee",
        "produkt": "Käfer Caffè Crema Lungo Ganze Bohnen",
        "marke": "Käfer",
        "haendler": "Netto Marken-Discount",
        "preis": 9.99,
        "menge": "1000 g (1 kg)",
        "menge_wert": 1.0,
        "menge_einheit": "kg",
        "grundpreis": 9.99,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-33% UVP 14.99 €, 5 € Sparen",
        "seite": 1,
        "kategorie": "Vorrat & Teigwaren",
        "bewertung": "SEHR GUTES SCHNÄPPCHEN",
        "begruendung": "1 kg Qualitätsbohnen unter 10 Euro ist selten zu finden.",
        "bild": None
    },
    {
        "id": "netto_booster_energy",
        "produkt": "Booster Energy Drink (6er Pack)",
        "marke": "Booster",
        "haendler": "Netto Marken-Discount",
        "preis": 2.99,
        "menge": "1.98 Liter (6x0.33L)",
        "menge_wert": 1.98,
        "menge_einheit": "l",
        "grundpreis": 1.51,
        "grundpreis_einheit": "€/L",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-44% UVP 5.34 €, 6 Dosen für 2.99 € zzgl. Pfand",
        "seite": 1,
        "kategorie": "Getränke",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "Knapp 50 Cent pro Dose im Vorratspack.",
        "bild": None
    },
    {
        "id": "netto_star_batterien",
        "produkt": "Star Super Energy Batterien 24er XXL (AA/AAA)",
        "marke": "Star",
        "haendler": "Netto Marken-Discount",
        "preis": 3.33,
        "menge": "24 Stück",
        "menge_wert": 24.0,
        "menge_einheit": "Stück",
        "grundpreis": 0.14,
        "grundpreis_einheit": "€/Stk.",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "Aktion XXL 24er Pack",
        "seite": 1,
        "kategorie": "Haushalt",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "Sehr nützlich vor Weihnachten für Spielzeug und Lichterketten (14 Cent/Batterie).",
        "bild": None
    },

    # ================= REWE (Lange Str. 60, 38685 Langelsheim) =================
    {
        "id": "rewe_grapefruit",
        "produkt": "Frische Grapefruit rot (Klasse 1)",
        "marke": "Spanische Ernte",
        "haendler": "REWE",
        "preis": 0.55,
        "menge": "1 Stück",
        "menge_wert": 1.0,
        "menge_einheit": "Stück",
        "grundpreis": 0.55,
        "grundpreis_einheit": "€/Stk.",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "Knaller-Aktion",
        "seite": 1,
        "kategorie": "Obst & Gemüse",
        "bewertung": "SEHR GUTES SCHNÄPPCHEN",
        "begruendung": "55 Cent für frische Grapefruit ist ein Top-Frischeangebot.",
        "bild": "rewe_grapefruit.jpg"
    },
    {
        "id": "rewe_milram_quark",
        "produkt": "Milram Frühlingsquark / Gewürzquark",
        "marke": "Milram",
        "haendler": "REWE",
        "preis": 0.99,
        "menge": "185 g",
        "menge_wert": 0.185,
        "menge_einheit": "kg",
        "grundpreis": 5.35,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "Statt 1.49 € (+0.10 € App-Bonus = effektiv 0.89 €)",
        "seite": 1,
        "kategorie": "Milch & Molkerei",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "Perfekt zu Kartoffeln für ein schnelles Familienessen unter 1 Euro.",
        "bild": "rewe_milram.jpg"
    },
    {
        "id": "rewe_kinder_bueno",
        "produkt": "Kinder Bueno (6er) oder Kinder Country (9er)",
        "marke": "Ferrero",
        "haendler": "REWE",
        "preis": 1.99,
        "menge": "211 g",
        "menge_wert": 0.211,
        "menge_einheit": "kg",
        "grundpreis": 9.43,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "-39% UVP 3.29 €",
        "seite": 1,
        "kategorie": "Süßes & Snacks",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "Sehr beliebter Familiensnack um fast 40% reduziert.",
        "bild": "rewe_kinder.jpg"
    },
    {
        "id": "rewe_ehrmann_protein",
        "produkt": "Ehrmann High Protein Pudding oder Drink",
        "marke": "Ehrmann",
        "haendler": "REWE",
        "preis": 0.99,
        "menge": "200 g",
        "menge_wert": 0.2,
        "menge_einheit": "kg",
        "grundpreis": 4.95,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "Statt 1.49 €",
        "seite": 1,
        "kategorie": "Milch & Molkerei",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "Beliebter Protein-Pudding unter 1 Euro.",
        "bild": None
    },
    {
        "id": "rewe_coca_cola",
        "produkt": "Coca-Cola / Fanta / Sprite (Kasten 12x1L)",
        "marke": "Coca-Cola",
        "haendler": "REWE",
        "preis": 11.99,
        "menge": "12 Liter (12x1L)",
        "menge_wert": 12.0,
        "menge_einheit": "l",
        "grundpreis": 1.0,
        "grundpreis_einheit": "€/L",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "Statt 16.99 € (+2.00 € App-Bonus = effektiv 9.99 € / 0.83 €/L)",
        "seite": 1,
        "kategorie": "Getränke",
        "bewertung": "GUTES ANGEBOT",
        "begruendung": "1 Euro pro Flasche (mit App sogar 0,83 €/L) für den Familienvorrat.",
        "bild": None
    },
    {
        "id": "rewe_rinder_rouladen",
        "produkt": "Rinder-Rouladen, -Braten oder -Gulasch (Bedientheke)",
        "marke": "REWE Qualitätsmetzgerei",
        "haendler": "REWE",
        "preis": 19.9,
        "menge": "1 kg (aus der Keule)",
        "menge_wert": 1.0,
        "menge_einheit": "kg",
        "grundpreis": 19.9,
        "grundpreis_einheit": "€/kg",
        "zeitraum": "23.11.2026 – 28.11.2026",
        "bedingungen": "Knaller-Aktion (1.99 € je 100g)",
        "seite": 1,
        "kategorie": "Fleisch & Geflügel",
        "bewertung": "NORMALER PREIS",
        "begruendung": "Feine Metzgerqualität von der Theke für Festtagsgerichte. Für die alltägliche Spar-Küche ist das Netto-Hackfleisch (6,98 €/kg) günstiger.",
        "bild": None
    }
]


def validate_and_save_deals():
    today = datetime.date.today()
    if today.weekday() >= 5:
        target_monday = today + datetime.timedelta(days=(7 - today.weekday()))
    else:
        target_monday = today - datetime.timedelta(days=today.weekday())
    kw = target_monday.isocalendar()[1]
    year = target_monday.year

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(project_root, "Prospekte", str(year), f"KW_{kw}")
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "angebote.json")
    
    print("=" * 70)
    print(f"Validiere {len(DEALS_DATA_KW_48)} Angebote für KW {kw} (Langelsheim)...")
    print("=" * 70)
    
    valid_deals = []
    errors = []
    
    for deal in DEALS_DATA_KW_48:
        calc_gp = round(deal["preis"] / deal["menge_wert"], 2)
        stated_gp = deal["grundpreis"]
        
        diff = abs(calc_gp - stated_gp)
        if diff > 0.08:
            errors.append(f"Grundpreis-Diskrepanz bei {deal['produkt']}: Berechnet {calc_gp}, angegeben {stated_gp}")
        else:
            valid_deals.append(deal)
    
    if errors:
        print("\nWARNUNGEN / DISKREPANZEN:")
        for err in errors:
            print(f"  [!] {err}")
    
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump({
            "kw": kw,
            "year": year,
            "validity": f"{target_monday.strftime('%d.%m.%Y')} – {(target_monday + datetime.timedelta(days=5)).strftime('%d.%m.%Y')}",
            "region": "38685 Langelsheim, Niedersachsen",
            "total_deals": len(valid_deals),
            "deals": valid_deals
        }, f, indent=2, ensure_ascii=False)
        
    print(f"\nErfolg: {len(valid_deals)} Angebote erfolgreich validiert und gespeichert in:\n{target_file}")
    
    # Statistik nach Bewertung
    stats = {}
    for d in valid_deals:
        stats[d["bewertung"]] = stats.get(d["bewertung"], 0) + 1
    print("\nVerteilung der Angebote:")
    for bewertung, count in stats.items():
        print(f"  - {bewertung}: {count}")


if __name__ == "__main__":
    validate_and_save_deals()
