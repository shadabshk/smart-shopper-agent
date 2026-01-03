import json
import os
import gspread
from google.oauth2.service_account import Credentials
from decision.select_cheapest import select_cheapest

def get_sheet():
    creds_json = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(creds_json, scopes=scopes)
    client = gspread.authorize(creds)

    return client.open_by_key(os.environ["GSHEET_ID"]).sheet1


def process_orders():
    sheet = get_sheet()
    rows = sheet.get_all_records()
    headers = sheet.row_values(1)

    print(f"📄 Total rows found: {len(rows)}")

    for index, row in enumerate(rows, start=2):  # start=2 → skip header
        if row["Status"] != "NEW":
            continue

        order_id = row["Order_ID"]
        item = row["Item_Intent"]
        max_price = row["Max_Price"]

        print(f"\n🛒 Processing Order_ID {order_id} → {item}")

        platform, price = select_cheapest(item, max_price)

        if not platform or not price:
            print(f"⚠️ No valid price found for Order_ID {order_id}")
            continue

        # Column positions (1-based)
        platform_col = headers.index("Selected_Platform") + 1
        price_col = headers.index("Final_Price") + 1
        status_col = headers.index("Status") + 1

        sheet.update_cell(index, platform_col, platform)
        sheet.update_cell(index, price_col, price)
        sheet.update_cell(index, status_col, "CART_READY")

        print(f"✅ Updated Order_ID {order_id}: {platform} @ ₹{price}")


if __name__ == "__main__":
    process_orders()
