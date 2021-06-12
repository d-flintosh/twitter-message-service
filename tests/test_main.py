import base64
from dataclasses import dataclass
from unittest.mock import patch, Mock

import pytest

from main import entrypoint


class TestEntrypoint:
    @dataclass
    class Fixture:
        mock_twitter: Mock
        mock_twitter_constructor: Mock

    @pytest.fixture
    @patch('main.Twitter', autospec=True)
    def setup(self, mock_twitter_constructor):
        mock_event = {
            'data': base64.b64encode(b'some content'),
            'attributes': {
                'school': 'someSchool'
            }
        }
        mock_twitter = mock_twitter_constructor.return_value
        entrypoint(event=mock_event, context=None)
        return TestEntrypoint.Fixture(
            mock_twitter=mock_twitter,
            mock_twitter_constructor=mock_twitter_constructor
        )

    def test_twitter_constructor(self, setup: Fixture):
        setup.mock_twitter_constructor.assert_called_once_with(school='someSchool')

    def test_get_credentials_called(self, setup: Fixture):
        setup.mock_twitter.send_tweet.assert_called_once_with(content='some content')







