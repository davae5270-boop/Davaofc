import httpx

from bs4 import BeautifulSoup

import re

from datetime import datetime

import time

import json

with open("flag.json", "r", encoding="utf-8") as f:
    FLAGS = json.load(f)
    
# ================= CONFIG =================

BASE = "http://159.69.3.189"

LOGIN_URL = f"{BASE}/login"

GET_RANGE_URL = f"{BASE}/portal/sms/received/getsms"

GET_NUMBER_URL = f"{BASE}/portal/sms/received/getsms/number"

GET_SMS_URL = f"{BASE}/portal/sms/received/getsms/number/sms"

USERNAME = "davae5270@gmail.com" # Ganti Email Ivas

PASSWORD = "dava0987." # Ganti Password Ivas

BOT_TOKEN = "8628381281:AAHgBO0Ptmuj_9t97xiDU9j471nhekZ8z3s" # Pakai Token Bot Mu

SERVICE_SHORT = {
    "WHATSAPP": "WS",
    "TELEGRAM": "TG",
    "GOOGLE": "GO",
    "FACEBOOK": "FB",
    "INSTAGRAM": "IG",
    "SHOPEE": "SP",
    "TOKOPEDIA": "TP",
    "GRAB": "GR",
    "GOJEK": "GJ",
    "TIKTOK": "TT"
}

CHAT_ID = "-1003742958303" #Wajib Pake - Misal -100000

session = httpx.Client(
    follow_redirects=True,
    timeout=30,
    headers={
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }
)

session.cookies.update({ 
    "XSRF-TOKEN": "eyJpdiI6IlRqYklDcWpqNWx4VGZBeC9yNy80ZXc9PSIsInZhbHVlIjoiWE5jbEpKUzZWNkhFT3o5RnZ4OFJVT1o0M1I5UHg0a2FReEE1d3AwT1ZaL2RCQzEyZWpoR3JQZ0JiRldCMmh5TWV4NXFBTVFQcnhYbllpQmN2WUxTR3dkTnZiSWsxdzJnVmg0U1hFOUVDVmUvVDJaRG8vamo2YWd2VVMremhsOXUiLCJtYWMiOiIxYzk4NzQxODExNWUxYzE5YTBiOGJiNDFmYzk4NWY2YmE0MDk0OTc3NDhkNTU3NDIzNzk4MjFjZmUwYjhhZmY3IiwidGFnIjoiIn0%3D",
    "ivas_sms_session": "eyJpdiI6ImNoaHlVS0U2WU5pa05pMk42ODhJdXc9PSIsInZhbHVlIjoiUklRdHF5ODFpNDMxYzg0TmxBYzUyNitVL3VQSUVDem9OY0loTnVjT1JmbWpySjNXVW5PbHo2UTlWOXo2bHVEN0VobHp6eUlMK2hwOTBxVFd3M2JRT2ZoQUVoQTh0enhlUmI0cVFrWks0TXNLUUZzb3o1eS8xQWZPWUFnUWZDc2YiLCJtYWMiOiJlNjUwMzU1M2FhMDVjY2Y0ODJmMjMxZDdlNDgzNGVhMTgzYWVmNWU5ZWM2NDkwM2ExZWY5N2NiYmMyZWVhMzlkIiwidGFnIjoiIn0%3D" # GANTI COOKIE XSRF/IVASMS_SESION TOKEN LU
})

sent_cache = set()

csrf_token = session.cookies.get("XSRF-TOKEN")

# ==========================================

import threading

def delete_later(message_id):
    time.sleep(300)  # auto hapus pesan atur sesuka lu
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"
    session.post(url, data={
        "chat_id": CHAT_ID,
        "message_id": message_id
    })

def tg_send(msg, otp):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🔑 𝘾𝙊𝙋𝙔 𝙊𝙏𝙋", "style": "success", "copy_text": {"text": otp, }}
            ],
            [
                {"text": "𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝙍📍", "url": "t.me/davaofc4", "style": "primary"},
                {"text": "𝘾𝙃𝘼𝙉𝙉𝙀𝙇🌐", "url": "t.me/numberdavaofc", "style": "primary"}
            ]
        ]
    }

    res = session.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "reply_markup": keyboard
    }).json()

    # 🔥 Ambil message_id lalu hapus otomatis
    if res.get("ok"):
        message_id = res["result"]["message_id"]
        threading.Thread(target=delete_later, args=(message_id,)).start()
    
      # ==========================================
def tg_active(msg):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    session.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    })      

# ================= UTILS =================

def escapeHTML(text=""):

    return (text.replace("&", "&amp;")

                .replace("<", "&lt;")

                .replace(">", "&gt;")

                .replace('"', "&quot;")

                .replace("'", "&#39;"))

def extract_otp(text):

    m = re.search(r"\b(\d{3}[- ]?\d{3}|\d{4,6})\b", text)

    return m.group(1) if m else None

def format_phone_number(number):

    if len(number) >= 8:

        return f"{number[:3]}XNXX.COM{number[-4:]}"

    return number

def clean_country(rng):

    country = re.sub(r"\s*\(.*?\)", "", rng)

    country = re.sub(r"\d+", "", country)

    return country.strip().upper()

def extract_service_short(text):
    m = re.search(
        r"(WhatsApp|Telegram|Google|Facebook|Instagram|Shopee|Tokopedia|Grab|Gojek|TikTok)",
        text,
        re.I
    )
    if m:
        return SERVICE_SHORT.get(m.group(1).upper(), "Unknown")
    return "Unknown"

# ================= LOGIN =================

def login():

    global csrf_token

    r = session.get(LOGIN_URL)

    soup = BeautifulSoup(r.text, "html.parser")

    csrf_token = soup.find("input", {"name": "_token"})["value"]

    session.post(LOGIN_URL, data={

        "_token": csrf_token,

        "email": USERNAME,

        "password": PASSWORD

    })

    print("[✓] Login Berhasil..")
    
    print("[✓] Bot Berjalan..")

# ============ GET SENSOR EMAIL ========
def mask_email(email):
    try:
        name, domain = email.split("@")
        if len(name) <= 2:
            masked = name[0] + "••••"
        else:
            masked = name[0] + "••••" + name[-1]
        return f"{masked}@{domain}"
    except:
        return email
        
# ======= AMBIL FLAGS ========
def get_flag(country):
    return FLAGS.get(country.upper(), "🏴‍☠️")        
        
# ================= GET RANGE =================

def get_ranges():

    today = datetime.now().strftime("%Y-%m-%d")

    r = session.post(GET_RANGE_URL, data={

        "_token": csrf_token,

        "from": today,

        "to": today

    })

    soup = BeautifulSoup(r.text, "html.parser")

    ranges = []

    for div in soup.find_all("div", onclick=True):

        if "toggleRange" in div["onclick"]:

            try:

                ranges.append(div["onclick"].split("'")[1])

            except:

                pass

    return list(set(ranges))

# ================= GET NUMBERS =================

def get_numbers(rng):

    today = datetime.now().strftime("%Y-%m-%d")

    r = session.post(GET_NUMBER_URL, data={

        "_token": csrf_token,

        "start": today,

        "end": today,

        "range": rng

    })

    soup = BeautifulSoup(r.text, "html.parser")

    numbers = []

    for div in soup.find_all("div", onclick=True):

        try:

            val = div["onclick"].split("'")[1]

            if val and val != rng:

                numbers.append(val)

        except:

            pass

    return list(set(numbers))

# ================= GET SMS =================

def get_sms(rng, number):

    today = datetime.now().strftime("%Y-%m-%d")

    r = session.post(GET_SMS_URL, data={

        "_token": csrf_token,

        "start": today,

        "end": today,

        "Number": number,

        "Range": rng

    })

    soup = BeautifulSoup(r.text, "html.parser")

    sms_texts = [p.get_text(strip=True) for p in soup.find_all("p")]

    

    if not sms_texts:

        raw_text = soup.get_text(separator="\n", strip=True)

        if raw_text:

            sms_texts = raw_text.split('\n')

            

    return list(set(sms_texts))

# ================= BOT LOOP =================

def run_bot():

    login()

    while True:

        try:

            ranges = get_ranges()

            for rng in ranges:

                country = clean_country(rng)
                flag = get_flag(country)

                for num in get_numbers(rng):

                    for sms in get_sms(rng, num):

                        

                        # 🔥 FIX BUG HARGA: Abaikan jika teksnya adalah harga (contoh: $0.0120)

                        if "$" in sms and len(sms) < 1500:

                            continue

                        otp = extract_otp(sms)

                        if not otp:

                            continue

                        unique_id = f"{num}-{otp}"

                        

                        if unique_id in sent_cache:

                            continue

                        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                        service = extract_service_short(sms)
                        email_mask = mask_email(USERNAME)

                        msg = (

                            f"<b>{flag} {country} | {service} | {format_phone_number(num)}</b>\n"

              

                                       

                        )

                        tg_send(msg, otp)

                        sent_cache.add(unique_id)

                        print("[Otp Terkirim]", otp, "ke", num)

            time.sleep(0)

        except Exception as e:

            print("[ERROR]", e)

            time.sleep(0)

# ================= START =================

run_bot()