import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import datetime
import json
import tempfile

# 🔐 Ambil dari GitHub Secrets
TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

# 📗 Scope akses Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 🔑 File kredensial yang kamu simpan di repo

# Simpan secret ke file temporary
json_data = os.environ['GOOGLE_CREDENTIALS_JSON']
with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_json:
    temp_json.write(json_data)
    temp_json_path = temp_json.name

# Pakai path sementara ini untuk autentikasi
creds = ServiceAccountCredentials.from_json_keyfile_name(temp_json_path, scope)

client = gspread.authorize(creds)

# 📄 URL spreadsheet kamu (share ke service account!)
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qKWUIB9QcJ2Yh-B5ciTxiDRWdBcpKcEGO2cNFf2zsro")
sheet = spreadsheet.worksheet("Jadwal")

# 🕒 Ambil hari ini
hari_map = {
    'Monday': 'Senin',
    'Tuesday': 'Selasa',
    'Wednesday': 'Rabu',
    'Thursday': 'Kamis',
    'Friday': 'Jumat',
    'Saturday': 'Sabtu',
    'Sunday': 'Minggu'
}
today = datetime.datetime.utcnow().strftime('%A')
hari_ini = hari_map[today]

# 📊 Baca semua data jadwal
data = sheet.get_all_records()
row = next((x for x in data if x['Hari'] == hari_ini), None)

if row:
    rotasi = row.get('Rotasi', '-')
    deskripsi = row.get('Deskripsi', '-')
    suplemen = row.get('Daftar Suplemen', '')

    pesan = f"📅 *Jadwal Suplemen Hari Ini* ({hari_ini})\n\n"
    pesan += f"🔁 *Rotasi:* {rotasi}\n"
    pesan += f"🎯 *Fokus:* {deskripsi}"
    if suplemen:
        pesan += f"\n💊 *Suplemen:* {suplemen}"

    # 🚀 Kirim ke Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "Markdown"
    })

    print("✅ Reminder dikirim")
else:
    print("❌ Hari tidak ditemukan dalam sheet.")
