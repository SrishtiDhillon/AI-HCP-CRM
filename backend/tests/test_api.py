import pytest
from app.routes import chat


def test_health_without_ai_credentials(client):
    assert client.get('/health').json() == {'status': 'Running'}


def test_create_and_list_hcp(client, hcp):
    assert client.get('/hcp').json() == [hcp]


@pytest.mark.parametrize('name', ['', '   ', 'x' * 101])
def test_invalid_hcp_name(client, hcp, name):
    assert client.post('/hcp', json={**hcp, 'name': name}).status_code == 422


def test_crud_round_trip(client, payload):
    created = client.post('/interaction', json=payload)
    assert created.status_code == 200
    record = created.json()
    assert record['summary'] == payload['summary']
    assert client.get(f"/interaction/{payload['hcp_id']}").json() == [record]
    updated = client.put(f"/interaction/{record['id']}", json={**payload, 'summary': 'Updated demo notes'})
    assert updated.status_code == 200
    assert updated.json()['summary'] == 'Updated demo notes'
    assert client.delete(f"/interaction/{record['id']}").status_code == 200
    assert client.get(f"/interaction/{payload['hcp_id']}").json() == []


def test_optional_fields(client, payload):
    payload.pop('follow_up_date')
    payload.pop('products_discussed')
    response = client.post('/interaction', json=payload)
    assert response.status_code == 200
    assert response.json()['follow_up_date'] is None
    assert response.json()['products_discussed'] == ''


@pytest.mark.parametrize('change', [
    {'summary': ''}, {'summary': '  '}, {'summary': 'x' * 10001},
    {'interaction_date': 'not-a-date'}, {'follow_up_date': '2026-09-01'},
    {'hcp_id': 0}, {'hcp_id': -1},
])
def test_bad_interaction_is_rejected_without_writing(client, payload, change):
    response = client.post('/interaction', json={**payload, **change})
    assert response.status_code == 422
    assert client.get(f"/interaction/{payload['hcp_id']}").json() == []


def test_missing_hcp_returns_404_without_writing(client, payload):
    assert client.post('/interaction', json={**payload, 'hcp_id': 999}).status_code == 404
    assert client.get('/interaction/999').json() == []


def test_update_missing_record_returns_404_not_500(client, payload):
    assert client.put('/interaction/999', json=payload).status_code == 404


def test_failed_update_preserves_existing_data(client, payload):
    record = client.post('/interaction', json=payload).json()
    response = client.put(f"/interaction/{record['id']}", json={**payload, 'hcp_id': 999, 'summary': 'Should not persist'})
    assert response.status_code == 404
    assert client.get(f"/interaction/{payload['hcp_id']}").json() == [record]


def test_delete_missing_record(client):
    assert client.delete('/interaction/999').status_code == 404


@pytest.mark.parametrize('message', ['', '  ', 'x' * 10001])
def test_invalid_chat_input(client, message):
    assert client.post('/chat/', json={'message': message}).status_code == 422


def test_chat_without_key_has_clear_error(client):
    response = client.post('/chat/', json={'message': 'List HCPs'})
    assert response.status_code == 503
    assert 'Structured logging is still available' in response.json()['detail']


def test_provider_failure_does_not_expose_details(client, monkeypatch):
    monkeypatch.setenv('GROQ_API_KEY', 'test-placeholder')
    def fail(_):
        raise RuntimeError('private-provider-detail')
    monkeypatch.setattr(chat, 'run_agent', fail)
    response = client.post('/chat/', json={'message': 'List HCPs'})
    assert response.status_code == 503
    assert 'private-provider-detail' not in response.text


def test_chat_response_contract_with_stubbed_agent(client, monkeypatch):
    monkeypatch.setenv('GROQ_API_KEY', 'test-placeholder')
    monkeypatch.setattr(chat, 'run_agent', lambda message: f'Received: {message}')
    assert client.post('/chat/', json={'message': 'List HCPs'}).json() == {'response': 'Received: List HCPs'}
