import os
import gspread
import base64
import tempfile
from oauth2client.service_account import ServiceAccountCredentials
import requests
from datetime import datetime

# 🔐 Ambil dan decode kredensial dari Secret
base64_creds = os.environ['GOOGLE_CREDENTIALS_B64']
json_data = base64.b64decode(base64_creds).decode('utf-8')

# 📝 Simpan sementara ke file
with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
    temp.write(json_data)
    temp_json_path = temp.name

# 🔗 Autentikasi Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(temp_json_path, scope)
client = gspread.authorize(creds)

# 📄 Akses spreadsheet dan worksheet
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qKWUIB9QcJ2Yh-B5ciTxiDRWdBcpKcEGO2cNFf2zsro")
sheet = spreadsheet.worksheet("Jadwal")

# 📆 Ambil data berdasarkan hari
hari_ini = datetime.now().strftime('%A')
data = sheet.get_all_records()
row = next((r for r in data if r['Hari'].lower() == hari_ini.lower()), None)

# ❌ Jika tidak ketemu
if not row:
    print("❌ Hari tidak ditemukan dalam Sheet.")
    exit(1)

# 🧠 Buat pesan untuk Telegram
pesan = f"🧠 Suplemen Hari {hari_ini}:\n\n"
for key, val in row.items():
    if key != 'Hari' and val:
        pesan += f"• {key}: {val}\n"

# ✅ Ambil dari environment setelah semua definisi
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

# 🔍 Debug log
print("📦 BOT_TOKEN:", BOT_TOKEN[:10] + "...", f"(panjang: {len(BOT_TOKEN)})")
print("📦 CHAT_ID:", CHAT_ID)
print("📨 PESAN:\n", pesan)

# 🚀 Kirim pesan ke Telegram
response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": pesan}
)

# 🧾 Tampilkan respons Telegram
print("🧾 RESPONSE:", response.status_code, response.text)
