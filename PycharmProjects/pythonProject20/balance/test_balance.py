import pytest
from balance.app import app
from balance.data import balance

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        # Сброс данных после тестов
        balance.clear()
        balance.extend([
            {"amount": 196872.42, "description": "Начисление заработной платы"},
            {"amount": -399.99, "description": "Покупка кофе в Дринкит"}
        ])

def test_get_balance(client):
    response = client.get('/balance')
    assert response.status_code == 200
    assert len(response.json['balance']) == 2

def test_add_balance(client):
    response = client.post('/balance', json={"amount": 196872.42, "description": "Начисление заработной платы"})
    assert response.status_code == 201
    assert len(balance) == 3
