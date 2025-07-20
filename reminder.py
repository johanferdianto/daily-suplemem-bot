import os
import gspread
import base64
import tempfile
from oauth2client.service_account import ServiceAccountCredentials
import requests
from datetime import datetime

# --- Load Google Credentials dari ENV ---
base64_creds = os.environ['GOOGLE_CREDENTIALS_B64']
json_data = base64.b64decode(base64_creds).decode('utf-8')

with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
    temp.write(json_data)
    temp_json_path = temp.name

# --- Setup koneksi Google Sheets ---
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(temp_json_path, scope)
client = gspread.authorize(creds)

spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qKWUIB9QcJ2Yh-B5ciTxiDRWdBcpKcEGO2cNFf2zsro")
sheet = spreadsheet.worksheet("Jadwal-Autophagy")

# Mapping hari Inggris ke Indonesia
map_hari = {
    "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
    "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
}

hari_eng = datetime.now().strftime('%A')
hari_ini = map_hari.get(hari_eng, hari_eng)

# 🔍 Ambil konten berdasarkan hari
data = sheet.get_all_records()
row = next((r for r in data if r.get('Hari', '').strip().lower() == hari_ini.lower()), None)

if not row or 'Konten' not in row or not row['Konten']:
    print(f"❌ Tidak ditemukan konten untuk hari: {hari_ini}")
    exit(1)

pesan = row['Konten']

# Ambil token dan chat_id
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = "7859319589"

# Debug log
print("📦 BOT_TOKEN (first 10):", BOT_TOKEN[:10] + "...")
print("📦 CHAT_ID:", CHAT_ID)
print("📨 PESAN:\n", pesan)

# Kirim ke Telegram
res = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={"chat_id": "7859319589", "text": pesan}
)

print("🧾 RESPONSE:", res.status_code, res.text)
