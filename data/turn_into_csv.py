# Python 3.6
# Authors: Maximilian Seidler, Mariia Stazherova
# Reads raw Twitter streaming data and collects it in a CSV-file

import re
import emoji
import csv
import time
import glob
from collections import Counter


def contains_target_emoji(tweet):
    """Returns True if at least one of the target emojis appears in a tweet.
    Returns False otherwise."""
    emojis = set(c for c in tweet if c in emoji.UNICODE_EMOJI)
    targets = {'😨', '😱', '😍', '❤', '😳', '😮', '😡', '😠', '😢', '😔',
               '😖', '🤢'}
    return len(emojis & targets) > 0


def make_tweet_list(filepath):
    """Given a file-path this function identifies the the boundaries of a tweet
    and makes a list with each element being a tweet."""
    tweets = []
    with open(filepath, encoding='UTF-8') as fp:
        current = ''
        for line in fp:
            # if a user id is found...
            if re.findall(r"(\d{18})", line):
                # ...we are at the beginning of a new tweet
                previous = current
                current = line
                if contains_target_emoji(previous):
                    tweets.append(previous)
            # if not, then the line is still part of the current tweet
            else:
                current += line
    # element 0 is an empty string, so it doesn't need to be returned
    return tweets[1:]


def cleaned_up(tweet):
    """Given a tweet, this function does some preprocessing by removing
    noise.

    Example:
        "2017-08-16 19:10:26","897898364787978241","RT @tushy_com: RT if you
        wouldn't mind being stuck in between @rileyreidx3 &amp; @AidraFOfficial!
        😍 #tushy https://t.co/mkUvdIvyeW"

        becomes:

        "RT if you wouldn't mind being stuck in between 😍 tushy"
    """
    # find 18 digit user_id...
    user_id = re.findall(r"(\d{18})", tweet)
    # to filter out date and user_id
    _, _, tweet = tweet.partition(user_id[0] + "\",")
    # filter out user mentions
    tweet = re.sub("(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z_]+[A-Za-z0-9_]+)", "", tweet)
    # filter out re-tweet indicatiors
    tweet = re.sub("RT : ", '', tweet)
    # filter out links
    tweet = re.sub("(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", '', tweet)
    # remove '#' form hashtags
    tweet = re.sub("#", '', tweet)
    # remove '&amp';
    tweet = re.sub("&amp;", '', tweet)
    # filter out non-ascii characters but leaving emojis
    emoji_pat = '[\U0001F300-\U0001F64F\U0001F680 - \U0001F6FF\u2600-\u26FF\u2700-\u27BF]'
    reg = re.compile(r'({})|[^\x00-\x7F]'.format(emoji_pat))  # from non-ascii chars return emojis
    tweet = reg.sub(lambda x: '{}'.format(x.group(1)) if x.group(1) else '', tweet)
    # remove beginning and ending quotations marks
    tweet = tweet[1:-2]
    # remove extra whitespace
    tweet = ' '.join(tweet.split())
    # remove newline at the end of tweet and return clean tweet
    return tweet


def extract_emojis(tweet):
    """Searches for emoji characters in a string and removes them.
    Returns a (string, emojis) tuple."""
    emojis = list(c for c in tweet if c in emoji.UNICODE_EMOJI)
    for emoji_ in emojis:
        tweet = tweet.replace(emoji_, '')

    return (tweet, emojis)


def identify_emotions(emojis):
    """Given a list of emojis it identifies the corresponding emotion.
    Returns a list of strings."""
    emotions = set()
    for emoji_ in set(emojis):
        if emoji_ == '😨' or emoji_ == '😱':
            emotions.add("fear")
        if emoji_ == '😍' or emoji_ == '❤':
            emotions.add("happiness")
        if emoji_ == '😳' or emoji_ == '😮':
            emotions.add("surprise")
        if emoji_ == '😡' or emoji_ == '😠':
            emotions.add("anger")
        if emoji_ == '😢' or emoji_ == '😔':
            emotions.add("sadness")
        if emoji_ == '😖' or emoji_ == '🤢':
            emotions.add("disgust")
    return list(emotions)


def write_to_csv(tweets):
    """Given a list of raw tweets, this function creates a csv-file and
    writes per row the corresponding emotion and the (cleaned up) tweet."""
    csvfile = open('corpus.csv', 'a')
    corpuswriter = csv.writer(csvfile, delimiter=';')
    for tweet in tweets:
        clean_tweet, emojis = extract_emojis(cleaned_up(tweet))
        emotions = identify_emotions(emojis)
        for emotion in emotions:
            corpuswriter.writerow([emotion, clean_tweet])
    csvfile.close()


def data_collector():
    """This function looks in the for raw streaming data in the '/streaming'
    directory and passes thoses file paths to other functions."""
    start_time = time.time()
    for filepath in glob.glob('../streaming/tweets*.txt'):
        print("Writing the tweets from {} into the corpus.csv".format(filepath))
        tweets = make_tweet_list(filepath)
        write_to_csv(tweets)
    print("Corpus-building completed in {0:.2f} seconds".format((time.time() - start_time)))


def give_emotion_frequency():
    """This helper function prints out the frequencies of the six emotions in
    our corpus."""
    emotions_list = []
    with open('corpus.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        for row in csvreader:
            emotions_list.append(row[0])

    c = Counter(emotions_list)
    csvfile.close()
    return c.most_common()


if __name__ == "__main__":
    data_collector()
    print(give_emotion_frequency())
