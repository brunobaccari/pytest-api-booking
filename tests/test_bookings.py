from urllib.parse import urlencode


def test_criacao_pode_ser_consultada_com_contrato_completo(api, booking):
    booking_id, expected = booking
    status, body = api('GET', f'/booking/{booking_id}')
    assert status == 200
    assert body == expected
    assert type(body['totalprice']) is int
    assert type(body['depositpaid']) is bool


def test_atualizacao_total_e_persistida(api, token, booking):
    booking_id, original = booking
    updated = {**original, 'totalprice': 275, 'depositpaid': False, 'additionalneeds': 'Dinner'}
    status, body = api('PUT', f'/booking/{booking_id}', updated, token)
    assert status == 200 and body == updated
    assert api('GET', f'/booking/{booking_id}') == (200, updated)

