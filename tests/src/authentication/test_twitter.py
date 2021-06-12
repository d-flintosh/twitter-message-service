from dataclasses import dataclass
from unittest.mock import Mock, patch, call

import pytest

from src.authentication.twitter import Twitter


class TestTwitter:
    @dataclass
    class Fixture:
        mock_twitter_api_constructor: Mock
        mock_twitter_api: Mock

    @pytest.fixture
    @patch('src.authentication.twitter.get_credentials')
    @patch('src.authentication.twitter.TwitterAPI')
    def setup(self, mock_twitter_api_constructor, mock_credentials):
        mock_twitter_api = mock_twitter_api_constructor.return_value
        mock_credentials.return_value = {
            "application_account": {
                "twitter_handle": "theHandle",
                'consumer_key': 'api_foo',
                'consumer_secret': 'secret_foo',
                'access_token_key': 'access_foo',
                'access_token_secret': 'access_secret_foo'
            },
            "some_school": {
                "twitter_handle": "anotherHandle",
                'consumer_key': 'school_foo',
                'consumer_secret': 'school_secret_foo',
                'access_token_key': 'school_access_foo',
                'access_token_secret': 'school_access_secret_foo'
            }
        }
        Twitter(school='some_school').send_tweet(content='the content')
        return TestTwitter.Fixture(
            mock_twitter_api_constructor=mock_twitter_api_constructor,
            mock_twitter_api=mock_twitter_api
        )

    def test_twitter_api_called(self, setup: Fixture):
        setup.mock_twitter_api_constructor.assert_has_calls([
            call(
                consumer_key='api_foo',
                consumer_secret='secret_foo',
                access_token_key='access_foo',
                access_token_secret='access_secret_foo'
            ),
            call(
                consumer_key='api_foo',
                consumer_secret='secret_foo',
                access_token_key='school_access_foo',
                access_token_secret='school_access_secret_foo'
            )
        ], any_order=True)

    def test_twitter_request(self, setup: Fixture):
        setup.mock_twitter_api.request.assert_has_calls([
            call('statuses/update', {'status': 'the content'}),
            call('statuses/update', {'status': 'the content'})
        ], any_order=True)
