import os
import requests
import smtplib as smtp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


SENDER_EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

url = "https://sky-scanner3.p.rapidapi.com/flights/search-roundtrip"

querystring = {
    "fromEntityId":"BUD",
    "toEntityId":"BCN",
    "departDate": "2025-03-26",
    "returnDate": "2025-03-29"
    }

headers = {
	"x-rapidapi-key": RAPIDAPI_KEY,
	"x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)


data = response.json()

itineraries = data['data']['itineraries']

pricesort = sorted(itineraries[:40], key= lambda x: x['price']['raw'])

for itinerary in pricesort[:5]:
    print(f"Price: {itinerary['price']['formatted']},  Departure: {itinerary['legs'][0]['departure']}, Arrival: {itinerary['legs'][0]['arrival']}, Returndeparture: {itinerary['legs'][1]['departure']}, ReturnArrival: {itinerary['legs'][1]['arrival']}")
    
lowestprice = pricesort[0]['price']['raw']



def send_email():
    subject = "Barcelona repjegy noti"
    body = f"""
    <html>
        <body>
            <p>Repjegy {lowestprice} EUR</p> <br>
            <p><a href="https://www.skyscanner.de" target="_blank">Katt ide</a></p>
        </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        server = smtp.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("sent")

    except Exception as e:
        print("hiba történt")


if lowestprice < 100:
    send_email()

    



