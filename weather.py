import os
import requests
import smtplib
from email.message import EmailMessage

# Environment variables from GitHub Secrets
API_KEY = os.getenv("OPENWEATHER_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

CITY = "Kochi,IN"

# Check if API key exists
if not API_KEY:
    print("ERROR: OPENWEATHER_API_KEY not found.")
    exit(1)

# OpenWeatherMap 5-day / 3-hour forecast API
URL = (
    f"https://api.openweathermap.org/data/2.5/forecast"
    f"?q={CITY}&appid={API_KEY}&units=metric"
)

response = requests.get(URL)
data = response.json()

# Handle API errors
if response.status_code != 200:
    print("API Error:")
    print(data)
    exit(1)

alert = False
reasons = []

# Check next 24 hours (8 forecasts × 3 hours)
for forecast in data["list"][:8]:

    temp = forecast["main"]["temp"]
    weather = forecast["weather"][0]["main"].lower()

    if temp > 35:
        alert = True
        reasons.append(f"High temperature expected: {temp}°C")

    if weather == "rain":
        alert = True
        reasons.append("Rain predicted")

# Send email if needed
if alert:

    msg = EmailMessage()

    msg["Subject"] = "⚠ Weather Alert"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    msg.set_content(
        "Weather alert for Kochi:\n\n" +
        "\n".join(reasons)
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        smtp.send_message(msg)

    print("✅ Alert email sent!")

else:
    print("✅ No alert needed.")