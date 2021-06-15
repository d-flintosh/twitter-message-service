import json

import tweepy
from google.cloud import secretmanager_v1
from google.cloud.secretmanager_v1 import AccessSecretVersionRequest


def get_credentials() -> dict:
    client = secretmanager_v1.SecretManagerServiceClient()
    secret_request = AccessSecretVersionRequest({
        'name': 'projects/557888643787/secrets/twitter-automation-001/versions/latest'
    })
    secret = client.access_secret_version(request=secret_request)
    return json.loads(secret.payload.data.decode('UTF-8'))


def get_access():
    credentials = get_credentials()
    consumer_key=credentials.get('application_account').get('consumer_key')
    consumer_secret=credentials.get('application_account').get('consumer_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback='oob')

    auth_url = auth.get_authorization_url()
    print('Authorization URL: ' + auth_url)

    verifier = input('PIN: ').strip()
    auth.get_access_token(verifier)
    print('ACCESS_KEY = "%s"' % auth.access_token)
    print('ACCESS_SECRET = "%s"' % auth.access_token_secret)

    auth.set_access_token(auth.access_token, auth.access_token_secret)
    api = tweepy.API(auth)
    username = api.me().name
    print('Ready to post to ' + username)


if __name__ == "__main__":
    get_access()
