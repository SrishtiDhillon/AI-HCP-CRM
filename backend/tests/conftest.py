import os
import sys
import tempfile
from pathlib import Path

# Set configuration before importing the app. Never touch a developer's real DB.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
_test_dir = tempfile.TemporaryDirectory(prefix='crm-tests-')
os.environ['DATABASE_URL'] = f'sqlite:///{_test_dir.name}/test.db'
os.environ['GROQ_API_KEY'] = ''

import pytest
from fastapi.testclient import TestClient
from app.database import Base, engine
from app.main import app


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def hcp(client):
    response = client.post('/hcp', json={
        'name': 'Dr Demo', 'speciality': 'Fictional specialty',
        'hospital': 'Example Hospital', 'location': 'Demo City',
        'email': 'demo@example.com', 'phone': '0000000000',
    })
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def payload(hcp):
    return {'hcp_id': hcp['id'], 'interaction_date': '2026-10-01',
            'summary': 'Discussed a fictional product demo.',
            'products_discussed': 'Example Product', 'follow_up_date': '2026-10-05'}
