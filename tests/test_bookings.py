from urllib.parse import urlencode


def test_criacao_pode_ser_consultada_com_contrato_completo(api, booking):
    booking_id, expected = booking
    status, body = api('GET', f'/booking/{booking_id}')
    assert status == 200
    assert body == expected
    assert type(body['totalprice']) is int
    assert type(body['depositpaid']) is bool

