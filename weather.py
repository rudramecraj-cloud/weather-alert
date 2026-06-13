import os
import requests
import smtplib
from email.message import EmailMessage

API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITY = "Kochi"

URL = (
    f"https://api.openweathermap.org/data/2.5/forecast"
    f"?q={CITY}&appid={API_KEY}&units=metric"
)

response = requests.get(URL)
data = response.json()
print("API KEY EXISTS:", API_KEY is not None)
print("STATUS CODE:", response.status_code)
print(data)

alert = False
reason = []

for forecast in data["list"][:8]:  # next 24 hrs

    temp = forecast["main"]["temp"]

    weather = forecast["weather"][0]["main"]

    if temp > 35:
        alert = True
        reason.append(f"High temperature: {temp}°C")

    if weather.lower() == "rain":
        alert = True
        reason.append("Rain predicted")

if alert:

    msg = EmailMessage()

    msg["Subject"] = "⚠ Weather Alert"
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = os.getenv("EMAIL_ADDRESS")

    msg.set_content("\n".join(reason))

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            os.getenv("EMAIL_ADDRESS"),
            os.getenv("EMAIL_PASSWORD")
        )

        smtp.send_message(msg)

    print("Alert email sent!")

else:
    print("No alert needed.")