import os
import gspread
import base64
import tempfile
from oauth2client.service_account import ServiceAccountCredentials
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # ⬅️ Tambahan penting

# ========== 🔐 Load Credentials ==========
base64_creds = os.environ['GOOGLE_CREDENTIALS_B64']
json_data = base64.b64decode(base64_creds).decode('utf-8')

with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
    temp.write(json_data)
    temp_json_path = temp.name

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(temp_json_path, scope)
client = gspread.authorize(creds)

# ========== 📅 Setup ==========
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qKWUIB9QcJ2Yh-B5ciTxiDRWdBcpKcEGO2cNFf2zsro")

# Mapping hari
map_hari = {
    "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
    "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
}
hari_eng = datetime.now(ZoneInfo("Asia/Jakarta")).strftime('%A')
hari_ini = map_hari[hari_eng]

# ========== 💬 Fungsi Kirim ==========
def send_to_telegram(text):
    return requests.post(
        f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/sendMessage",
        data={"chat_id":"7859319589", "text": text}
    )

def get_konten(sheetname):
    sheet = spreadsheet.worksheet(sheetname)
    rows = sheet.get_all_records()
    row = next((r for r in rows if r['Hari'].lower() == hari_ini.lower()), None)
    return row['Konten'] if row else None

# ========== 🚀 Jalankan Dua Reminder ==========
konten_full = get_konten("Jadwal-Full")
konten_lite = get_konten("Jadwal-Lite")

if konten_full:
    send_to_telegram(konten_full)

if konten_lite:
    send_to_telegram(konten_lite)
