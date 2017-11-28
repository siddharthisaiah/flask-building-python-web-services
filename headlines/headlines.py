#!/usr/bin/env python


import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import requests


app = Flask(__name__)

RSS_FEEDS = {
                'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
                'cnn': 'http://rss.cnn.com/rss/edition.rss%2520',
                'fox': 'http://feeds.foxnews.com/foxnews/latest',
                'iol': 'http://rss.iol.io/iol/all-content-feed'
            }

DEFAULTS = {'publication': 'bbc',
            'city': 'London,UK',
            'currency_from': 'USD',
            'currency_to': 'INR'}
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=40a55eba91bef9d3add157f46b22e4e8"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=e66c15a824634686bd03643369beddf7"
EXCHANGE_API = "e66c15a824634686bd03643369beddf7"


@app.route('/')
def home():
    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news('publication')

    # get customized weather based on user input or defaults
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)

    # get customized currency based on user input or defaults
    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)

    return render_template("home.html",
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           currencies=sorted(currencies))


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    url = WEATHER_URL.format(query)
    data = requests.get(url)
    parsed = json.loads(data.text)
    weather = None

    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"],
                   "country": parsed["sys"]["country"]}

    return weather


def get_rate(frm, to):
    all_currency = requests.get(CURRENCY_URL).text
    parsed = json.loads(all_currency)
    frm_rate = parsed['rates'].get(frm.upper())
    to_rate = parsed['rates'].get(to.upper())

    return to_rate/frm_rate, parsed['rates'].keys()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
