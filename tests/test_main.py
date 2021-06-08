import base64
import json
from dataclasses import dataclass
from unittest.mock import patch, Mock

import pytest
from google.cloud.secretmanager_v1 import AccessSecretVersionResponse, SecretPayload, AccessSecretVersionRequest

from main import get_credentials, send_tweet, entrypoint


class TestEntrypoint:
    @dataclass
    class Fixture:
        mock_send_tweet: Mock
        mock_get_credentials: Mock

    @pytest.fixture
    @patch('main.send_tweet', autospec=True)
    @patch('main.get_credentials', autospec=True)
    def setup(self, mock_get_credentials, mock_send_tweet):
        mock_event = {
            'data': base64.b64encode(b'some content')
        }
        mock_credentials = {
            'foo': 'creds'
        }
        mock_get_credentials.return_value = mock_credentials
        entrypoint(event=mock_event, context=None)
        return TestEntrypoint.Fixture(
            mock_send_tweet=mock_send_tweet,
            mock_get_credentials=mock_get_credentials
        )

    def test_mock_send_tweet_called(self, setup: Fixture):
        setup.mock_send_tweet.assert_called_once_with(
            credentials={
                'foo': 'creds'
            },
            content='some content'
        )

    def test_get_credentials_called(self, setup: Fixture):
        setup.mock_get_credentials.assert_called_once()


class TestSendTweet:
    @dataclass
    class Fixture:
        mock_twitter_api_constructor: Mock
        mock_twitter_api: Mock

    @pytest.fixture
    @patch('main.TwitterAPI')
    def setup(self, mock_twitter_api_constructor):
        mock_twitter_api = mock_twitter_api_constructor.return_value
        mock_credentials = {
            'api_key': 'api_foo',
            'api_secret': 'secret_foo',
            'access_token_key': 'access_foo',
            'access_token_secret': 'access_secret_foo'
        }
        send_tweet(credentials=mock_credentials, content='the content')
        return TestSendTweet.Fixture(
            mock_twitter_api_constructor=mock_twitter_api_constructor,
            mock_twitter_api=mock_twitter_api
        )

    def test_twitter_api_called(self, setup: Fixture):
        setup.mock_twitter_api_constructor.assert_called_once_with(
            consumer_key='api_foo',
            consumer_secret='secret_foo',
            access_token_key='access_foo',
            access_token_secret='access_secret_foo'
        )

    def test_twitter_request(self, setup: Fixture):
        setup.mock_twitter_api.request.assert_called_once_with(
            'statuses/update', {'status': 'the content'}
        )


class TestCredentials:
    expected = {
        'foo': 'bar'
    }

    @dataclass
    class Fixture:
        mock_client: Mock
        actual: dict

    @pytest.fixture
    @patch('main.secretmanager_v1')
    def setup(self, mock_secret_manager):
        mock_client = mock_secret_manager.SecretManagerServiceClient.return_value
        mock_response = Mock(spec=AccessSecretVersionResponse)

        mock_payload = Mock(spec=SecretPayload)

        mock_payload.data = str.encode(json.dumps(TestCredentials.expected))
        mock_response.payload = mock_payload
        mock_client.access_secret_version.return_value = mock_response

        return TestCredentials.Fixture(
            mock_client=mock_client,
            actual=get_credentials()
        )

    def test_access_secret_version_called(self, setup: Fixture):
        request = AccessSecretVersionRequest({
            'name': 'projects/557888643787/secrets/twitter-automation-001/versions/1'
        })
        setup.mock_client.access_secret_version.assert_called_once_with(
            request=request
        )

    def test_result(self, setup: Fixture):
        assert setup.actual == TestCredentials.expected
