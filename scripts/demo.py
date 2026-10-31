"""Run an isolated, fictional API demo. No server, database service or AI key needed."""
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--record', action='store_true', help='Save verified demo steps to docs/demo-results.json')
args = parser.parse_args()
sys.path.insert(0, str(ROOT / 'backend'))
frames = []

with tempfile.TemporaryDirectory(prefix='hcp-crm-demo-') as demo_dir:
    os.environ['DATABASE_URL'] = f'sqlite:///{demo_dir}/demo.db'
    os.environ['GROQ_API_KEY'] = ''
    from fastapi.testclient import TestClient
    from app.main import app

    def show(title, method, route, response, expected):
        assert response.status_code == expected, (title, response.text)
        frame = {'title': title, 'request': f'{method} {route}',
                 'status': response.status_code, 'response': response.json()}
        frames.append(frame)
        print(f'\n{title}\n{method} {route} -> {response.status_code}')
        print(json.dumps(response.json(), indent=2))

    with TestClient(app) as client:
        show('1. Start without an AI key', 'GET', '/health', client.get('/health'), 200)
        hcp_response = client.post('/hcp', json={
            'name': 'Dr Demo', 'speciality': 'Fictional specialty',
            'hospital': 'Example Hospital', 'location': 'Demo City',
            'email': 'demo@example.com', 'phone': '0000000000',
        })
        show('2. Add a fictional HCP', 'POST', '/hcp', hcp_response, 200)
        payload = {'hcp_id': hcp_response.json()['id'], 'interaction_date': '2026-10-01',
                   'summary': 'Discussed an example product demonstration.', 'products_discussed': 'Example Product'}
        response = client.post('/interaction', json=payload)
        show('3. Log structured data without calling an LLM', 'POST', '/interaction', response, 200)
        record = response.json()
        show('4. Reject an unknown HCP', 'POST', '/interaction',
             client.post('/interaction', json={**payload, 'hcp_id': 999}), 404)
        show('5. Reject an invalid follow-up date', 'POST', '/interaction',
             client.post('/interaction', json={**payload, 'follow_up_date': '2026-09-01'}), 422)
        response = client.get(f"/interaction/{payload['hcp_id']}")
        assert response.json() == [record], 'Rejected writes must not change stored history'
        show('6. Verify failed requests did not add records', 'GET', f"/interaction/{payload['hcp_id']}", response, 200)
        show('7. Explain optional AI availability honestly', 'POST', '/chat/',
             client.post('/chat/', json={'message': 'List HCPs'}), 503)

if args.record:
    target = ROOT / 'docs' / 'demo-results.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(frames, indent=2) + '\n')
print('\nDemo passed. Temporary database removed; no external AI calls made.')
