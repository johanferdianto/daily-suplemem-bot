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

# Mapping hari Inggris ke Indonesia
english_to_indo = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu",
    "Sunday": "Minggu"
}

hari_eng = datetime.now().strftime('%A')
hari_ini = english_to_indo.get(hari_eng, hari_eng)

data = sheet.get_all_records()
row = next((row for row in data if row['Hari'].strip().lower() == hari_ini.lower()), None)

if not row:
    print("❌ Hari tidak ditemukan dalam Sheet.")
    exit(1)

print("📦 TOKEN:", repr(BOT_TOKEN))
print("📦 CHAT_ID:", repr(CHAT_ID))
print("📨 PESAN:", pesan)

# Format pesan
pesan = f"🧠 Suplemen Hari {hari_ini}:\n\n"
for key, val in row.items():
    if key.lower() != 'hari' and val:
        pesan += f"• {key}: {val}\n"

# Kirim ke Telegram
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
res = requests.post(url, data={"chat_id": CHAT_ID, "text": pesan})
print("✅ Reminder dikirim:", res.status_code)

response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": pesan}
)

print("🧾 RESPONSE:", response.status_code, response.text)

