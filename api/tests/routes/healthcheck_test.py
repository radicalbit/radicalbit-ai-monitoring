from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app, raise_server_exceptions=False)


def test_healthcheck():
    response = client.get('/healthcheck')
    assert response.status_code == 200
    assert response.json() == {'status': 'alive'}
