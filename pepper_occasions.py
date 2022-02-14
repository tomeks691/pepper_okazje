import os
import time
from os.path import exists

import telepot
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
from requests_html import HTMLSession


def send_deals(link):
    load_dotenv(find_dotenv())
    api_bot = os.environ.get("api")
    chat_id = os.environ.get("user_id")
    bot = telepot.Bot(api_bot)
    bot.sendMessage(chat_id, link)


def check_if_link_exist(link):
    link_exist = False
    if not exists("links.txt"):
        f = open("links.txt", "x")
        f.close()

    with open("links.txt", "r") as f:
        links = f.read()
        if link not in links:
            send_deals(link)
        else:
            link_exist = True
    if not link_exist:
        with open("links.txt", "a") as f:
            f.write(link + "\n")


def get_sale(group_url):
    session = HTMLSession()
    r = session.get(group_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    link = soup.select(".thread-title > a")[0].get("href")
    check_if_link_exist(link)


if not exists("pepper_groups_to_check.txt"):
    print("First create file pepper_groups_to_check.txt")
    exit()

with open('pepper_groups_to_check.txt') as f:
    group_urls = f.read().splitlines()
    if len(group_urls) == 0:
        print("Add some links to pepper_groups_to_check.txt")
for group_url in group_urls:
    get_sale(group_url)
    time.sleep(2)
