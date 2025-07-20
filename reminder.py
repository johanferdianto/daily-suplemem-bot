import os
import gspread
import base64
import tempfile
from oauth2client.service_account import ServiceAccountCredentials
import requests
from datetime import datetime

# Decode base64 credentials
base64_creds = os.environ['GOOGLE_CREDENTIALS_B64']
json_data = base64.b64decode(base64_creds).decode('utf-8')

# Tulis sementara ke file
with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
    temp.write(json_data)
    temp_json_path = temp.name

# Setup Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(temp_json_path, scope)
client = gspread.authorize(creds)

spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qKWUIB9QcJ2Yh-B5ciTxiDRWdBcpKcEGO2cNFf2zsro")
sheet = spreadsheet.worksheet("Jadwal")

hari_ini = datetime.now().strftime('%A')
data = sheet.get_all_records()

row = next((row for row in data if row['Hari'].lower() == hari_ini.lower()), None)

if not row:
    print("❌ Hari tidak ditemukan dalam Sheet.")
    exit(1)

pesan = f"🧠 Suplemen Hari {hari_ini}:\n\n"
for key, val in row.items():
    if key != 'Hari' and val:
        pesan += f"• {key}: {val}\n"

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ_
