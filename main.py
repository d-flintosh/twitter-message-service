import json
import base64
import logging

from TwitterAPI import TwitterAPI
from google.cloud import secretmanager_v1
from google.cloud.secretmanager_v1 import AccessSecretVersionRequest


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
    logging.info(f'The data {data}')

    credentials = get_credentials()
    send_tweet(credentials=credentials, content=data)


def send_tweet(credentials: dict, content: str):
    api = TwitterAPI(
        consumer_key=credentials.get('api_key'),
        consumer_secret=credentials.get('api_secret'),
        access_token_key=credentials.get('access_token_key'),
        access_token_secret=credentials.get('access_token_secret')
    )
    response = api.request('statuses/update', {'status': content})
    logging.info(f'The response code: {response.status_code}')


def get_credentials() -> dict:
    client = secretmanager_v1.SecretManagerServiceClient()
    secret_request = AccessSecretVersionRequest({
        'name': 'projects/557888643787/secrets/twitter-automation-001/versions/1'
    })
    secret = client.access_secret_version(request=secret_request)
    return json.loads(secret.payload.data.decode('UTF-8'))
