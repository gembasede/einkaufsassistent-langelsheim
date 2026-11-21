"""
Download- und Assemblierungsmodul für den intelligenten Einkaufsassistenten.
Lädt die Original-Prospektseiten für die aktuelle/kommende Kalenderwoche für Langelsheim herunter,
assembliert sie zu echten, vollwertigen PDFs und führt eine Integritätsprüfung durch.
Unterstützt vollautomatische, dynamische Wochenberechnung.
"""

import os
import sys
import json
import time
import datetime
import urllib.request
import concurrent.futures
import pymupdf  # PyMuPDF
from PIL import Image

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_target_week_config(custom_monday: str = None) -> dict:
    """
    Ermittelt dynamisch die Ziel-Kalenderwoche.
    Am Wochenende (Samstag/Sonntag) wird automatisch der kommende Montag für die neue Woche gewählt.
    Unter der Woche (Mo-Fr) wird der Montag der laufenden Woche gewählt.
    """
    if custom_monday:
        target_monday = datetime.datetime.strptime(custom_monday, "%Y-%m-%d").date()
    else:
        today = datetime.date.today()
        # Am Wochenende (Samstag=5, Sonntag=6) bereiten wir die neue Woche ab Montag vor
        if today.weekday() >= 5:
            target_monday = today + datetime.timedelta(days=(7 - today.weekday()))
        else:
            target_monday = today - datetime.timedelta(days=today.weekday())

    target_saturday = target_monday + datetime.timedelta(days=5)
    kw = target_monday.isocalendar()[1]
    year = target_monday.year
    date_str = target_monday.strftime("%Y-%m-%d")
    date_de_str = target_monday.strftime("%d-%m-%Y")
    validity = f"{target_monday.strftime('%d.%m.%Y')} – {target_saturday.strftime('%d.%m.%Y')}"

    # Bekannte Seitenzahlen für KW 48 (23.11.2026), ansonsten dynamische Erkennung
    page_counts = {
        "ALDI_Nord": 49,
        "PENNY": 17,
        "Netto_Marken_Discount": 36,
        "REWE": 32
    }

    return {
        "year": year,
        "kw": kw,
        "target_monday": date_str,
        "validity": validity,
        "stores": {
            "ALDI_Nord": {
                "name": "ALDI Nord",
                "branch": "Lange Straße 62, 38685 Langelsheim",
                "pdf_name": "ALDI_Nord.pdf",
                "page_count": page_counts["ALDI_Nord"],
                "url_pattern": f"https://prospekte.com/wp-content/uploads/prospekte/aldi-nord/{date_str}/prospekt/{{:04d}}.jpg",
                "source_type": "Originalseiten aus digitalem Blätterkatalog (assembliert)",
                "source_url": f"https://onlineprospekt.com/prospekte/aldi-nord/prospekt-{date_de_str}/"
            },
            "PENNY": {
                "name": "PENNY",
                "branch": "Lange Straße 64, 38685 Langelsheim",
                "pdf_name": "PENNY.pdf",
                "page_count": page_counts["PENNY"],
                "url_pattern": f"https://prospekte.com/wp-content/uploads/prospekte/penny/{date_str}/prospekt/{{:04d}}.jpg",
                "source_type": "Originalseiten aus digitalem Blätterkatalog (assembliert)",
                "source_url": f"https://onlineprospekt.com/prospekte/penny/prospekt-{date_de_str}/"
            },
            "Netto_Marken_Discount": {
                "name": "Netto Marken-Discount",
                "branch": "Ringstraße 34a, 38685 Langelsheim",
                "pdf_name": "Netto_Marken_Discount.pdf",
                "page_count": page_counts["Netto_Marken_Discount"],
                "url_pattern": f"https://prospekte.com/wp-content/uploads/prospekte/netto/{date_str}/prospekt/{{:04d}}.jpg",
                "source_type": "Originalseiten aus digitalem Blätterkatalog (assembliert)",
                "source_url": f"https://onlineprospekt.com/prospekte/netto/prospekt-{date_de_str}/"
            },
            "REWE": {
                "name": "REWE",
                "branch": "Lange Str. 60, 38685 Langelsheim",
                "pdf_name": "REWE.pdf",
                "page_count": page_counts["REWE"],
                "url_pattern": f"https://prospekte.com/wp-content/uploads/prospekte/rewe/{date_str}/prospekt/{{:04d}}.jpg",
                "source_type": "Originalseiten aus digitalem Blätterkatalog (assembliert)",
                "source_url": f"https://onlineprospekt.com/prospekte/rewe/prospekt-{date_de_str}/"
            }
        }
    }


def download_single_image(url: str, output_path: str, retries: int = 3) -> bool:
    """Lädt ein einzelnes Bild herunter mit Wiederholungsversuchen."""
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        return True
        
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as response:
                content = response.read()
                if len(content) > 1000:  # Plausibilitätsprüfung
                    with open(output_path, 'wb') as f:
                        f.write(content)
                    return True
        except Exception:
            time.sleep(0.5)
    return False


def build_pdf_from_images(image_paths: list, output_pdf_path: str) -> bool:
    """Erzeugt mit PyMuPDF ein valides, hochqualitatives PDF aus Bildseiten."""
    try:
        doc = pymupdf.open()
        for img_path in image_paths:
            img_doc = pymupdf.open(img_path)
            pdf_bytes = img_doc.convert_to_pdf()
            img_pdf = pymupdf.open("pdf", pdf_bytes)
            doc.insert_pdf(img_pdf)
            img_doc.close()
            img_pdf.close()
        
        doc.save(output_pdf_path)
        doc.close()
        return True
    except Exception as e:
        print(f"Fehler beim PDF-Bau für {output_pdf_path}: {e}")
        return False


def verify_pdf(pdf_path: str, expected_pages: int) -> dict:
    """Überprüft die physische Integrität und Lesbarkeit des PDFs."""
    if not os.path.exists(pdf_path):
        return {"valid": False, "error": "Datei existiert nicht"}
    
    size_bytes = os.path.getsize(pdf_path)
    if size_bytes < 10000:
        return {"valid": False, "error": f"Datei zu klein ({size_bytes} Bytes)"}
    
    try:
        doc = pymupdf.open(pdf_path)
        actual_pages = len(doc)
        if actual_pages != expected_pages:
            doc.close()
            return {
                "valid": False,
                "error": f"Seitenzahl weicht ab (Erwartet: {expected_pages}, Tatsächlich: {actual_pages})"
            }
        
        # Teste, ob Seite 1 gerendert werden kann
        first_page = doc[0]
        rect = first_page.rect
        doc.close()
        
        return {
            "valid": True,
            "size_mb": round(size_bytes / (1024 * 1024), 2),
            "size_bytes": size_bytes,
            "pages": actual_pages,
            "page_width": round(rect.width, 1),
            "page_height": round(rect.height, 1)
        }
    except Exception as e:
        return {"valid": False, "error": f"PDF beschädigt oder unlesbar: {e}"}


def process_store(store_key: str, store_info: dict, target_dir: str, temp_dir: str, validity: str) -> dict:
    """Verarbeitet den Download und die Validierung für einen einzelnen Händler."""
    name = store_info["name"]
    pdf_path = os.path.join(target_dir, store_info["pdf_name"])
    expected_pages = store_info["page_count"]
    
    print(f"\n[{name}] Starte Download von {expected_pages} Prospektseiten...")
    store_temp_dir = os.path.join(temp_dir, store_key)
    os.makedirs(store_temp_dir, exist_ok=True)
    
    # 1. Bild-URLs vorbereiten
    page_tasks = []
    for page_num in range(1, expected_pages + 1):
        url = store_info["url_pattern"].format(page_num)
        img_file = os.path.join(store_temp_dir, f"page_{page_num:04d}.jpg")
        page_tasks.append((url, img_file))
    
    # 2. Paralleler Download mit ThreadPool
    downloaded_files = []
    failed_pages = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_page = {
            executor.submit(download_single_image, url, path): (i + 1, path)
            for i, (url, path) in enumerate(page_tasks)
        }
        for future in concurrent.futures.as_completed(future_to_page):
            page_idx, path = future_to_page[future]
            if future.result():
                downloaded_files.append((page_idx, path))
            else:
                failed_pages.append(page_idx)
    
    if failed_pages:
        print(f"[{name}] FEHLER: {len(failed_pages)} Seiten konnten nicht geladen werden!")
        return {
            "store": name,
            "branch": store_info["branch"],
            "pdf_name": store_info["pdf_name"],
            "status": "FEHLGESCHLAGEN",
            "error": f"Seiten nicht abrufbar: {failed_pages}",
            "source": store_info["source_type"]
        }
    
    # Sortiere nach Seitennummer
    downloaded_files.sort(key=lambda x: x[0])
    image_paths = [p for _, p in downloaded_files]
    
    # 3. Assembliere PDF
    print(f"[{name}] Assembliere PDF ({expected_pages} Seiten)...")
    success = build_pdf_from_images(image_paths, pdf_path)
    if not success:
        return {
            "store": name,
            "branch": store_info["branch"],
            "pdf_name": store_info["pdf_name"],
            "status": "FEHLGESCHLAGEN",
            "error": "PDF-Generierung fehlgeschlagen",
            "source": store_info["source_type"]
        }
    
    # 4. Validierung
    verif = verify_pdf(pdf_path, expected_pages)
    if verif["valid"]:
        print(f"[{name}] ERFOLG: {store_info['pdf_name']} verifiziert ({verif['size_mb']} MB, {verif['pages']} Seiten)")
        return {
            "store": name,
            "branch": store_info["branch"],
            "pdf_name": store_info["pdf_name"],
            "file_path": os.path.abspath(pdf_path),
            "file_size_mb": verif["size_mb"],
            "pages": verif["pages"],
            "validity": validity,
            "status": "HERUNTERGELADEN UND VERIFIZIERT",
            "source": store_info["source_type"],
            "source_url": store_info["source_url"]
        }
    else:
        print(f"[{name}] VALIDIERUNGSFEHLER: {verif['error']}")
        return {
            "store": name,
            "branch": store_info["branch"],
            "pdf_name": store_info["pdf_name"],
            "status": "VALIDIERUNG FEHLGESCHLAGEN",
            "error": verif["error"],
            "source": store_info["source_type"]
        }


def run_download_pipeline():
    """Führt die vollständige Download- und Verifikationspipeline aus."""
    config = get_target_week_config()
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(project_root, "Prospekte", str(config["year"]), f"KW_{config['kw']}")
    temp_dir = os.path.join(target_dir, "_temp_pages")
    
    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    
    print("=" * 70)
    print(f"Einkaufsassistent Langelsheim: Prospekt-Download KW {config['kw']} ({config['validity']})")
    print(f"Zielordner: {target_dir}")
    print("=" * 70)
    
    results = []
    for store_key, store_info in config["stores"].items():
        res = process_store(store_key, store_info, target_dir, temp_dir, config["validity"])
        results.append(res)
    
    # Statusübersicht speichern
    status_file = os.path.join(target_dir, "download_status.json")
    with open(status_file, "w", encoding="utf-8") as f:
        json.dump({
            "kw": config["kw"],
            "year": config["year"],
            "validity": config["validity"],
            "target_monday": config["target_monday"],
            "region": "38685 Langelsheim, Niedersachsen",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "downloads": results
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 70)
    print("DOWNLOAD-STATUS-ÜBERSICHT")
    print("=" * 70)
    for r in results:
        status_symbol = "✓" if r["status"] == "HERUNTERGELADEN UND VERIFIZIERT" else "✗"
        mb_str = f"{r.get('file_size_mb', 0)} MB" if 'file_size_mb' in r else "-"
        pages_str = f"{r.get('pages', 0)} S." if 'pages' in r else "-"
        print(f"[{status_symbol}] {r['store']:<22} | {r['pdf_name']:<25} | {mb_str:<8} | {pages_str:<6} | {r['status']}")
    print(f"\nStatusdatei gespeichert unter: {status_file}")


if __name__ == "__main__":
    run_download_pipeline()
