"""
Web-App Generator für den Einkaufsassistenten Langelsheim.
Generiert eine vollständige mobile PWA (Single-Page-App) mit:
1. Angebote-Katalog mit Markt-Filtern & Suchleiste
2. Interaktiver Einkaufs-Checkliste mit Live-Summenrechner und localStorage-Speicherung
3. Mobilem Prospekt-Blätterkatalog für alle 4 Märkte
4. Familien-Essensplan mit 1-Klick-Übernahme in die Einkaufsliste
5. PWA-Manifest und Vercel-Konfiguration
"""

import os
import shutil
import json
import pymupdf


def setup_web_assets(project_root: str, report_dir: str, web_dir: str):
    """Kopiert Bilder und generiert Web-optimierte Prospektseiten für den Blätterkatalog."""
    print("1. Kopiere Produktbilder...")
    src_images = os.path.join(report_dir, "images")
    dst_images = os.path.join(web_dir, "images")
    os.makedirs(dst_images, exist_ok=True)
    
    if os.path.exists(src_images):
        for img in os.listdir(src_images):
            if img.lower().endswith(('.jpg', '.png', '.webp')):
                shutil.copy2(os.path.join(src_images, img), os.path.join(dst_images, img))
                
    print("2. Rendere Prospektseiten für den schnellen Blätterkatalog...")
    brochures_dir = os.path.join(web_dir, "brochures")
    os.makedirs(brochures_dir, exist_ok=True)
    
    stores_pdf = {
        "aldi": ("ALDI_Nord.pdf", "ALDI Nord"),
        "penny": ("PENNY.pdf", "PENNY"),
        "netto": ("Netto_Marken_Discount.pdf", "Netto Marken-Discount"),
        "rewe": ("REWE.pdf", "REWE")
    }
    
    brochures_manifest = {}
    
    for store_key, (pdf_name, store_title) in stores_pdf.items():
        pdf_path = os.path.join(report_dir, pdf_name)
        store_web_dir = os.path.join(brochures_dir, store_key)
        os.makedirs(store_web_dir, exist_ok=True)
        
        if os.path.exists(pdf_path):
            doc = pymupdf.open(pdf_path)
            total_pages = len(doc)
            # Kopiere auch das Original-PDF für direkten Download
            shutil.copy2(pdf_path, os.path.join(store_web_dir, pdf_name))
            
            # Rendere die Seiten als Web-JPEGs (90 DPI für schnelle mobile Ladezeiten)
            print(f"   [{store_title}] Rendere {total_pages} Seiten...")
            for page_num in range(total_pages):
                page = doc[page_num]
                pix = page.get_pixmap(dpi=90)
                page_img_name = f"p_{page_num + 1}.jpg"
                pix.save(os.path.join(store_web_dir, page_img_name))
            
            doc.close()
            brochures_manifest[store_key] = {
                "title": store_title,
                "pdf_url": f"brochures/{store_key}/{pdf_name}",
                "pages": total_pages,
                "page_pattern": f"brochures/{store_key}/p_{{}}.jpg"
            }
        else:
            print(f"   [!] Warnung: {pdf_name} nicht gefunden!")
            
    return brochures_manifest


def generate_manifest(web_dir: str):
    """Erzeugt das PWA-Manifest für die Installation auf dem Smartphone."""
    manifest = {
        "name": "Einkaufs-Assistent Langelsheim",
        "short_name": "Einkauf",
        "description": "Wöchentliche Prospekte, Angebote & Einkaufsliste für Langelsheim",
        "start_url": "./index.html",
        "display": "standalone",
        "background_color": "#f8fafc",
        "theme_color": "#1e3a8a",
        "icons": [
            {
                "src": "images/aldi_hackfleisch.jpg",
                "sizes": "192x192",
                "type": "image/jpeg"
            }
        ]
    }
    with open(os.path.join(web_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


def generate_vercel_config(web_dir: str):
    """Erzeugt die vercel.json Konfiguration."""
    config = {
        "version": 2,
        "name": "einkaufsassistent-langelsheim",
        "cleanUrls": True,
        "routes": [
            {
                "src": "/(.*)",
                "dest": "/index.html"
            }
        ]
    }
    with open(os.path.join(web_dir, "vercel.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def generate_spa_html(deals_data: dict, brochures_manifest: dict, web_dir: str):
    """Erzeugt die Single-Page-App HTML mit allen interaktiven Features."""
    html_path = os.path.join(web_dir, "index.html")
    
    deals_json = json.dumps(deals_data["deals"], ensure_ascii=False)
    brochures_json = json.dumps(brochures_manifest, ensure_ascii=False)
    
    # Pre-render initiale Deals-Karten (SSR-Style für sofortige Sichtbarkeit)
    pre_rendered_cards = ""
    for deal in deals_data["deals"]:
        badge_cls = "rating-schnaeppchen" if deal["bewertung"] == "SEHR GUTES SCHNÄPPCHEN" else ("rating-angebot" if deal["bewertung"] == "GUTES ANGEBOT" else "rating-normal")
        img_html = f'<img src="images/{deal["bild"]}" alt="{deal["produkt"]}" class="deal-img">' if deal.get("bild") else f'<div style="font-weight: bold; color: #94a3b8;">{deal["haendler"]}</div>'
        pre_rendered_cards += f"""
        <div class="deal-card" data-deal-id="{deal['id']}">
            <div class="deal-img-wrap">{img_html}</div>
            <div class="deal-content">
                <div class="deal-store">{deal["haendler"]} • S. {deal["seite"]}</div>
                <div class="deal-title">{deal["produkt"]}</div>
                <div><span class="rating-badge {badge_cls}">{deal["bewertung"]}</span></div>
                <div class="price-badge-row">
                    <span class="deal-price">{deal["preis"]:.2f} €</span>
                    <span class="deal-baseprice">{deal["grundpreis"]:.2f} {deal["grundpreis_einheit"]}</span>
                </div>
                <div style="font-size: 0.8rem; color: #64748b; margin-bottom: 10px;">
                    {deal["menge"]} | {deal["bedingungen"]}
                </div>
                <button class="btn-add-list" onclick="toggleAddToList('{deal['id']}', this)">
                    + Auf Einkaufsliste
                </button>
            </div>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#1e3a8a">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>Einkaufs-Assistent Langelsheim</title>
    <link rel="manifest" href="manifest.json">
    <style>
        :root {{
            --primary: #1e3a8a;
            --primary-light: #2563eb;
            --primary-bg: #eff6ff;
            --success: #16a34a;
            --success-bg: #dcfce7;
            --warning: #d97706;
            --warning-bg: #fef3c7;
            --bg-page: #f8fafc;
            --bg-card: #ffffff;
            --text-dark: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --radius: 12px;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-dark);
            padding-bottom: 74px; /* Platz für Bottom Navigation */
            font-size: 15px;
        }}
        
        /* Top App Bar */
        .app-bar {{
            position: sticky;
            top: 0;
            z-index: 50;
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            color: white;
            padding: 12px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }}
        .app-title {{
            font-size: 1.15rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .app-badge {{
            font-size: 0.72rem;
            background: rgba(255,255,255,0.22);
            padding: 2px 8px;
            border-radius: 99px;
            font-weight: 600;
        }}
        
        /* Bottom Tab Navigation */
        .bottom-nav {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: var(--bg-card);
            display: flex;
            border-top: 1px solid var(--border);
            z-index: 50;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        }}
        .nav-item {{
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 3px;
            color: var(--text-muted);
            font-size: 0.72rem;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            border: none;
            background: none;
            transition: color 0.15s;
        }}
        .nav-item.active {{
            color: var(--primary-light);
        }}
        .nav-icon {{
            font-size: 1.25rem;
        }}
        .nav-badge {{
            position: absolute;
            top: 6px;
            right: 28%;
            background: #ef4444;
            color: white;
            font-size: 0.65rem;
            padding: 1px 5px;
            border-radius: 99px;
            font-weight: bold;
        }}
        
        /* Container & Tabs */
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 14px;
        }}
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
        
        /* Search & Filter Bar */
        .search-box {{
            width: 100%;
            padding: 10px 14px;
            border-radius: 10px;
            border: 1px solid var(--border);
            background: white;
            font-size: 0.95rem;
            margin-bottom: 12px;
            outline: none;
        }}
        .search-box:focus {{
            border-color: var(--primary-light);
            box-shadow: 0 0 0 3px rgba(37,99,235,0.15);
        }}
        .filter-chips {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 8px;
            margin-bottom: 14px;
            scrollbar-width: none;
        }}
        .filter-chips::-webkit-scrollbar {{ display: none; }}
        .chip {{
            white-space: nowrap;
            padding: 6px 14px;
            border-radius: 99px;
            font-size: 0.85rem;
            font-weight: 600;
            background: white;
            border: 1px solid var(--border);
            color: var(--text-dark);
            cursor: pointer;
        }}
        .chip.active {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }}
        
        /* Deal Cards */
        .deals-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 14px;
        }}
        .deal-card {{
            background: white;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        }}
        .deal-img-wrap {{
            height: 150px;
            background: #f1f5f9;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            border-bottom: 1px solid var(--border);
        }}
        .deal-img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}
        .deal-content {{
            padding: 12px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }}
        .deal-store {{
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
        }}
        .deal-title {{
            font-size: 1rem;
            font-weight: 700;
            margin: 4px 0 8px 0;
            line-height: 1.25;
        }}
        .price-badge-row {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            margin-bottom: 8px;
        }}
        .deal-price {{
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--primary);
        }}
        .deal-baseprice {{
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-muted);
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
        }}
        .rating-badge {{
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 99px;
            margin-bottom: 8px;
        }}
        .rating-schnaeppchen {{ background: var(--success-bg); color: var(--success); }}
        .rating-angebot {{ background: var(--primary-bg); color: var(--primary-light); }}
        .rating-normal {{ background: var(--warning-bg); color: var(--warning); }}
        
        .btn-add-list {{
            width: 100%;
            padding: 9px;
            border-radius: 8px;
            border: none;
            background: var(--primary);
            color: white;
            font-weight: 700;
            font-size: 0.85rem;
            cursor: pointer;
            margin-top: auto;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            transition: background 0.15s;
        }}
        .btn-add-list.added {{
            background: var(--success);
        }}
        
        /* Shopping Checklist Tab */
        .list-header {{
            background: white;
            border-radius: var(--radius);
            padding: 14px;
            border: 1px solid var(--border);
            margin-bottom: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .list-store-group {{
            background: white;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            margin-bottom: 14px;
            overflow: hidden;
        }}
        .list-store-title {{
            background: #f1f5f9;
            padding: 10px 14px;
            font-size: 0.85rem;
            font-weight: 800;
            color: var(--primary);
            text-transform: uppercase;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
        }}
        .list-item {{
            padding: 12px 14px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            user-select: none;
        }}
        .list-item:last-child {{ border-bottom: none; }}
        .list-item.checked {{
            background: #f8fafc;
            opacity: 0.55;
        }}
        .list-item.checked .item-text {{
            text-decoration: line-through;
        }}
        .custom-checkbox {{
            width: 22px;
            height: 22px;
            border-radius: 6px;
            border: 2px solid #cbd5e1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: bold;
            color: white;
            flex-shrink: 0;
        }}
        .list-item.checked .custom-checkbox {{
            background: var(--success);
            border-color: var(--success);
        }}
        .item-text {{
            flex-grow: 1;
            font-size: 0.95rem;
            font-weight: 600;
        }}
        .item-price {{
            font-weight: 700;
            color: var(--primary);
            font-size: 0.95rem;
        }}
        .btn-delete-item {{
            color: #94a3b8;
            background: none;
            border: none;
            font-size: 1.1rem;
            padding: 4px;
            cursor: pointer;
        }}
        .add-custom-form {{
            display: flex;
            gap: 8px;
            margin-top: 14px;
        }}
        .add-custom-input {{
            flex-grow: 1;
            padding: 10px 12px;
            border-radius: 8px;
            border: 1px solid var(--border);
            font-size: 0.95rem;
        }}
        .btn-add-custom {{
            background: var(--primary);
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
        }}
        
        /* Brochure Viewer Tab */
        .viewer-controls {{
            background: white;
            padding: 12px;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            margin-bottom: 12px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .viewer-nav-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .viewer-select {{
            padding: 9px;
            border-radius: 8px;
            border: 1px solid var(--border);
            font-weight: 600;
            background: white;
            font-size: 0.92rem;
            width: 100%;
        }}
        .viewer-img-container {{
            background: #1e293b;
            border-radius: var(--radius);
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 480px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        .viewer-page-img {{
            max-width: 100%;
            height: auto;
            display: block;
        }}
        .btn-nav-page {{
            padding: 8px 16px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
        }}
        .btn-nav-page:disabled {{
            opacity: 0.35;
            cursor: not-allowed;
        }}
        
        /* Meal Plan Tab */
        .meal-card {{
            background: white;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            padding: 16px;
            margin-bottom: 14px;
        }}
        .meal-day {{
            font-size: 0.8rem;
            font-weight: 800;
            color: var(--primary-light);
            text-transform: uppercase;
        }}
        .meal-title {{
            font-size: 1.15rem;
            font-weight: 700;
            margin: 4px 0 8px 0;
        }}
        .meal-desc {{
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-bottom: 12px;
            line-height: 1.4;
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <div class="app-bar">
        <div class="app-title">
            🛒 Angebotsradar
            <span class="app-badge">Langelsheim • KW 46</span>
        </div>
        <div style="font-size: 0.8rem; opacity: 0.9;">09.11. – 14.11.</div>
    </div>

    <div class="container">

        <!-- TAB 1: ANGEBOTE -->
        <div id="tab-deals" class="tab-content active">
            <input type="text" id="dealSearch" class="search-box" placeholder="🔍 Angebote durchsuchen (z. B. Hackfleisch, Pasta, Bio)..." oninput="filterDeals()">
            
            <div class="filter-chips">
                <button class="chip active" onclick="setStoreFilter('all', this)">Alle Märkte</button>
                <button class="chip" onclick="setStoreFilter('ALDI Nord', this)">ALDI Nord</button>
                <button class="chip" onclick="setStoreFilter('PENNY', this)">PENNY</button>
                <button class="chip" onclick="setStoreFilter('Netto Marken-Discount', this)">Netto</button>
                <button class="chip" onclick="setStoreFilter('REWE', this)">REWE</button>
            </div>

            <div id="dealsGrid" class="deals-grid">
                {pre_rendered_cards}
            </div>
        </div>

        <!-- TAB 2: EINKAUFSLISTE -->
        <div id="tab-list" class="tab-content">
            <div class="list-header">
                <div>
                    <div style="font-size: 0.8rem; color: var(--text-muted); font-weight: 700;">GEMEINSAME EINKAUFSLISTE</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: var(--primary);" id="listTotal">0,00 €</div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button onclick="clearCheckedItems()" style="padding: 6px 12px; border-radius: 6px; border: 1px solid var(--border); background: white; font-size: 0.8rem; font-weight: 600; cursor: pointer;">Erledigte löschen</button>
                    <button onclick="clearAllList()" style="padding: 6px 12px; border-radius: 6px; border: 1px solid #fee2e2; background: #fef2f2; color: #dc2626; font-size: 0.8rem; font-weight: 600; cursor: pointer;">Leeren</button>
                </div>
            </div>

            <div id="listItemsContainer">
                <!-- Dynamisch generierte Einkaufsliste nach Supermarkt -->
            </div>

            <div class="add-custom-form">
                <input type="text" id="customItemInput" class="add-custom-input" placeholder="+ Eigenen Artikel notieren (z. B. Milch, Brot)...">
                <button onclick="addCustomItem()" class="btn-add-custom">Hinzufügen</button>
            </div>
        </div>

        <!-- TAB 3: PROSPEKTE BLÄTTERN -->
        <div id="tab-flyer" class="tab-content">
            <div class="viewer-controls">
                <select id="storeSelector" class="viewer-select" onchange="changeBrochureStore(this.value)">
                    <option value="aldi">ALDI Nord (44 Seiten)</option>
                    <option value="penny">PENNY (48 Seiten)</option>
                    <option value="netto">Netto Marken-Discount (75 Seiten)</option>
                    <option value="rewe">REWE (28 Seiten)</option>
                </select>
                
                <div class="viewer-nav-row">
                    <button id="btnPrevPage" class="btn-nav-page" onclick="prevPage()">‹ Zurück</button>
                    <span id="pageIndicator" style="font-weight: 700; font-size: 0.95rem;">Seite 1 / 44</span>
                    <button id="btnNextPage" class="btn-nav-page" onclick="nextPage()">Weiter ›</button>
                </div>
            </div>

            <div class="viewer-img-container">
                <img id="viewerImage" src="brochures/aldi/p_1.jpg" alt="Prospektseite" class="viewer-page-img">
            </div>
            
            <div style="text-align: center; margin-top: 12px;">
                <a id="originalPdfLink" href="brochures/aldi/ALDI_Nord.pdf" target="_blank" style="color: var(--primary-light); font-weight: 600; font-size: 0.85rem; text-decoration: none;">📄 Original-PDF herunterladen</a>
            </div>
        </div>

        <!-- TAB 4: ESSENSPLAN -->
        <div id="tab-meals" class="tab-content">
            <div class="meal-card">
                <div class="meal-day">Montag</div>
                <div class="meal-title">Großer Topf Familien-Bolognese mit Pasta</div>
                <div class="meal-desc">
                    <strong>Angebote:</strong> ALDI Rinderhackfleisch XXL 800g (7,99 €) + PENNY Barilla Pasta (0,79 €) + Netto Pflaumentomaten & Zwiebeln.<br>
                    <em>Tipp:</em> Eine Portion direkt für Donnerstag oder die Tiefkühltruhe einfrieren!
                </div>
                <button class="btn-add-list" onclick="addMealIngredients('bolognese')">+ Zutaten auf Einkaufsliste setzen</button>
            </div>

            <div class="meal-card">
                <div class="meal-day">Dienstag</div>
                <div class="meal-title">Knusprige Ofen-Hähnchenschenkel mit Kartoffeln</div>
                <div class="meal-desc">
                    <strong>Angebote:</strong> PENNY Mühlenhof Hähnchenschenkel XXL 2kg (6,49 € = 3,25 €/kg) + ALDI Speisekartoffeln XXL (3,33 € für 5kg) + ALDI Möhren (1,11 €).
                </div>
                <button class="btn-add-list" onclick="addMealIngredients('chicken')">+ Zutaten auf Einkaufsliste setzen</button>
            </div>

            <div class="meal-card">
                <div class="meal-day">Mittwoch</div>
                <div class="meal-title">Cremige Tomaten-Penne mit überbackenem Gouda</div>
                <div class="meal-desc">
                    <strong>Angebote:</strong> PENNY Barilla Penne (0,79 €) + Netto Pflaumentomaten (1,00 € Anteil) + Netto Gutes Land Gouda Jung (1,99 €).
                </div>
                <button class="btn-add-list" onclick="addMealIngredients('pasta')">+ Zutaten auf Einkaufsliste setzen</button>
            </div>

            <div class="meal-card">
                <div class="meal-day">Donnerstag</div>
                <div class="meal-title">Wirsing-Kartoffel-Eintopf mit Hackbällchen</div>
                <div class="meal-desc">
                    <strong>Angebote:</strong> ALDI Wirsingkohl (0,99 €) + ALDI Speisekartoffeln + Reste vom ALDI Hackfleisch.
                </div>
                <button class="btn-add-list" onclick="addMealIngredients('wirsing')">+ Zutaten auf Einkaufsliste setzen</button>
            </div>
        </div>

    </div>

    <!-- Bottom Tab Navigation -->
    <nav class="bottom-nav">
        <button class="nav-item active" onclick="switchTab('deals', this)">
            <span class="nav-icon">🔥</span>
            <span>Angebote</span>
        </button>
        <button class="nav-item" style="position: relative;" onclick="switchTab('list', this)">
            <span class="nav-icon">🛒</span>
            <span>Einkaufsliste</span>
            <span id="listBadge" class="nav-badge" style="display: none;">0</span>
        </button>
        <button class="nav-item" onclick="switchTab('flyer', this)">
            <span class="nav-icon">📖</span>
            <span>Prospekte</span>
        </button>
        <button class="nav-item" onclick="switchTab('meals', this)">
            <span class="nav-icon">🍳</span>
            <span>Essensplan</span>
        </button>
    </nav>

    <script>
        const DEALS = {deals_json};
        const BROCHURES = {brochures_json};

        let activeStoreFilter = 'all';
        let currentBrochureKey = 'aldi';
        let currentBrochurePage = 1;
        let shoppingList = JSON.parse(localStorage.getItem('familie_shopping_list') || '[]');

        // Tab Switching
        function switchTab(tabId, el) {{
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            el.classList.add('active');
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
            if (tabId === 'list') renderShoppingList();
        }}

        // Render Deals
        function renderDeals(filterDealsList) {{
            const container = document.getElementById('dealsGrid');
            container.innerHTML = '';
            
            filterDealsList.forEach(deal => {{
                const isAdded = shoppingList.some(item => item.id === deal.id);
                const badgeCls = deal.bewertung === 'SEHR GUTES SCHNÄPPCHEN' ? 'rating-schnaeppchen' : (deal.bewertung === 'GUTES ANGEBOT' ? 'rating-angebot' : 'rating-normal');
                const imgHtml = deal.bild ? `<img src="images/${{deal.bild}}" alt="${{deal.produkt}}" class="deal-img">` : `<div style="font-weight: bold; color: #94a3b8;">${{deal.haendler}}</div>`;
                
                const card = document.createElement('div');
                card.className = 'deal-card';
                card.innerHTML = `
                    <div class="deal-img-wrap">
                        ${{imgHtml}}
                    </div>
                    <div class="deal-content">
                        <div class="deal-store">${{deal.haendler}} • S. ${{deal.seite}}</div>
                        <div class="deal-title">${{deal.produkt}}</div>
                        <div><span class="rating-badge ${{badgeCls}}">${{deal.bewertung}}</span></div>
                        
                        <div class="price-badge-row">
                            <span class="deal-price">${{deal.preis.toFixed(2)}} €</span>
                            <span class="deal-baseprice">${{deal.grundpreis.toFixed(2)}} ${{deal.grundpreis_einheit}}</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #64748b; margin-bottom: 10px;">
                            ${{deal.menge}} | ${{deal.bedingungen}}
                        </div>
                        <button class="btn-add-list ${{isAdded ? 'added' : ''}}" onclick="toggleAddToList('${{deal.id}}', this)">
                            ${{isAdded ? '✓ Auf der Liste' : '+ Auf Einkaufsliste'}}
                        </button>
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function setStoreFilter(store, btn) {{
            activeStoreFilter = store;
            document.querySelectorAll('.filter-chips .chip').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            filterDeals();
        }}

        function filterDeals() {{
            const query = document.getElementById('dealSearch').value.toLowerCase();
            const filtered = DEALS.filter(d => {{
                const matchStore = activeStoreFilter === 'all' || d.haendler === activeStoreFilter;
                const matchQuery = d.produkt.toLowerCase().includes(query) || d.kategorie.toLowerCase().includes(query) || d.marke.toLowerCase().includes(query);
                return matchStore && matchQuery;
            }});
            renderDeals(filtered);
        }}

        // Shopping List Logic
        function saveShoppingList() {{
            localStorage.setItem('familie_shopping_list', JSON.stringify(shoppingList));
            updateListBadge();
        }}

        function updateListBadge() {{
            const badge = document.getElementById('listBadge');
            const count = shoppingList.filter(i => !i.checked).length;
            if (count > 0) {{
                badge.style.display = 'block';
                badge.innerText = count;
            }} else {{
                badge.style.display = 'none';
            }}
        }}

        function toggleAddToList(dealId, btn) {{
            const deal = DEALS.find(d => d.id === dealId);
            if (!deal) return;
            
            const existingIdx = shoppingList.findIndex(i => i.id === dealId);
            if (existingIdx >= 0) {{
                shoppingList.splice(existingIdx, 1);
                if (btn) {{
                    btn.classList.remove('added');
                    btn.innerText = '+ Auf Einkaufsliste';
                }}
            }} else {{
                shoppingList.push({{
                    id: deal.id,
                    title: deal.produkt,
                    store: deal.haendler,
                    price: deal.preis,
                    checked: false
                }});
                if (btn) {{
                    btn.classList.add('added');
                    btn.innerText = '✓ Auf der Liste';
                }}
            }}
            saveShoppingList();
        }}

        function renderShoppingList() {{
            const container = document.getElementById('listItemsContainer');
            container.innerHTML = '';
            
            if (shoppingList.length === 0) {{
                container.innerHTML = '<div style="text-align: center; padding: 40px; color: #94a3b8; font-weight: 600;">Eure Einkaufsliste ist noch leer.<br>Tippe bei den Angeboten auf „+ Auf Einkaufsliste“!</div>';
                document.getElementById('listTotal').innerText = '0,00 €';
                return;
            }}

            // Gruppiere nach Supermarkt
            const grouped = {{}};
            let total = 0;
            shoppingList.forEach((item, idx) => {{
                if (!grouped[item.store]) grouped[item.store] = [];
                grouped[item.store].push({{ ...item, originalIdx: idx }});
                if (!item.checked) total += item.price;
            }});

            document.getElementById('listTotal').innerText = total.toFixed(2) + ' €';

            for (const [store, items] of Object.entries(grouped)) {{
                const groupEl = document.createElement('div');
                groupEl.className = 'list-store-group';
                
                const storeTotal = items.filter(i => !i.checked).reduce((acc, i) => acc + i.price, 0);
                groupEl.innerHTML = `
                    <div class="list-store-title">
                        <span>${{store}}</span>
                        <span>${{storeTotal.toFixed(2)}} €</span>
                    </div>
                `;

                items.forEach(item => {{
                    const itemEl = document.createElement('div');
                    itemEl.className = 'list-item ' + (item.checked ? 'checked' : '');
                    itemEl.innerHTML = `
                        <div class="custom-checkbox" onclick="toggleCheckItem(${{item.originalIdx}})">
                            ${{item.checked ? '✓' : ''}}
                        </div>
                        <div class="item-text" onclick="toggleCheckItem(${{item.originalIdx}})">
                            ${{item.title}}
                        </div>
                        <div class="item-price">${{item.price > 0 ? item.price.toFixed(2) + ' €' : ''}}</div>
                        <button class="btn-delete-item" onclick="deleteItem(${{item.originalIdx}})">✕</button>
                    `;
                    groupEl.appendChild(itemEl);
                }});

                container.appendChild(groupEl);
            }}
        }}

        function toggleCheckItem(idx) {{
            shoppingList[idx].checked = !shoppingList[idx].checked;
            saveShoppingList();
            renderShoppingList();
        }}

        function deleteItem(idx) {{
            shoppingList.splice(idx, 1);
            saveShoppingList();
            renderShoppingList();
            filterDeals();
        }}

        function clearCheckedItems() {{
            shoppingList = shoppingList.filter(i => !i.checked);
            saveShoppingList();
            renderShoppingList();
            filterDeals();
        }}

        function clearAllList() {{
            if (confirm('Möchtest du die gesamte Einkaufsliste leeren?')) {{
                shoppingList = [];
                saveShoppingList();
                renderShoppingList();
                filterDeals();
            }}
        }}

        function addCustomItem() {{
            const input = document.getElementById('customItemInput');
            const val = input.value.trim();
            if (!val) return;
            shoppingList.push({{
                id: 'custom_' + Date.now(),
                title: val,
                store: 'Sonstiges / Notizen',
                price: 0.0,
                checked: false
            }});
            input.value = '';
            saveShoppingList();
            renderShoppingList();
        }}

        // Meal plan ingredient adder
        function addMealIngredients(mealKey) {{
            const mealMap = {{
                'bolognese': ['aldi_rinderhack', 'penny_barilla', 'netto_tomaten_xxl'],
                'chicken': ['penny_haehnchenschenkel', 'aldi_kartoffeln', 'aldi_bio_bananen'],
                'pasta': ['penny_barilla', 'netto_tomaten_xxl', 'netto_gouda'],
                'wirsing': ['aldi_wirsingkohl', 'aldi_kartoffeln']
            }};
            const ids = mealMap[mealKey] || [];
            ids.forEach(id => {{
                if (!shoppingList.some(item => item.id === id)) {{
                    toggleAddToList(id, null);
                }}
            }});
            alert('Die Zutaten für dieses Gericht wurden auf die Einkaufsliste gesetzt!');
            renderDeals(DEALS);
            updateListBadge();
        }}

        // Brochure Viewer Logic
        function changeBrochureStore(storeKey) {{
            currentBrochureKey = storeKey;
            currentBrochurePage = 1;
            updateViewer();
        }}

        function updateViewer() {{
            const b = BROCHURES[currentBrochureKey];
            if (!b) return;
            const imgEl = document.getElementById('viewerImage');
            const pageUrl = `brochures/${{currentBrochureKey}}/p_${{currentBrochurePage}}.jpg`;
            imgEl.src = pageUrl;
            
            document.getElementById('pageIndicator').innerText = `Seite ${{currentBrochurePage}} / ${{b.pages}}`;
            document.getElementById('btnPrevPage').disabled = (currentBrochurePage <= 1);
            document.getElementById('btnNextPage').disabled = (currentBrochurePage >= b.pages);
            
            const pdfLink = document.getElementById('originalPdfLink');
            pdfLink.href = b.pdf_url;
        }}

        function prevPage() {{
            if (currentBrochurePage > 1) {{
                currentBrochurePage--;
                updateViewer();
            }}
        }}

        function nextPage() {{
            const b = BROCHURES[currentBrochureKey];
            if (currentBrochurePage < b.pages) {{
                currentBrochurePage++;
                updateViewer();
            }}
        }}

        // Init
        window.addEventListener('DOMContentLoaded', () => {{
            renderDeals(DEALS);
            updateListBadge();
            updateViewer();
        }});
    </script>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Single-Page-App erfolgreich erstellt: {html_path}")


def run_generate_web():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_dir = os.path.join(project_root, "Prospekte", "2026", "KW_46")
    web_dir = os.path.join(project_root, "web")
    
    print("=" * 70)
    print("Erstelle mobile PWA Web-App für den Einkaufsassistenten...")
    print(f"Zielverzeichnis: {web_dir}")
    print("=" * 70)
    
    # Lade Deals
    with open(os.path.join(report_dir, "angebote.json"), "r", encoding="utf-8") as f:
        deals_data = json.load(f)
        
    brochures_manifest = setup_web_assets(project_root, report_dir, web_dir)
    generate_manifest(web_dir)
    generate_vercel_config(web_dir)
    generate_spa_html(deals_data, brochures_manifest, web_dir)
    
    print("\n" + "=" * 70)
    print("WEB-APP ERFOLGREICH GENERIERT!")
    print(f"Lokale Datei zum Testen: file:///{web_dir.replace(chr(92), '/')}/index.html")
    print("=" * 70)


if __name__ == "__main__":
    run_generate_web()
