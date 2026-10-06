from urllib.parse import urlencode
import pytest


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


def test_atualizacao_parcial_preserva_demais_campos(api, token, booking):
    booking_id, original = booking
    status, body = api('PATCH', f'/booking/{booking_id}', {'totalprice': 300}, token)
    expected = {**original, 'totalprice': 300}
    assert status == 200 and body == expected
    assert api('GET', f'/booking/{booking_id}') == (200, expected)


def test_filtro_encontra_o_id_criado(api, booking):
    booking_id, original = booking
    status, body = api('GET', '/booking?' + urlencode({'firstname': original['firstname']}))
    assert status == 200
    assert {'bookingid': booking_id} in body


@pytest.mark.parametrize('credential', [None, 'invalid-portfolio-token'], ids=['sem-token', 'token-invalido'])
@pytest.mark.parametrize('method', ['PUT', 'PATCH', 'DELETE'])
def test_mutacao_sem_autorizacao_nao_altera_reserva(api, booking, method, credential):
    booking_id, original = booking
    data = None if method == 'DELETE' else {**original, 'totalprice': 1}
    status, _ = api(method, f'/booking/{booking_id}', data, credential)
    assert status == 403
    assert api('GET', f'/booking/{booking_id}') == (200, original)


def test_exclusao_autenticada_remove_reserva(api, token, booking):
    booking_id, _ = booking
    assert api('DELETE', f'/booking/{booking_id}', token=token)[0] == 201
    assert api('GET', f'/booking/{booking_id}')[0] == 404


def test_credenciais_invalidas_nao_retornam_token(api):
    status, body = api('POST', '/auth', {'username': 'invalid-portfolio', 'password': 'invalid'})
    assert status == 200
    assert body == {'reason': 'Bad credentials'}
