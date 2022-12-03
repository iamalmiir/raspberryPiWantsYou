from time import sleep
from src.lib import get_date
from os import getenv

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Class to handle the application
class App:
    def __init__(self) -> None:
        self.microcenter_url: str = getenv("MICROCENTER_URL")
        self.sendgrid_url: str = getenv("SENDGRID_URL")
        self.greeting_name: str = getenv("GREETING_NAME")
        self.sender_email: str = getenv("SENDER_EMAIL")
        self.email_receiver: str = getenv("EMAIL_RECEIVER")
        self.until: str = "2022-12-31"
        self.in_stock = str

    # Send email to notify user
    def send_email(self) -> None:
        subject = "Raspberry Pi is Back in Stock!"
        body = f"Hey {self.greeting_name}, \n\nRaspberry Pi is back in stock at Microcenter! \n\n{self.microcenter_url}"
        payload = {
            "personalizations": [{"to": [{"email": self.email_receiver}], "subject": subject}],
            "from": {"email": self.sender_email},
            "content": [{"type": "text/plain", "value": body}],
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": getenv("SENDGRID_API_KEY"),
            "X-RapidAPI-Host": getenv("SENDGRID_API_HOST"),
        }
        requests.request("POST", self.sendgrid_url, json=payload, headers=headers)

    # Check if Raspberry Pi is in stock and send email if it is
    def get_html(self):
        # Get HTML from Microcenter
        html: str = requests.get(self.microcenter_url).text
        # Parse HTML
        soup: BeautifulSoup = BeautifulSoup(html, "lxml")
        # Get the in stock status
        inventory = soup.find("div", {"class": "inventory"})
        # Check if Raspberry Pi is in stock
        if inventory is not None:
            self.in_stock = inventory.find("i", {"class": "fa-solid fa-circle-xmark text-burnt"})
        # Keep checking until date is reached or Raspberry Pi is in stock
        while get_date() != self.until:
            # If element is not found, Raspberry Pi is in stock
            if self.in_stock == "None":
                self.send_email()
                break
            else:
                print("Going to sleep for 1 hour...")
                sleep(3600)
