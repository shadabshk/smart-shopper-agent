import json
import os
import gspread
from google.oauth2.service_account import Credentials

def get_sheet():
    # Load service account credentials from GitHub Secret
    creds_json = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(creds_json, scopes=scopes)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(os.environ["GSHEET_ID"]).sheet1
    return sheet

def read_new_orders():
    sheet = get_sheet()
    rows = sheet.get_all_records()

    new_orders = [r for r in rows if r["Status"] == "NEW"]

    print(f"🟢 Found {len(new_orders)} NEW orders")
    for order in new_orders:
        print(order)

if __name__ == "__main__":
    read_new_orders()

