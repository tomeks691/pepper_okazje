import json
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import telepot

def send_deals(link):
    with open("api_credentials.json") as f:
        api_credentials = json.load(f)
    api_bot = api_credentials["api"]
    chat_id = api_credentials["chat_id"]
    bot = telepot.Bot(api_bot)
    bot.sendMessage(chat_id, link)


def check_if_link_exist(link):
    link_exist = False
    with open("links.txt", "r") as f:
        links = f.read()
        if link not in links:
            send_deals(link)
        else:
            link_exist = True
    if link_exist == False:
        with open("links.txt", "a") as f:
            f.write(link)

session = HTMLSession()
r = session.get("https://www.pepper.pl/kupony/store.sonyentertainmentnetwork.com")
soup = BeautifulSoup(r.content, 'html.parser')
link = soup.select(".thread-title > a")[0].get("href")
title = soup.select(".thread-title > a")[0].get("title")
check_if_link_exist(title)
check_if_link_exist(link)


