import os
import sys
import feedparser
from sql import db
from time import sleep, time
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config

api_id = Config.14004199
api_hash = Config.cc2af30267df60c87bb95b2fe6315aa2
feed_urls = Config.https://subsplease.org/rss/?t&r=720
bot_token = Config.2146356949:AAHUWOT0m_8vHN3oayO2gH5k-6wUplqz6rw
log_channel = Config.1001587828312
check_interval = Config.INTERVAL
max_instances = Config.MAX_INSTANCES

for feed_url in feed_urls:
    if db.get_link(feed_url) == None:
        db.update_link(feed_url, "*")


app = Client(":memory:", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


def create_feed_checker(feed_url):
    def check_feed():
        FEED = feedparser.parse(feed_url)
        entry = FEED.entries[0]
        enid = {entry.id}
        if entry.id != db.get_link(feed_url).link:
                       # ↓ Edit this message as your needs.
            if "eztv.re" in enid or "yts.mx" in enid:   
                message = f"/leech@Chaprileechbot {entry.torrent_magneturi}"
            else:
                message = f"/leech@Chaprileechbot {entry.link}"
            try:
                app.send_message(log_channel, message)
                db.update_link(feed_url, entry.id)
            except FloodWait as e:
                print(f"FloodWait: {e.x} seconds")
                sleep(e.x)
            except Exception as e:
                print(e)
        else:
            print(f"Checked RSS FEED: {entry.id}")
    return check_feed


scheduler = BackgroundScheduler()
for feed_url in feed_urls:
    feed_checker = create_feed_checker(feed_url)
    scheduler.add_job(feed_checker, "interval", seconds=check_interval, max_instances=max_instances)
scheduler.start()
app.run()
