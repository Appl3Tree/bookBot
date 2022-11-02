#!/usr/bin/env python3
import requests
import discord
import re
from os import name, system, getenv
from math import floor
from datetime import datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup
import webhook_links


def getLastBookTitle():
    with open('/home/forrest/scripts/python/bookBot/.lastBook') as f:
        return f.readlines()

def my_task():
    url = 'https://www.packtpub.com/free-learning'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    bookTitle = soup.select_one('.product-info__title').get_text().strip()
    if bookTitle == getLastBookTitle()[0]:
        exit()
    bookImg = soup.select_one('.product-image')['src']
    bookAuthor = soup.select_one('.free_learning__author').get_text().strip()
    bookPubDate = soup.select_one('.free_learning__product_pages_date').get_text().split('\n')[1]
    bookPages = soup.select_one('.free_learning__product_pages').get_text().split('\n')[1]
    bookDescription = soup.select_one('.free_learning__product_description').get_text().split('\n')[1]
    bookText = discord.Embed(
            title=bookTitle,
            url=url,
            description=bookPubDate + '\n' + bookPages + '\n\n' + bookDescription,
            color=discord.Color.blue()
            )
    if '\n,' in bookAuthor:
        bookAuthor = bookAuthor.replace('\n,', ',')
    if '\n ,' in bookAuthor:
        bookAuthor = bookAuthor.replace('\n,', ',')
    bookText.set_author(name=bookAuthor)
    bookText.set_thumbnail(url=bookImg)

    # Determine hours and minutes until new book.
    pattern = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}')
    script = soup.find("script", text=pattern)
    # Commented due to this actually being false data in PacktPub's Javascript. The books are only available for 24 hours and they don't account for timezones in their scripts.
    # if script:
    #     match = pattern.search(script.text)
    #     if match:
    #         expiration_year = int(match.group(0)[0:4])
    #         expiration_month = int(match.group(0)[5:7])
    #         expiration_day = int(match.group(0)[8:10])
    #         expiration = datetime(expiration_year, expiration_month, expiration_day, 7, 0)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current = datetime.now()
    expiration = current + timedelta(days=1)
    expiration = expiration.replace(hour=0, minute=0, second=0, microsecond=0)
    countdown = (expiration - current).total_seconds()
    hours = floor(countdown / 60 / 60)
    countdown -= hours * 60 * 60
    minutes = floor(countdown / 60)
    countdownText = f'{hours}h {minutes}m left to grab this book. Expires on: {expiration.day} {months[expiration.month - 1]}, {expiration.year} at {str(expiration)[11:19]} (UTC).'
    bookText.set_footer(text=countdownText)

    #   Infinity Testing Zone
#   webhook = discord.SyncWebhook.from_url(webhook_links.infinity_testing_zone)
#   webhook.send(embed=bookText)

    #   Infinity
    webhook = discord.SyncWebhook.from_url(webhook_links.infinity)
    webhook.send(embed=bookText)

    #   IT Be Like That Sometimes
#   webhook = discord.SyncWebhook.from_url(webhook_links.it_be_like_that_sometimes)
#   webhook.send(embed=bookText)

    #   SchoolOfOats
    webhook = discord.SyncWebhook.from_url(webhook_links.school_of_oats)
    webhook.send(embed=bookText)
    with open('/home/forrest/scripts/python/bookBot/.lastBook', 'w') as f:
        f.write(bookTitle)

my_task()

