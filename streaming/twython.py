# Twython.
# by Tatjana Scheffler
# A simple example script for corpus collection from Twitter using Tweepy https://github.com/tweepy

import sys
import tweepy
import langid
import csv
import codecs
import logging
from config import TwitterAuth
from http.client import IncompleteRead, HTTPException
from urllib3.exceptions import ProtocolError
from requests.exceptions import ChunkedEncodingError, ConnectionError
import time
from datetime import date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# configurations
auth = tweepy.OAuthHandler(TwitterAuth.CONSUMER_KEY, TwitterAuth.CONSUMER_SECRET)
auth.set_access_token(TwitterAuth.ACCESS_TOKEN, TwitterAuth.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# open log file
logfile = open('twython.log', 'a')

number = 0


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        global old_date
        global writer
        global outfile
        global number
        new_date = date.today()
        if not new_date == old_date:
            outfile.close
            outfile = codecs.open("tweets-" + str(new_date) + ".txt", "ab", "utf-8")
            writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
            old_date = new_date
        try:
            lang = langid.classify(status.text)[0]
            if lang == "en":
                writer.writerow((status.created_at, status.id_str, status.text))
                logger.info('writing tweet #'+str(number)+'...')
                number += 1

        except Exception as e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            sys.exc_clear()
            pass

    def on_error(self, status_code):
        logger.error('Error with status code:', status_code)
        logfile.write(str(time.asctime(time.localtime(time.time()))) + ' Encountered error with status code:' + str(
            status_code) + "\n")
        return True  # Don't kill the stream

    def on_timeout(self):
        logger.warning('Timeout')
        logfile.write(str(time.asctime(time.localtime(time.time()))) + ' Timeout...' + "\n")
        return True  # Don't kill the stream

        # def on_data(self, data):
        #     print data
        #     return True


localtime = time.asctime(time.localtime(time.time()))
logfile.write(localtime + " Tracking 12 emojis\nStarting stream \n")

# open output file
old_date = date.today()
outfile = codecs.open("tweets-" + str(old_date) + ".txt", "ab", "utf-8")
writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')

# terms = [line.strip() for line in open('twython-keywords.txt')]
# stream.filter(track=terms)

while True:
    try:
        # longer timeout to keep SSL connection open even when few tweets are coming in
        stream = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=1000.0)
        logger.info(str(localtime)+' starting streaming...')
        stream.filter(track=[u"\U0001F628", u"\U0001F631", u"\U0001F60D", u"\u2764", u"\U0001F633", u"\U0001F62E",
                     u"\U0001F621", u"\U0001F620", u"\U0001F622", u"\U0001F614", u"\U0001F616", u"\U0001F922"], stall_warnings=True)
    except ChunkedEncodingError:
        pass
    except IncompleteRead:
        logging.error('incompleteRead http.client occured')
        continue
    except ConnectionError:
        logging.error('connection_error occured')
        continue
    except HTTPException:
        logging.error('httpException occured')
        continue
    except ProtocolError:
        logging.error('ProtocolError occured')
        pass
    except KeyboardInterrupt:
        stream.disconnect()
        break

