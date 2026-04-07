import requests
import time
import smtplib
import urllib3

urllib3.disable_warnings()

# ====== SETTINGS ======
UP_TARGET = 4685
DOWN_TARGET = 4683

EMAIL = "ahmed.fouad@newegygold.com"
PASSWORD = "fpksjcxfhssdrdcb"

TEST_MODE = True

up_alert_sent = False
down_alert_sent = False

# ====== FUNCTIONS ======

def get_gold_price():
    url = "https://api.gold-api.com/price/XAU"
    response = requests.get(url, verify=False)
    data = response.json()
    return data['price']

def send_email(subject, body):
    print("📩 Trying to send email...")

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)

    message = f"Subject: {subject}\n\n{body}"

    server.sendmail(EMAIL, EMAIL, message)
    server.quit()

    print("✅ Email Sent!")

# ====== LOOP ======

print("🚀 Script started")

while True:
    try:
        price = get_gold_price()
        print("Current price:", price)

        # 🔥 TEST MODE (إجباري مرة واحدة)
        if TEST_MODE:
            send_email(
                "TEST FROM RAILWAY",
                f"System is working. Current price: {price}"
            )
            print("🔥 TEST SENT")
            TEST_MODE = False

        # 📈 UP ALERT
        if price >= UP_TARGET and not up_alert_sent:
            send_email(
                "Gold Break Up",
                f"Gold price reached: {price}"
            )
            print("📈 Up Alert Sent!")
            up_alert_sent = True

        # 📉 DOWN ALERT
        if price <= DOWN_TARGET and not down_alert_sent:
            send_email(
                "Gold Break Down",
                f"Gold price dropped: {price}"
            )
            print("📉 Down Alert Sent!")
            down_alert_sent = True

        time.sleep(60)

    except Exception as e:
        print("❌ Error:", e)
        time.sleep(60)
