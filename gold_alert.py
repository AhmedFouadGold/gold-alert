import requests
import time
import smtplib
import urllib3

urllib3.disable_warnings()

# ====== SETTINGS ======
TARGET_PRICE = 100

EMAIL = "ahmed.fouad@newegygold.com"
PASSWORD = "fpksjcxfhssdrdcb"

# ====== FUNCTIONS ======

def get_gold_price():
    url = "https://api.gold-api.com/price/XAU"
    response = requests.get(url, verify=False)  
    data = response.json()
    return data['price']

def send_email(price):
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)

    message = f"Subject: Gold Alert\n\nGold price reached: {price}"

    server.sendmail(EMAIL, EMAIL, message)
    server.quit()

# ====== LOOP ======

while True:
    try:
        price = get_gold_price()
        print("Current price:", price)

        if price >= TARGET_PRICE:
            send_email(price)
            print("✅ Email Sent!")
            break

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
