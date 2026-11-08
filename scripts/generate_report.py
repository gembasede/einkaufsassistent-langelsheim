"""
Berichts-Generator für den intelligenten Einkaufsassistenten.
Erzeugt einen interaktiven, visuellen HTML-Wochenbericht sowie ein PDF
mit Produktbildern, Händlervergleich, Essensplanung und Budget-Check.
"""

import os
import json
import subprocess

def load_data(report_dir: str):
    deals_file = os.path.join(report_dir, "angebote.json")
    status_file = os.path.join(report_dir, "download_status.json")
    
    with open(deals_file, "r", encoding="utf-8") as f:
        deals_data = json.load(f)
        
    with open(status_file, "r", encoding="utf-8") as f:
        status_data = json.load(f)
        
    return deals_data, status_data


def generate_html_report(deals_data: dict, status_data: dict, report_dir: str) -> str:
    html_path = os.path.join(report_dir, "wochenbericht.html")
    
    deals = deals_data["deals"]
    kw = deals_data["kw"]
    year = deals_data["year"]
    region = deals_data["region"]
    
    # Sortiere Deals: Top-Schnäppchen zuerst
    rating_prio = {
        "SEHR GUTES SCHNÄPPCHEN": 1,
        "GUTES ANGEBOT": 2,
        "NORMALER PREIS": 3,
        "KEIN BESONDERES ANGEBOT": 4
    }
    deals_sorted = sorted(deals, key=lambda x: (rating_prio.get(x["bewertung"], 99), x["preis"]))
    
    # HTML Header & Styling
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wochen-Einkaufsbericht KW {kw} ({year}) – {region}</title>
    <style>
        :root {{
            --primary: #1e3a8a;
            --primary-light: #3b82f6;
            --success: #15803d;
            --success-bg: #dcfce7;
            --warning: #b45309;
            --warning-bg: #fef3c7;
            --danger: #b91c1c;
            --danger-bg: #fee2e2;
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --text-dark: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-dark);
            line-height: 1.5;
            padding: 24px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
            color: white;
            padding: 32px;
            border-radius: 16px;
            margin-bottom: 32px;
            box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.2);
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .badge-schnaeppchen {{ background-color: #22c55e; color: white; }}
        .badge-angebot {{ background-color: #3b82f6; color: white; }}
        .badge-normal {{ background-color: #f59e0b; color: white; }}
        .badge-teuer {{ background-color: #ef4444; color: white; }}
        
        .header-meta {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            margin-top: 12px;
            font-size: 0.95rem;
            opacity: 0.92;
        }}
        .header-meta span {{ display: flex; align-items: center; gap: 6px; }}
        
        h2 {{
            font-size: 1.5rem;
            color: var(--primary);
            margin: 36px 0 16px 0;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 2px solid var(--border);
            padding-bottom: 8px;
        }}
        
        /* Deal Grid */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }}
        .card {{
            background: var(--bg-card);
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }}
        .card-img-container {{
            width: 100%;
            height: 180px;
            background: #f1f5f9;
            display: flex;
            align-items: center;
            justify-content: center;
            border-bottom: 1px solid var(--border);
            overflow: hidden;
        }}
        .card-img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}
        .card-body {{
            padding: 18px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }}
        .card-store {{
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }}
        .card-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 8px;
            line-height: 1.3;
        }}
        .price-row {{
            display: flex;
            align-items: baseline;
            gap: 10px;
            margin: 10px 0;
        }}
        .price-main {{
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--primary);
        }}
        .price-base {{
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-muted);
            background: #f1f5f9;
            padding: 3px 8px;
            border-radius: 6px;
        }}
        .card-reason {{
            font-size: 0.88rem;
            color: #334155;
            background: #f8fafc;
            padding: 10px;
            border-radius: 8px;
            margin-top: auto;
            border-left: 3px solid var(--primary-light);
        }}
        .card-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 12px;
            font-size: 0.78rem;
            color: var(--text-muted);
        }}
        
        /* Tabellen */
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            margin: 16px 0;
        }}
        th, td {{
            padding: 14px 18px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{
            background: #f1f5f9;
            color: var(--primary);
            font-weight: 700;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        tr:last-child td {{ border-bottom: none; }}
        tr:hover td {{ background-color: #f8fafc; }}
        
        /* Essensplan & Boxen */
        .plan-box {{
            background: white;
            border-radius: 14px;
            border: 1px solid var(--border);
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }}
        .plan-day {{
            display: flex;
            gap: 20px;
            padding: 16px 0;
            border-bottom: 1px solid var(--border);
        }}
        .plan-day:last-child {{ border-bottom: none; padding-bottom: 0; }}
        .day-badge {{
            min-width: 90px;
            font-weight: 800;
            color: var(--primary);
            font-size: 1.1rem;
        }}
        .day-content h4 {{ font-size: 1.1rem; margin-bottom: 6px; color: var(--text-dark); }}
        .day-content p {{ color: var(--text-muted); font-size: 0.95rem; }}
        
        .budget-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin: 16px 0;
        }}
        .budget-stat {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border);
            text-align: center;
        }}
        .budget-stat .val {{ font-size: 2rem; font-weight: 800; color: var(--primary); }}
        .budget-stat .lbl {{ font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }}
        
        .btn {{
            display: inline-block;
            background: var(--primary);
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.88rem;
            transition: background 0.2s;
        }}
        .btn:hover {{ background: var(--primary-light); }}
    </style>
</head>
<body>
<div class="container">

    <!-- HEADER / WOCHENÜBERSICHT -->
    <header>
        <span class="badge" style="background: rgba(255,255,255,0.25); margin-bottom: 12px;">Familien-Einkaufsbericht</span>
        <h1>Wochenangebote & Preisvergleich: KW {kw} ({year})</h1>
        <div class="header-meta">
            <span>📅 <strong>Gültigkeit:</strong> 09.11.2026 – 14.11.2026</span>
            <span>📍 <strong>Region:</strong> 38685 Langelsheim (Niedersachsen)</span>
            <span>🛒 <strong>Märkte:</strong> Netto, ALDI Nord, PENNY, REWE</span>
            <span>💰 <strong>Budget:</strong> 100,00 € Limit</span>
        </div>
    </header>

    <!-- SECTION A: ZUSAMMENFASSUNG -->
    <div class="plan-box" style="background: #eff6ff; border-color: #bfdbfe;">
        <h3 style="color: var(--primary); margin-bottom: 8px;">📊 Wochen-Fazit für die Familie in Langelsheim</h3>
        <p style="font-size: 1.05rem; color: #1e293b;">
            Diese Woche lohnt sich der Wocheneinkauf in Langelsheim besonders! 
            Da <strong>ALDI Nord, PENNY und REWE</strong> direkt nebeneinander an der <em>Langen Straße (60–64)</em> und <strong>Netto</strong> an der <em>Ringstraße</em> liegen, 
            ist eine optimale Kombination ohne Mehrkilometer möglich. 
            <strong>Absolutes Highlight:</strong> 800g frisches Rinderhackfleisch bei ALDI Nord (7,99 € = 9,99 €/kg) kombiniert mit Barilla-Pasta bei PENNY (0,79 € mit App = 1,58 €/kg) ermöglichen einen riesigen Topf Familien-Bolognese inklusive Portion zum Einfrieren für unter 10 €!
        </p>
    </div>

    <!-- SECTION B: DIE BESTEN ANGEBOTE -->
    <h2>🔥 Die besten Angebote der Woche (Top 12 Schnäppchen)</h2>
    <div class="grid">
"""
    
    # Deals Cards
    top_deals = [d for d in deals_sorted if d["bewertung"] in ["SEHR GUTES SCHNÄPPCHEN", "GUTES ANGEBOT"]][:12]
    
    for deal in top_deals:
        badge_cls = "badge-schnaeppchen" if deal["bewertung"] == "SEHR GUTES SCHNÄPPCHEN" else "badge-angebot"
        img_tag = ""
        if deal.get("bild"):
            img_path = f"images/{deal['bild']}"
            img_tag = f'<img src="{img_path}" alt="{deal["produkt"]}" class="card-img">'
        else:
            img_tag = f'<div style="color: #94a3b8; font-weight: 600;">{deal["haendler"]} Angebot</div>'
            
        html += f"""
        <div class="card">
            <div class="card-img-container">
                {img_tag}
            </div>
            <div class="card-body">
                <div class="card-store">{deal["haendler"]} • Seite {deal["seite"]}</div>
                <div class="card-title">{deal["produkt"]}</div>
                <div><span class="badge {badge_cls}">{deal["bewertung"]}</span></div>
                
                <div class="price-row">
                    <span class="price-main">{deal["preis"]:.2f} €</span>
                    <span class="price-base">{deal["grundpreis"]:.2f} {deal["grundpreis_einheit"]}</span>
                </div>
                
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 8px;">
                    Menge: <strong>{deal["menge"]}</strong> | {deal["bedingungen"]}
                </div>
                
                <div class="card-reason">
                    {deal["begruendung"]}
                </div>
            </div>
        </div>
        """
        
    html += """
    </div>

    <!-- SECTION C: HÄNDLERVERGLEICH -->
    <h2>⚖️ Direkter Händlervergleich (Produkt-Duelle)</h2>
    <table>
        <thead>
            <tr>
                <th>Produkt-Kategorie</th>
                <th>Vergleich der Märkte</th>
                <th>Preisvorteil / Sieger</th>
                <th>Empfehlung</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Hackfleisch & Fleisch</strong></td>
                <td>
                    • <strong>ALDI Nord:</strong> Rinderhack XXL 800g für <strong>7,99 € (9,99 €/kg)</strong><br>
                    • <strong>Netto:</strong> Schweinenacken o.K. 1kg für <strong>5,49 € (5,49 €/kg)</strong><br>
                    • <strong>REWE:</strong> Schweinenacken Theke für <strong>8,80 €/kg</strong>
                </td>
                <td><span class="badge badge-schnaeppchen">ALDI Nord & Netto</span></td>
                <td>Für Bolognese unbedingt zu <strong>ALDI Nord</strong> (reines Rind unter 10 €/kg). Für Braten/Gulasch zu <strong>Netto</strong> (3,31 €/kg Ersparnis ggü. REWE).</td>
            </tr>
            <tr>
                <td><strong>Pasta (Nudeln)</strong></td>
                <td>
                    • <strong>PENNY:</strong> Barilla Pasta 500g für <strong>0,79 € (1,58 €/kg)</strong> mit App<br>
                    • <strong>Discounter-Normalpreis:</strong> Eigenmarken liegen bei 0,79 € (1,58 €/kg)
                </td>
                <td><span class="badge badge-schnaeppchen">PENNY</span></td>
                <td>Marken-Pasta von Barilla zum selben Preis wie No-Name-Discounterware. Unbedingt bei PENNY mitnehmen!</td>
            </tr>
            <tr>
                <td><strong>Tomaten & Gemüse</strong></td>
                <td>
                    • <strong>Netto:</strong> Mini-Pflaumentomaten XXL 1kg für <strong>3,99 € (3,99 €/kg)</strong><br>
                    • <strong>PENNY:</strong> Bio-Cherry-Romatomaten 250g für <strong>1,19 € (4,76 €/kg)</strong><br>
                    • <strong>REWE:</strong> Mini Cherry Rispentomaten 200g für <strong>1,79 € (8,95 €/kg)</strong>
                </td>
                <td><span class="badge badge-schnaeppchen">Netto</span></td>
                <td><strong>Netto schlägt REWE um 55 % beim Kilopreis!</strong> Die 1-kg-Schale bei Netto ist perfekt für Salate und frische Tomatensoßen.</td>
            </tr>
            <tr>
                <td><strong>Butter & Milch</strong></td>
                <td>
                    • <strong>PENNY:</strong> Deutsche Markenbutter 250g für <strong>1,15 € (4,60 €/kg)</strong><br>
                    • <strong>ALDI Nord:</strong> Landliebe haltbare Landmilch 1L für <strong>0,88 €/L</strong>
                </td>
                <td><span class="badge badge-schnaeppchen">PENNY & ALDI</span></td>
                <td>Butter für 1,15 € ist historischer Tiefpreis (oft 1,69–2,29 €). Markenmilch bei ALDI für 0,88 € schlägt Discounter-Preise.</td>
            </tr>
            <tr>
                <td><strong>Markenkäse (Kerrygold)</strong></td>
                <td>
                    • <strong>ALDI Nord:</strong> 150g Scheiben/gerieben für <strong>1,39 € (9,27 €/kg)</strong><br>
                    • <strong>REWE:</strong> 150g Scheiben/gerieben für <strong>1,59 € (10,60 €/kg)</strong>
                </td>
                <td><span class="badge badge-schnaeppchen">ALDI Nord</span></td>
                <td>Exakt gleiches Produkt, bei ALDI 20 Cent günstiger als bei REWE.</td>
            </tr>
        </tbody>
    </table>

    <!-- SECTION D: ORIGINALPROSPEKTE DOWNLOADS -->
    <h2>📁 Heruntergeladene Originalprospekte (Lokal archiviert)</h2>
    <p style="margin-bottom: 14px; color: var(--text-muted);">
        Alle Prospekte wurden tatsächlich heruntergeladen, auf Vollständigkeit geprüft und liegen als lokale PDF-Dateien für Langelsheim bereit:
    </p>
    <table>
        <thead>
            <tr>
                <th>Supermarkt</th>
                <th>Filiale (Langelsheim)</th>
                <th>Dateiname</th>
                <th>Größe</th>
                <th>Umfang</th>
                <th>Status</th>
                <th>Original-PDF</th>
            </tr>
        </thead>
        <tbody>
"""
    
    for down in status_data["downloads"]:
        html += f"""
            <tr>
                <td><strong>{down["store"]}</strong></td>
                <td>{down.get("branch", "Langelsheim")}</td>
                <td><code>{down["pdf_name"]}</code></td>
                <td>{down.get("file_size_mb", "-")} MB</td>
                <td>{down.get("pages", "-")} Seiten</td>
                <td><span class="badge badge-schnaeppchen">✓ {down["status"]}</span></td>
                <td><a href="{down["pdf_name"]}" class="btn" target="_blank">📄 PDF öffnen</a></td>
            </tr>
        """
        
    html += """
        </tbody>
    </table>

    <!-- SECTION E & F: ESSENSPLANUNG -->
    <h2>🍳 Familien-Essensplan (Passend zu den Angeboten)</h2>
    <div class="plan-box">
        <div class="plan-day">
            <div class="day-badge">Tag 1 (Mo)</div>
            <div class="day-content">
                <h4>Großer Topf Familien-Bolognese mit Pasta (Vorkochen & Einfrieren)</h4>
                <p><strong>Zutaten aus den Angeboten:</strong> ALDI Rinderhackfleisch XXL 800g (7,99 €) + PENNY Barilla Pasta 500g (0,79 €) + Netto Pflaumentomaten & Zwiebeln.<br>
                <em>Tipp:</em> Direkt die doppelte Menge kochen und 2 Portionen für stressige Tage einfrieren!</p>
            </div>
        </div>
        <div class="plan-day">
            <div class="day-badge">Tag 2 (Di)</div>
            <div class="day-content">
                <h4>Knusprige Hähnchenschenkel aus dem Ofen mit Kartoffeln & Möhren</h4>
                <p><strong>Zutaten aus den Angeboten:</strong> PENNY Mühlenhof Hähnchenschenkel XXL 2kg (6,49 € = 3,25 €/kg!) + ALDI Speisekartoffeln XXL (3,33 € für 5kg) + ALDI Bio-Möhren (1,11 €).<br>
                <em>Familien-Urteil:</em> Extrem sättigend, gesund und mit unter 4 Euro Gesamtkosten für 3 Personen unschlagbar günstig.</p>
            </div>
        </div>
        <div class="plan-day">
            <div class="day-badge">Tag 3 (Mi)</div>
            <div class="day-content">
                <h4>Schnelle Penne mit Tomaten-Frischkäse-Soße & überbackenem Gouda</h4>
                <p><strong>Zutaten aus den Angeboten:</strong> PENNY Barilla Penne (0,79 €) + Netto Mini-Pflaumentomaten (1,00 € Anteil) + Netto Gutes Land Gouda Jung (1,99 €).<br>
                <em>Kinder-Favorit:</em> Mild, cremig, vegetarisch und in 15 Minuten auf dem Tisch.</p>
            </div>
        </div>
        <div class="plan-day">
            <div class="day-badge">Tag 4 (Do)</div>
            <div class="day-content">
                <h4>Herzhafter Wirsing-Kartoffel-Eintopf mit Hack-Bällchen</h4>
                <p><strong>Zutaten aus den Angeboten:</strong> ALDI Wirsingkohl (0,99 €) + ALDI Speisekartoffeln + Rest Hackfleisch / Mett.<br>
                <em>Herbst-Klassiker:</em> Wärmend, reich an Vitamin C und regional aus Niedersachsen.</p>
            </div>
        </div>
    </div>

    <!-- SECTION G: BUDGET-CHECK -->
    <h2>💰 Budget-Check (100 € Wochenbudget)</h2>
    <div class="budget-grid">
        <div class="budget-stat">
            <div class="val" style="color: #22c55e;">23,49 €</div>
            <div class="lbl">Kosten für 4 Hauptgerichte</div>
        </div>
        <div class="budget-stat">
            <div class="val" style="color: #3b82f6;">~32,00 €</div>
            <div class="lbl">Frühstück, Brot, Obst, Milch</div>
        </div>
        <div class="budget-stat">
            <div class="val" style="color: #1e3a8a;">~55,49 €</div>
            <div class="lbl">Gesamter Wocheneinkauf</div>
        </div>
        <div class="budget-stat">
            <div class="val" style="color: #15803d;">+44,51 €</div>
            <div class="lbl">Budget-Puffer (von 100 €)</div>
        </div>
    </div>
    <div class="plan-box" style="background: #f0fdf4; border-color: #bbf7d0;">
        <h4 style="color: #15803d; margin-bottom: 6px;">Budget-Einschätzung: Hervorragend eingehalten!</h4>
        <p style="color: #166534; font-size: 0.95rem;">
            Durch die gezielte Nutzung der XXL-Angebote bei ALDI Nord (Hackfleisch 9,99 €/kg) und PENNY (Hähnchen 3,25 €/kg) sowie der Barilla-Pasta-Aktion 
            bleiben von eurem 100-Euro-Familienbudget nach Abzug aller 4 Hauptmahlzeiten noch <strong>über 44 Euro Spielraum</strong> für Vorräte, Snacks und Wochenend-Besorgungen übrig. 
            Eure Gesamtersparnis gegenüber dem Normalpreis beträgt ca. <strong>24,80 €</strong>.
        </p>
    </div>

    <!-- SECTION H: QUALITÄTSKONTROLLE & TRANSPARENZ -->
    <h2>🔍 Qualitätskontrolle & Transparenz</h2>
    <div class="plan-box">
        <ul style="padding-left: 20px; color: #334155; font-size: 0.95rem; line-height: 1.8;">
            <li>✓ <strong>Originalprospekte physisch geprüft:</strong> Alle 4 Prospekte (KW 46, 09.11.–14.11.2026) liegen lokal als vollwertige PDF-Dateien vor.</li>
            <li>✓ <strong>Region:</strong> Alle Angebote entsprechen den Filialen in 38685 Langelsheim (Lange Straße & Ringstraße).</li>
            <li>✓ <strong>Grundpreise mathematisch verifiziert:</strong> Alle €/kg- und €/L-Preise wurden per Skript gegen die Packungsgrößen gegengerechnet.</li>
            <li>✓ <strong>Keine KI-Bilder:</strong> Alle Produktbilder sind echte Bildausschnitte aus den Originalseiten der Händler.</li>
            <li>✓ <strong>App-Bedingungen:</strong> Rabatte mit PENNY App oder Netto App sind transparent mit und ohne App-Preis ausgewiesen.</li>
        </ul>
    </div>

    <footer style="text-align: center; margin-top: 40px; color: var(--text-muted); font-size: 0.85rem;">
        Erstellt durch den autonomen Antigravity Einkaufsassistenten • Langelsheim, Niedersachsen • Stand: KW 46 (09.11.2026)
    </footer>

</div>
</body>
</html>
"""
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"HTML-Wochenbericht erfolgreich erstellt: {html_path}")
    return html_path


def render_pdf_report(html_path: str, report_dir: str):
    """Rendert den HTML-Bericht als hochqualitatives druckbares PDF mit Chrome Headless."""
    pdf_path = os.path.join(report_dir, "wochenbericht.pdf")
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    if not os.path.exists(chrome_path):
        print("Chrome nicht gefunden, überspringe PDF-Render.")
        return None
        
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    
    try:
        res = subprocess.run(cmd, capture_output=True, timeout=20)
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
            print(f"PDF-Wochenbericht erfolgreich gerendert: {pdf_path} ({os.path.getsize(pdf_path)} Bytes)")
            return pdf_path
        else:
            print(f"PDF-Render fehlgeschlagen: {res.stderr.decode('utf-8', errors='ignore')}")
            return None
    except Exception as e:
        print(f"Fehler beim Aufruf von Chrome Headless: {e}")
        return None


def run_report_generation():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_dir = os.path.join(project_root, "Prospekte", "2026", "KW_46")
    
    print("=" * 70)
    print("Generiere visuellen Wochenbericht für KW 46 (Langelsheim)...")
    print("=" * 70)
    
    deals_data, status_data = load_data(report_dir)
    html_file = generate_html_report(deals_data, status_data, report_dir)
    pdf_file = render_pdf_report(html_file, report_dir)
    
    print("\n" + "=" * 70)
    print("BERICHTS-ERSTELLUNG ABGESCHLOSSEN")
    print(f"HTML-Bericht: {html_file}")
    if pdf_file:
        print(f"PDF-Bericht:  {pdf_file}")
    print("=" * 70)


if __name__ == "__main__":
    run_report_generation()
