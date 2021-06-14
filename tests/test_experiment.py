import base64

import pytest

from main import entrypoint


@pytest.mark.skip(reason="only run this manually")
def test_send_message():
    mock_event = {
        'data': base64.b64encode(b'Tina Charles (WAS) 13 pts/7 reb/1 ast. Tiffany Hayes (ATL) 18 pts/2 reb/6 ast. Moriah Jefferson (DAL) 5 pts/1 ast. Kia Nurse (PHO) 9 pts/2 reb/4 ast. Megan Walker (PHO) 6 pts/4 reb/3 ast. Katie Lou Samuelson (SEA) 8 pts/4 ast. Breanna Stewart (SEA) 22 pts/9 reb/5 ast. Sue Bird (SEA) 13 pts/1 reb/4 ast'),
        'attributes': {
            'school': None
        }
    }
    entrypoint(mock_event, None)
