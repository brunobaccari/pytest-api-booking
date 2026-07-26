import json
import os
from dotenv import load_dotenv
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from uuid import uuid4
import pytest

load_dotenv()
BASE_URL = os.environ['API_BASE_URL'].rstrip('/')


@pytest.fixture(scope='session')
def api():
    def request(method, path, data=None, token=None):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        if token:
            headers['Cookie'] = f'token={token}'
        request = Request(BASE_URL + path, method=method, headers=headers,
                          data=json.dumps(data).encode() if data is not None else None)
        try:
            response = urlopen(request, timeout=30)
        except HTTPError as error:
            response = error
        with response:
            raw = response.read().decode()
            body = json.loads(raw) if response.headers.get_content_type() == 'application/json' else raw
            return response.status, body
    return request


@pytest.fixture(scope='session')
def token(api):
    status, body = api('POST', '/auth', {'username': os.environ['API_USER'], 'password': os.environ['API_PASSWORD']})
    assert status == 200 and isinstance(body.get('token'), str)
    return body['token']


@pytest.fixture
def booking(api, token):
    payload = {'firstname': f'QA-{uuid4().hex}', 'lastname': 'Portfolio', 'totalprice': 149,
               'depositpaid': True, 'bookingdates': {'checkin': '2027-03-01', 'checkout': '2027-03-04'},
               'additionalneeds': 'Breakfast'}
    status, body = api('POST', '/booking', payload)
    booking_id = body.get('bookingid') if isinstance(body, dict) else None
    try:
        assert status == 200 and type(booking_id) is int
        assert body['booking'] == payload
        yield booking_id, payload
    finally:
        if booking_id is not None:
            cleanup_status, _ = api('DELETE', f'/booking/{booking_id}', token=token)
            assert cleanup_status in (201, 404, 405), f'Falha ao limpar reserva própria {booking_id}: {cleanup_status}'
