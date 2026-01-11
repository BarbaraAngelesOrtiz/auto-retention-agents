# test_sheets.py
from dotenv import load_dotenv
load_dotenv()

from agents.google_sheets_agent import write_to_sheet
import os
from datetime import datetime

# --- Datos de prueba ---
spreadsheet_id = os.getenv("SPREADSHEET_ID")  # debe estar en tu .env
if not spreadsheet_id:
    raise ValueError("SPREADSHEET_ID no definido en .env")

row = [
    datetime.utcnow().isoformat(),
    "C999",
    0.75,
    "test_sheet_write"
]

# write_to_sheet espera lista de listas
values = [row]

# --- Ejecutar ---
result = write_to_sheet(
    range_name="Sheet1!A1",
    values=values
)

print("Resultado de escritura en Sheets:", result)
