#!/usr/bin/env python3

from pathlib import Path
from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
import re
import shutil

templates = read_templates("./templates")
source = Path("./input")
target = Path("./output")
target.mkdir(parents=True, exist_ok=True)

def safe_filename(value):
    return re.sub(r'[<>:"/\\|?*]', "_", str(value)).strip()

for pdf in source.glob("*.pdf"):
    data = extract_data(str(pdf), templates=templates)

    if not data:
        print(f"Kein passendes Template: {pdf.name}")
        continue

    template = data.get("template_name", "")
    date = data.get("date", "").strftime('%Y%m%d')
    customer_number = data.get("customer_number", "") 
    invoice_number = data.get("invoice_number", "")
    issuer = data.get("issuer", "Unbekannt")
    item = data.get("item", "Unbekannt")

    # Je nach erkanntem Template unterschiedlich benennen
    if template == "de.telekom.festnetz.yml":
        filename = f"{date}-rechnung-telekom-{customer_number}-{invoice_number}-monatsrechnung_{item}.pdf"

    elif template == "lieferant_b.yml":
        filename = f"{issuer}_{number}.pdf"

    else:
        filename = f"{date}_{number}.pdf"

    destination = target / safe_filename(filename)

    # Vorhandene Dateien nicht versehentlich überschreiben
    if destination.exists():
        print(f"Datei existiert bereits: {destination}")
        continue

    shutil.copy2(pdf, destination)
    print(f"{pdf.name} -> {destination.name}")
    
#FILENAME_FORMATS = {
#    "lieferant_a.yml": "{date}_{invoice_number}.pdf",
#    "lieferant_b.yml": "{issuer}_{invoice_number}_{amount}.pdf",
#    "lieferant_c.yml": "{date}_{issuer}_{desc}.pdf",
#}

#template = data.get("template_name", "")
#filename_format = FILENAME_FORMATS.get(
#    template,
#    "{date}_{invoice_number}.pdf"
#)

#filename = filename_format.format_map(
#    {key: str(value) for key, value in data.items()}
#)

