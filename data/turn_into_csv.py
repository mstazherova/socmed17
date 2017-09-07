import re
import emoji

# reading in the tweets and putting them into an array
tweets = []
with open('sample_tweets.txt', encoding='UTF-8') as fp:
    current = ''
    for line in fp:
        # if a user id is found...
        if re.findall(r"(\d{18})", line):
            # ... we are at the beginning of a new tweet
            previous = current
            current = line
            tweets.append(previous)
        # if not, then the line is still part of the current tweet
        else:
            current += line
# the first element is now an empty string so it gets removed
tweets = tweets[1:]


def extract_emojis(tweet):
    emojis = list(c for c in tweet if c in emoji.UNICODE_EMOJI)
    for emoji_ in emojis:
        tweet = tweet.replace(emoji_, "")

    return (tweet, emojis)


def identify_emotions(emojis):
    emotions = []
    for emoji_ in set(emojis):
        if emoji_ == '😨' or emoji_ == '😱':
            emotions.append("fear")
        if emoji_ == '😍' or emoji_ == '❤':
            emotions.append("happiness")
        if emoji_ == '😳' or emoji_ == '😮':
            emotions.append("surprise")
        if emoji_ == '😡' or emoji_ == '😠':
            emotions.append("anger")
        if emoji_ == '😢' or emoji_ == '😔':
            emotions.append("sadness")
        if emoji_ == '😖' or emoji_ == '🤢':
            emotions.append("disgust")
    return emotions


for tweet in tweets:
    # find 18 digit user_id...
    user_id = re.findall(r"(\d{18})", tweet)
    # to filter out date and user_id
    _, _, tweet = tweet.partition(user_id[0] + "\",")
    # filter out user mentions
    tweet = re.sub("(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z_]+[A-Za-z0-9_]+)", '', tweet)
    # filter out re-tweet indicatiors
    tweet = re.sub("RT : ", '', tweet)
    # filter out links
    tweet = re.sub("(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", '', tweet)
    # filter out non-ascii characters but leaving emojis
    emoji_pat = '[\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u26FF\u2700-\u27BF]'
    reg = re.compile(r'({})|[^\x00-\x7F]'.format(emoji_pat))  # from non-ascii chars return emojis
    tweet = reg.sub(lambda x: '{}'.format(x.group(1)) if x.group(1) else '', tweet)
    # remove newline at the end of tweet
    tweet = tweet[:-1]

    tweet_plus_emojis = extract_emojis(tweet)
    print(tweet_plus_emojis)
    print(identify_emotions(tweet_plus_emojis[1]))
