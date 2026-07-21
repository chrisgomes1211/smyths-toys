#!/usr/bin/env python3
"""
Google Sheet Setup for Smyths Toys Chatbot

This script uploads the three CSV data files as separate tabs in a
Google Sheet. The chatbot then fetches live data from this sheet.

REQUIREMENTS:
  pip install gspread oauth2client

USAGE:
  1. Go to https://console.cloud.google.com/apis/credentials
  2. Create a service account and download the JSON key file
  3. Share your Google Sheet with the service account email
  4. Run: python setup-sheet.py --key service_account.json --sheet-id YOUR_SHEET_ID
"""

import csv
import json
import argparse
import os

def load_csv(filename):
    rows = []
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def main():
    parser = argparse.ArgumentParser(description='Upload CSVs to Google Sheet')
    parser.add_argument('--key', required=True, help='Path to service account JSON key')
    parser.add_argument('--sheet-id', required=True, help='Google Sheet ID')
    parser.add_argument('--data-dir', default='data', help='Path to data directory')
    args = parser.parse_args()

    try:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
    except ImportError:
        print("ERROR: Install gspread and oauth2client:")
        print("  pip install gspread oauth2client")
        return

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(args.key, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(args.sheet_id)

    # Tab 1: Products
    products = load_csv(os.path.join(args.data_dir, 'products.csv'))
    ws_prod = sheet.worksheet('Products') if 'Products' in [w.title for w in sheet.worksheets()] else sheet.add_worksheet('Products', len(products)+1, 20)
    ws_prod.clear()
    ws_prod.update([list(products[0].keys())] + [list(p.values()) for p in products])
    print(f"✅ Uploaded {len(products)} products to 'Products' tab")

    # Tab 2: Orders
    orders = load_csv(os.path.join(args.data_dir, 'orders.csv'))
    ws_ord = sheet.worksheet('Orders') if 'Orders' in [w.title for w in sheet.worksheets()] else sheet.add_worksheet('Orders', len(orders)+1, 20)
    ws_ord.clear()
    ws_ord.update([list(orders[0].keys())] + [list(o.values()) for o in orders])
    print(f"✅ Uploaded {len(orders)} orders to 'Orders' tab")

    # Tab 3: Training
    training = load_csv(os.path.join(args.data_dir, 'training.csv'))
    ws_trn = sheet.worksheet('Training') if 'Training' in [w.title for w in sheet.worksheets()] else sheet.add_worksheet('Training', len(training)+1, 20)
    ws_trn.clear()
    ws_trn.update([list(training[0].keys())] + [list(t.values()) for t in training])
    print(f"✅ Uploaded {len(training)} training examples to 'Training' tab")

    print(f"\n✅ Done! Sheet ID: {args.sheet_id}")
    print(f"   Paste this ID into the chatbot's SHEET_ID constant.")

if __name__ == '__main__':
    main()
