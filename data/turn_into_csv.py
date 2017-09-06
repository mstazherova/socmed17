import re

tweets = []

with open('sample_tweets.txt', encoding="utf-8") as fp:
    for line in fp:
        tweets.append(line)

for element in tweets:
    # find 18 digit user_id...
    user_id = re.findall(r"(\d{18})", element)
    # to filter out date and user_id
    if len(user_id) > 0:
        _, _, tweet = element.partition(user_id[0] + "\",")
    else:
        tweet = element
    # filter out user mentions
    tweet = re.sub("(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z_]+[A-Za-z0-9_]+)", '', tweet)
    # filter out re-tweet indicatiors
    tweet = re.sub("RT : ", '', tweet)
    # filter out links
    tweet = re.sub("(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", '', tweet)
    # filter out non-ascii characters
    tweet = re.sub("[^\x00-\x7f]", '', tweet)
    print(tweet)
