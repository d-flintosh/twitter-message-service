import builtins
import json
from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

from src.authentication.twitter_auth import get_credentials, get_access
from google.cloud.secretmanager_v1 import AccessSecretVersionRequest, AccessSecretVersionResponse, SecretPayload


class TestCredentials:
    expected = {
        'foo': 'bar'
    }

    @dataclass
    class Fixture:
        mock_client: Mock
        actual: dict

    @pytest.fixture
    @patch('src.authentication.twitter_auth.secretmanager_v1')
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
            'name': 'projects/557888643787/secrets/twitter-automation-001/versions/4'
        })
        setup.mock_client.access_secret_version.assert_called_once_with(
            request=request
        )

    def test_result(self, setup: Fixture):
        assert setup.actual == TestCredentials.expected


class TestGetAccess:
    expected = {
        'foo': 'bar'
    }

    @dataclass
    class Fixture:
        mock_get_credentials: Mock
        mock_tweepy: Mock

    @pytest.fixture
    @patch.object(builtins, 'input', lambda _: '1234')
    @patch('src.authentication.twitter_auth.tweepy')
    @patch('src.authentication.twitter_auth.get_credentials')
    def setup(self, mock_get_credentials, mock_tweepy):
        mock_get_credentials.return_value = {
            'application_account': {
                'consumer_key': 'foo',
                'consumer_secret': 'bar'
            }
        }
        mock_tweepy.OAuthHandler.return_value.access_token = 'accessToken'
        mock_tweepy.OAuthHandler.return_value.access_token_secret = 'accessTokenSecret'
        get_access()

        return TestGetAccess.Fixture(
            mock_get_credentials=mock_get_credentials,
            mock_tweepy=mock_tweepy
        )

    def test_get_credentials_called(self, setup: Fixture):
        setup.mock_get_credentials.assert_called_once()

    def test_oauth_handler_called(self, setup: Fixture):
        setup.mock_tweepy.OAuthHandler.assert_called_once_with('foo', 'bar', callback='oob')

    def test_tweepy_get_authorization(self, setup: Fixture):
        setup.mock_tweepy.OAuthHandler.return_value.get_authorization_url.assert_called_once()

    def test_verifier(self, setup: Fixture):
        setup.mock_tweepy.OAuthHandler.return_value.get_access_token.assert_called_once_with('1234')

    def test_set_access_token(self, setup: Fixture):
        setup.mock_tweepy.OAuthHandler.return_value.set_access_token.assert_called_once_with('accessToken', 'accessTokenSecret')