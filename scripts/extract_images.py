import pymupdf
import os
import datetime

today = datetime.date.today()
if today.weekday() >= 5:
    target_monday = today + datetime.timedelta(days=(7 - today.weekday()))
else:
    target_monday = today - datetime.timedelta(days=today.weekday())
kw = target_monday.isocalendar()[1]
year = target_monday.year

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf_dir = os.path.join(project_root, "Prospekte", str(year), f"KW_{kw}")
img_out_dir = os.path.join(pdf_dir, "images")
os.makedirs(img_out_dir, exist_ok=True)

crops = [
    # ALDI NORD (Page 1)
    {
        "id": "aldi_clementinen",
        "pdf": "ALDI_Nord.pdf",
        "page": 1,
        "bbox": [0.05, 0.25, 0.33, 0.42],
        "name": "Clementinen 1kg (ALDI)"
    },
    {
        "id": "aldi_minutensteaks",
        "pdf": "ALDI_Nord.pdf",
        "page": 1,
        "bbox": [0.05, 0.42, 0.33, 0.59],
        "name": "Minutensteaks 400g (ALDI)"
    },
    {
        "id": "aldi_baerenmarke_milch",
        "pdf": "ALDI_Nord.pdf",
        "page": 1,
        "bbox": [0.36, 0.22, 0.65, 0.39],
        "name": "Bärenmarke Milch 1L (ALDI)"
    },
    {
        "id": "aldi_rougette",
        "pdf": "ALDI_Nord.pdf",
        "page": 1,
        "bbox": [0.75, 0.22, 0.95, 0.39],
        "name": "Rougette Ofenkäse (ALDI)"
    },
    {
        "id": "aldi_prinzenrolle",
        "pdf": "ALDI_Nord.pdf",
        "page": 1,
        "bbox": [0.65, 0.40, 0.95, 0.58],
        "name": "Prinzenrolle 400g (ALDI)"
    },
    
    # PENNY (Page 1)
    {
        "id": "penny_avocado",
        "pdf": "PENNY.pdf",
        "page": 1,
        "bbox": [0.57, 0.45, 0.98, 0.63],
        "name": "Avocado Hass (PENNY)"
    },
    {
        "id": "penny_bauer_joghurt",
        "pdf": "PENNY.pdf",
        "page": 1,
        "bbox": [0.03, 0.64, 0.33, 0.95],
        "name": "Der Grosse Bauer Joghurt (PENNY)"
    },
    {
        "id": "penny_haribo",
        "pdf": "PENNY.pdf",
        "page": 1,
        "bbox": [0.35, 0.64, 0.64, 0.95],
        "name": "Haribo Fruchtgummi (PENNY)"
    },

    # NETTO (Page 1)
    {
        "id": "netto_hackfleisch",
        "pdf": "Netto_Marken_Discount.pdf",
        "page": 1,
        "bbox": [0.02, 0.16, 0.34, 0.36],
        "name": "Hackfleisch gemischt 500g (Netto)"
    },
    {
        "id": "netto_mueller_ecke",
        "pdf": "Netto_Marken_Discount.pdf",
        "page": 1,
        "bbox": [0.02, 0.36, 0.34, 0.55],
        "name": "Müller Joghurt mit der Ecke (Netto)"
    },
    {
        "id": "netto_fol_epi",
        "pdf": "Netto_Marken_Discount.pdf",
        "page": 1,
        "bbox": [0.02, 0.56, 0.34, 0.72],
        "name": "Fol Epi Käsescheiben (Netto)"
    },

    # REWE (Page 1)
    {
        "id": "rewe_grapefruit",
        "pdf": "REWE.pdf",
        "page": 1,
        "bbox": [0.34, 0.60, 0.65, 0.76],
        "name": "Grapefruit rot (REWE)"
    },
    {
        "id": "rewe_milram",
        "pdf": "REWE.pdf",
        "page": 1,
        "bbox": [0.01, 0.57, 0.33, 0.76],
        "name": "Milram Frühlingsquark (REWE)"
    },
    {
        "id": "rewe_kinder",
        "pdf": "REWE.pdf",
        "page": 1,
        "bbox": [0.67, 0.76, 0.98, 0.95],
        "name": "Kinder Bueno / Country (REWE)"
    }
]

print(f"Schneide {len(crops)} Produktbilder für KW {kw} ({year}) zu...")

for c in crops:
    pdf_path = os.path.join(pdf_dir, c["pdf"])
    if not os.path.exists(pdf_path):
        print(f"PDF nicht gefunden: {pdf_path}")
        continue
    doc = pymupdf.open(pdf_path)
    page = doc[c["page"] - 1]
    
    rect = page.rect
    w, h = rect.width, rect.height
    
    x0, y0, x1, y1 = c["bbox"]
    crop_rect = pymupdf.Rect(x0 * w, y0 * h, x1 * w, y1 * h)
    
    pix = page.get_pixmap(clip=crop_rect, dpi=200)
    out_file = os.path.join(img_out_dir, f"{c['id']}.jpg")
    pix.save(out_file)
    doc.close()
    print(f"Cropped {c['name']} -> {out_file} ({pix.width}x{pix.height})")

print(f"\nAlle Produktbilder erfolgreich zugeschnitten in:\n{img_out_dir}")
