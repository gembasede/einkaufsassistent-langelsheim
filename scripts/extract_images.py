import pymupdf
import os
from PIL import Image

pdf_dir = r"C:\Users\gorni\.gemini\antigravity\scratch\einkaufsassistent\Prospekte\2026\KW_46"
img_out_dir = os.path.join(pdf_dir, "images")
os.makedirs(img_out_dir, exist_ok=True)

crops = [
    {
        "id": "aldi_hackfleisch",
        "pdf": "ALDI_Nord.pdf",
        "page": 5,
        # Normalized bbox [x0, y0, x1, y1] (0.0 to 1.0)
        "bbox": [0.08, 0.06, 0.62, 0.31],
        "name": "Rinderhackfleisch XXL 800g (ALDI)"
    },
    {
        "id": "aldi_milch",
        "pdf": "ALDI_Nord.pdf",
        "page": 1,
        "bbox": [0.36, 0.40, 0.54, 0.56],
        "name": "Landliebe Landmilch 1L (ALDI)"
    },
    {
        "id": "aldi_bananen",
        "pdf": "ALDI_Nord.pdf",
        "page": 1,
        "bbox": [0.06, 0.27, 0.33, 0.42],
        "name": "Bio Bananen Fairtrade (ALDI)"
    },
    {
        "id": "penny_barilla",
        "pdf": "PENNY.pdf",
        "page": 1,
        "bbox": [0.04, 0.66, 0.33, 0.94],
        "name": "Barilla Pasta 500g (PENNY)"
    },
    {
        "id": "penny_haehnchen",
        "pdf": "PENNY.pdf",
        "page": 1,
        "bbox": [0.35, 0.38, 0.94, 0.60],
        "name": "Mühlenhof Frische Hähnchenschenkel XXL (PENNY)"
    },
    {
        "id": "penny_butter",
        "pdf": "PENNY.pdf",
        "page": 2,
        "bbox": [0.06, 0.50, 0.45, 0.67],
        "name": "Milprima Deutsche Markenbutter (PENNY)"
    },
    {
        "id": "netto_almighurt",
        "pdf": "Netto_Marken_Discount.pdf",
        "page": 1,
        "bbox": [0.36, 0.10, 0.62, 0.48],
        "name": "Ehrmann Almighurt (Netto)"
    },
    {
        "id": "netto_schweinenacken",
        "pdf": "Netto_Marken_Discount.pdf",
        "page": 1,
        "bbox": [0.02, 0.18, 0.32, 0.33],
        "name": "Schweinenacken (Netto)"
    },
    {
        "id": "netto_tomaten",
        "pdf": "Netto_Marken_Discount.pdf",
        "page": 4,
        "bbox": [0.08, 0.28, 0.64, 0.48],
        "name": "Mini-Pflaumentomaten XXL 1kg (Netto)"
    },
    {
        "id": "rewe_toffifee",
        "pdf": "REWE.pdf",
        "page": 1,
        "bbox": [0.35, 0.75, 0.64, 0.96],
        "name": "Storck Toffifee (REWE)"
    },
    {
        "id": "rewe_bonduelle",
        "pdf": "REWE.pdf",
        "page": 1,
        "bbox": [0.66, 0.75, 0.96, 0.96],
        "name": "Bonduelle Goldmais (REWE)"
    },
    {
        "id": "aldi_kartoffeln",
        "pdf": "ALDI_Nord.pdf",
        "page": 2,
        "bbox": [0.60, 0.70, 0.98, 0.94],
        "name": "Speisekartoffeln XXL 5kg (ALDI)"
    },
    {
        "id": "aldi_wirsingkohl",
        "pdf": "ALDI_Nord.pdf",
        "page": 2,
        "bbox": [0.03, 0.36, 0.33, 0.64],
        "name": "Wirsingkohl unverpackt (ALDI)"
    },
    {
        "id": "netto_haribo",
        "pdf": "Netto_Marken_Discount.pdf",
        "page": 1,
        "bbox": [0.36, 0.78, 0.64, 0.96],
        "name": "Haribo Fruchtgummi (Netto)"
    },
    {
        "id": "rewe_spitzkohl",
        "pdf": "REWE.pdf",
        "page": 5,
        "bbox": [0.68, 0.54, 0.96, 0.74],
        "name": "REWE Regional Spitzkohl (REWE)"
    }
]

for c in crops:
    pdf_path = os.path.join(pdf_dir, c["pdf"])
    doc = pymupdf.open(pdf_path)
    page = doc[c["page"] - 1]
    
    # Get page width & height in points
    rect = page.rect
    w, h = rect.width, rect.height
    
    # Calculate crop rect in points
    x0, y0, x1, y1 = c["bbox"]
    crop_rect = pymupdf.Rect(x0 * w, y0 * h, x1 * w, y1 * h)
    
    # Render with high DPI (200 dpi for sharp product view)
    pix = page.get_pixmap(clip=crop_rect, dpi=200)
    out_file = os.path.join(img_out_dir, f"{c['id']}.jpg")
    pix.save(out_file)
    doc.close()
    print(f"Cropped {c['name']} -> {out_file} ({pix.width}x{pix.height})")
