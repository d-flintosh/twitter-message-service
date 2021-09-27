from dataclasses import dataclass
from typing import List
from unittest.mock import Mock, patch, call

import pytest

from src.authentication.twitter import Twitter


class TestTwitter:
    @dataclass
    class Params:
        expected_twitter_api_calls: List
        content: str

    @dataclass
    class Fixture:
        mock_twitter_api_constructor: Mock
        mock_twitter_api: Mock
        expected_twitter_api_calls: List

    @pytest.fixture(
        ids=['Under 140 characters', 'Over 140 characters', 'Over 280 Characters'],
        params=[
            Params(
                content='the content',
                expected_twitter_api_calls=[
                    call('statuses/update', {'status': 'the content'})
                ]
            ),
            Params(
                content='the content has a first name. it is oscar. the content has a second name it is meyer\nthis is not long enough so the content has a third name but I forgot what it was',
                expected_twitter_api_calls=[
                    call('statuses/update', {'status': 'the content has a first name. it is oscar. the content has a second name it is meyer 1/2'}),
                    call('statuses/update', {'status': 'this is not long enough so the content has a third name but I forgot what it was 2/2'})
                ]
            ),
            Params(
                content='the content has a first name. it is oscar. the content has a second name it is meyer\nthis is not long enough so the content has a third name but I forgot what it was. here we go throwing shit\nat the fan trying to make this over 280 characters. am I there yet. Almost. But not quite.',
                expected_twitter_api_calls=[
                    call('statuses/update', {'status': 'the content has a first name. it is oscar. the content has a second name it is meyer 1/3'}),
                    call('statuses/update', {'status': 'this is not long enough so the content has a third name but I forgot what it was. here we go throwing shit 2/3'}),
                    call('statuses/update', {'status': 'at the fan trying to make this over 280 characters. am I there yet. Almost. But not quite. 3/3'})

                ]
            )
        ])
    @patch('src.authentication.twitter.get_credentials')
    @patch('src.authentication.twitter.TwitterAPI')
    def setup(self, mock_twitter_api_constructor, mock_credentials, request):
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
        Twitter(school='some_school').send_tweet(content=request.param.content)
        return TestTwitter.Fixture(
            mock_twitter_api_constructor=mock_twitter_api_constructor,
            mock_twitter_api=mock_twitter_api,
            expected_twitter_api_calls=request.param.expected_twitter_api_calls
        )

    def test_twitter_api_called(self, setup: Fixture):
        setup.mock_twitter_api_constructor.assert_has_calls([
            call(
                consumer_key='api_foo',
                consumer_secret='secret_foo',
                access_token_key='school_access_foo',
                access_token_secret='school_access_secret_foo'
            )
        ], any_order=True)

    def test_twitter_request(self, setup: Fixture):
        print(setup.mock_twitter_api.request.mock_calls)
        setup.mock_twitter_api.request.assert_has_calls(setup.expected_twitter_api_calls, any_order=True)
