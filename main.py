# stockAlert.py
#
# Python Bootcamp Day 36 - Stock Trading News Alert
#
# Usage:
#   Using Twilio, NewsAPI and AlphaAdvantageAPI, send a text with the top 3
# headlines if a chosen stock is up or down over a given percentage (5%)
#
# Marceia Egler December 8, 2021

import requests
import os
from requests.api import head
from twilio.rest import Client
from dotenv import load_dotenv
import datetime as dt
from newsapi import NewsApiClient
import html

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
news_api = os.getenv("newsApiKey")
stock_api = os.getenv("stockApiKey")

STOCK = "KMX"
COMPANY_NAME = "CarMax"
PERCENT_CHANGE = 5


def calculate_price_change(api: str, symbol: str) -> int:
    stock_params = {
        "apikey": api,
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
    }
    r = requests.get("https://www.alphavantage.co/query", params=stock_params)
    r.raise_for_status()
    data = r.json()
    today = dt.date.today()
    yesterday_date = str(today - dt.timedelta(days=1))
    day_before_date = str(today - dt.timedelta(days=2))
    yesterday_price = round(
        float(data["Time Series (Daily)"][yesterday_date]["4. close"]), 2
    )

    day_before_price = round(
        float(data["Time Series (Daily)"][day_before_date]["4. close"]), 2
    )

    compute_change = round(
        (yesterday_price - day_before_price) / day_before_price * 100
    )

    return compute_change


def upOrDown():
    up_down = None

    if change > PERCENT_CHANGE:
        up_down = "🔺"
    elif change < (PERCENT_CHANGE * -1):
        up_down = "🔻"
    return up_down


def get_news(symbol: str) -> list:
    news_params = {
        "q": symbol,
        "language": "en",
        "apiKey": news_api,
    }

    r = requests.get("https://newsapi.org/v2/everything", params=news_params)
    r.raise_for_status()
    data = r.json()
    top_news = data["articles"][:3]
    return top_news


def send_message(symbol: str, upOrDown, percent_change=PERCENT_CHANGE):
    for article in news:
        headline = article["title"]
        body = html.unescape(article["description"])
        if change > percent_change or change < (percent_change * -1):
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f"{symbol}: {up_down}{change}%\nHeadline: {headline}\nBrief: {body}",
                from_="+18506088282",
                to="+14076171799",
            )

            print(message.status)


if __name__ == "__main__":
    change = calculate_price_change(stock_api, STOCK)
    up_down = upOrDown()
    news = get_news(STOCK)
    send_message(STOCK, up_down)
