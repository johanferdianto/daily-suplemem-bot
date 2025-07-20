import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import requests
import os
import requests

# Token & Chat ID
TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

# Autentikasi Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('DailySuplemen/dailysuplemen-f678a059f076.json', scope)
client = gspread.authorize(creds)

# Buka Google Sheet
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qKWUIB9QcJ2Yh-B5ciTxiDRWdBcpKcEGO2cNFf2zsro")
sheet = spreadsheet.worksheet("Jadwal")

# Ambil semua data
data = sheet.get_all_records()

# Hari ini
day_map = {
    'Monday': 'Senin',
    'Tuesday': 'Selasa',
    'Wednesday': 'Rabu',
    'Thursday': 'Kamis',
    'Friday': 'Jumat',
    'Saturday': 'Sabtu',
    'Sunday': 'Minggu'
}
today_eng = datetime.datetime.now().strftime('%A')
today_id = day_map[today_eng]

# Cari baris sesuai hari
today_row = next((row for row in data if row['Hari'] == today_id), None)

if today_row:
    rotasi = today_row.get('Rotasi', '-')
    deskripsi = today_row.get('Deskripsi', '-')
    suplemen = today_row.get('Daftar Suplemen', '')

    pesan = f"📅 *Jadwal Suplemen Hari Ini* ({today_id})\n\n"
    pesan += f"🔁 *Rotasi:* {rotasi}\n"
    pesan += f"🎯 *Fokus:* {deskripsi}"
    if suplemen:
        pesan += f"\n💊 *Suplemen:* {suplemen}"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, data=payload)
    print("✅ Reminder dikirim:", response.status_code)
else:
    print("❌ Hari tidak ditemukan dalam Sheet.")
