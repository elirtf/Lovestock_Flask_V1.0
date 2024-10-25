import pytest
from app import app, db
from models import User


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        db.drop_all()


def test_register(client):
    response = client.post('/auth/register', data={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 302  # Redirect after successful registration

def test_login_logout(client):
    client.post('/auth/register', data={'username': 'testuser', 'password': 'testpass'})
    response = client.post('/auth/login', data={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 302  # Redirect after successful login

    response = client.get('/auth/logout')
    assert response.status_code == 302  # Redirect after logout

def test_stock_search(client):
    client.post('/auth/register', data={'username': 'testuser', 'password': 'testpass'})
    client.post('/auth/login', data={'username': 'testuser', 'password': 'testpass'})

    response = client.post('/stock/stock', data={'symbol': 'AAPL', 'time_period': '1d'})
    assert response.status_code == 200
    assert b'AAPL Stock' in response.data

def test_add_to_watchlist(client):
    client.post('/auth/register', data={'username': 'testuser', 'password': 'testpass'})
    client.post('/auth/login', data={'username': 'testuser', 'password': 'testpass'})

    response = client.post('/stock/add_to_watchlist', data={'symbol': 'AAPL'})
    assert response.status_code == 302  # Redirect after adding to watchlist
