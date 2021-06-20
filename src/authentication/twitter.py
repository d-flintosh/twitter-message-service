from math import ceil

from TwitterAPI import TwitterAPI

from src.authentication.twitter_auth import get_credentials


class Twitter:
    def __init__(self, school: str):
        credentials = get_credentials()
        self.application_credentials = credentials.get('application_account')
        self.twitter_credentials = credentials.get(school)

    def send_tweet(self, content: str):
        self._send_tweet(
            application_credentials=self.application_credentials,
            twitter_credentials=self.twitter_credentials,
            content=content
        )

    def _send_tweet(self, application_credentials: dict, twitter_credentials: dict, content: str):
        print(f'Sending tweet to: {twitter_credentials.get("twitter_handle")}')
        twitter_api = TwitterAPI(
            consumer_key=application_credentials.get('consumer_key'),
            consumer_secret=application_credentials.get('consumer_secret'),
            access_token_key=twitter_credentials.get('access_token_key'),
            access_token_secret=twitter_credentials.get('access_token_secret')
        )
        tweets_to_send = self._format_for_tweet(content=content)

        for tweet in tweets_to_send:
            response = twitter_api.request('statuses/update', {'status': tweet})
            print(f'The response code: {response.status_code}')

    def _format_for_tweet(self, content: str):
        punctuation = ['.']
        tweets = []
        tweet_count = 0
        expected_tweet_count = ceil(len(content)/140)

        while len(content) > 140:
            tweet_count += 1
            cut_where, cut_why = max((content.rfind(punc, 0, 136), punc) for punc in punctuation)
            if cut_where <= 0:
                cut_where = content.rfind(' ', 0, 136)
                cut_why = ' '
            cut_where += len(cut_why)
            tweets.append(content[:cut_where].rstrip() + f' {tweet_count}/{expected_tweet_count}')
            content = content[cut_where:].lstrip()

        final_content = f'{content} {tweet_count+1}/{expected_tweet_count}' if expected_tweet_count > 1 else content
        tweets.append(final_content)
        return tweets
