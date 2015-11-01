import os
import threading
import requests
import datetime
import time
import configparser
import random

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError


DIRECTORY = os.getcwd() + os.sep + 'images' + os.sep

CMD = 'gsettings set org.gnome.desktop.background picture-uri file://'

SUBREDDIT_GALLERY_NAME = 'earthporn'
SLEEP_TIME_IN_SEC_LOOP = 300
SLEEP_TIME_IN_SEC_GETR = 21600

LOG_FILE = 'log.txt'


def write_log(entry):
    try:
        with open(LOG_FILE, 'a') as output:
            output.write(
                str(datetime.datetime.now()) +
                ': ' +
                entry +
                '\n')
    except Exception:
        pass


class getter(threading.Thread):

    def run(self):
        client = self.setup_connection()
        page = 0
        while True:
            items = self.get_items(client, SUBREDDIT_GALLERY_NAME, page)
            if items:
                self.save_images(items)
                page += 1
            time.sleep(SLEEP_TIME_IN_SEC_GETR)

    def setup_connection(self):
        config = configparser.ConfigParser()
        config.read('auth.ini')
        client_id = config.get('CREDENTIALS', 'client_id')
        client_secret = config.get('CREDENTIALS', 'client_secret')
        client = ImgurClient(client_id, client_secret)
        return client

    def get_items(self, client, subreddit_gallery_name, page=0):
        try:
            return client.subreddit_gallery(
                subreddit_gallery_name,
                sort='time',
                window='week',
                page=page
            )
        except ImgurClientError as e:
            write_log(e.error_message)

    def save_images(self, items):
        for item in items:
            file_name = item.link.split('/')[-1]
            full_path = DIRECTORY + file_name

            # check if the file already exists
            if os.path.isfile(full_path):
                continue

            try:
                # get the file and save it
                r = requests.get(item.link)
                try:
                    with open(full_path, 'wb') as output:
                        # print('Saving: ', full_path)
                        output.write(r.content)
                except Exception as e:
                    write_log(e)
            except Exception as e:
                write_log(e)


class looper(threading.Thread):

    def run(self):
        self.loop()

    def loop(self):
        while True:
            backgrounds = os.listdir(DIRECTORY)
            if backgrounds:
                background = random.choice(backgrounds)
                self.set_background(DIRECTORY + background)
            time.sleep(SLEEP_TIME_IN_SEC_LOOP)

    def set_background(self, file_name):
        # print('Setting: ', file_name)
        os.system(CMD + file_name)


def main():

    if not os.path.exists(DIRECTORY):
        os.mkdir(DIRECTORY)

    # thread looping on background
    looper().start()
    # thread download images
    getter().start()


if __name__ == '__main__':
    main()
