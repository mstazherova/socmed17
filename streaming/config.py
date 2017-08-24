from emoji.unicode_codes import UNICODE_EMOJI

class TwitterAuth:
    CONSUMER_KEY = 'Og9EHMrtpgHs8WJRZlsYA25rZ'
    CONSUMER_SECRET = 'psdfATmllw8pnUJYineEEIYK1pJIdWAqUdCvasYNfVB6u7rtCg'
    ACCESS_TOKEN = '199341516-qy6f8ddhTmv0GnfEOHvZ2xJOtoRxMCggQMm7JBDK'
    ACCESS_TOKEN_SECRET = 'drGWTjdOXfQs0Q8ZcMYunKjJSnygQ0pYZlnTYwo6Kf4dq'

raw_emojis = '😨😱😍❤😳😮😡😠😢😔😖🤢'


def is_valid(e):
    try:
        UNICODE_EMOJI[e]
        return e
    except KeyError:
        pass

LANGUAGE = 'en'

# filter out emojis not in our library
EMOJIS = list(filter(None, [is_valid(e) for e in raw_emojis]))


DOWNLOADED_TWEETS_PATH = 'emoji_twitter_data.txt'
SENTRY_DSN = ''
