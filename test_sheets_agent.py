# test_sheets.py
from dotenv import load_dotenv
load_dotenv()

from agents.google_sheets_agent import write_to_sheet
import os
from datetime import datetime

spreadsheet_id = os.getenv("SPREADSHEET_ID")  
if not spreadsheet_id:
    raise ValueError("SPREADSHEET_ID not defined in .env")

row = [
    datetime.utcnow().isoformat(),
    "C999",
    0.75,
    "test_sheet_write"
]

# write_to_sheet expects list of lists
values = [row]

result = write_to_sheet(
    range_name="Sheet1!A1",
    values=values
)

print("Result of writing in Sheets:", result)
