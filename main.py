import base64

from TwitterAPI import TwitterAPI

from src.authentication.twitter_auth import get_credentials


def entrypoint(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
                        event. The `@type` field maps to
                         `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
                        The `data` field maps to the PubsubMessage data
                        in a base64-encoded string. The `attributes` field maps
                        to the PubsubMessage attributes if any is present.
         context (google.cloud.functions.Context): Metadata of triggering event
                        including `event_id` which maps to the PubsubMessage
                        messageId, `timestamp` which maps to the PubsubMessage
                        publishTime, `event_type` which maps to
                        `google.pubsub.topic.publish`, and `resource` which is
                        a dictionary that describes the service API endpoint
                        pubsub.googleapis.com, the triggering topic's name, and
                        the triggering event type
                        `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
    """

    data = base64.b64decode(event['data']).decode('utf-8')
    credentials = get_credentials()
    application_credentials = credentials.get("application_account")
    print(f'The data {data}')
    accounts_to_tweet = [
        application_credentials,
        credentials.get("fsu")
    ]
    for account in accounts_to_tweet:
        send_tweet(application_credentials=application_credentials, twitter_credentials=account, content=data)


def send_tweet(application_credentials: dict, twitter_credentials: dict, content: str):
    print(f'Sending tweet to: {twitter_credentials.get("twitter_handle")}')
    api = TwitterAPI(
        consumer_key=application_credentials.get('consumer_key'),
        consumer_secret=application_credentials.get('consumer_secret'),
        access_token_key=twitter_credentials.get('access_token_key'),
        access_token_secret=twitter_credentials.get('access_token_secret')
    )
    response = api.request('statuses/update', {'status': content})
    print(f'The response code: {response.status_code}')
