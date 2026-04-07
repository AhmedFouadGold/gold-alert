import requests
import time
import urllib3
import os

urllib3.disable_warnings()

# ====== SETTINGS ======
UP_TARGET = 4685
DOWN_TARGET = 4683

EMAIL = "ahmed.fouad@newegygold.com"
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

up_alert_sent = False
down_alert_sent = False

# ====== FUNCTIONS ======

def get_gold_price():
    url = "https://api.gold-api.com/price/XAU"
    response = requests.get(url, verify=False)
    data = response.json()
    return data['price']

def send_email(subject, body):
    print("📩 Sending email via Resend...")

    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "from": "onboarding@resend.dev",
        "to": EMAIL,
        "subject": subject,
        "html": f"<p>{body}</p>"
    }

    response = requests.post(url, json=data, headers=headers)

    print("📩 Response:", response.status_code, response.text)

# ====== LOOP ======

print("🚀 Script started")

while True:
    try:
        price = get_gold_price()
        print("Current price:", price)

        # 📈 UP ALERT
        if price >= UP_TARGET and not up_alert_sent:
            send_email(
                "Gold Break Up",
                f"Gold price reached: {price}"
            )
            up_alert_sent = True

        # 📉 DOWN ALERT
        if price <= DOWN_TARGET and not down_alert_sent:
            send_email(
                "Gold Break Down",
                f"Gold price dropped: {price}"
            )
            down_alert_sent = True

        time.sleep(60)

    except Exception as e:
        print("❌ Error:", e)
        time.sleep(60)
