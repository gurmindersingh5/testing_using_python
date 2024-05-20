import pytest
from src.app import db, app
import json
from src.app.models import User
import json


# Another better way this fixture can be handled is by storing it in conftest.py file \
# and passing it (client in this case) to test_funtions as an argument. For example:
# conftest.py has fixture function client and in the tests.py a func will be like this:
# def test_func(client):
#     code
@pytest.fixture(scope='session') # session to cache the value and avoid multiple conn to db
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client  
        db.drop_all()


def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Go to : /api/users/all or /api/users/add or /api/users/<int:user_id>' in rv.data


def test_get_existing_user(client):
    user = User(name="John Doe", email="john.doe@example.com")
    db.session.add(user)
    db.session.commit()
    rv = client.get(f'/api/users/{user.id}')
    assert rv.status_code == 200
    assert b'John Doe' in rv.data


def test_get_non_existing_user(client):
    rv = client.get('/api/users/9999')
    assert rv.status_code == 404
    assert b'error' in rv.data
    assert b'user not found' in rv.data


def test_get_all_users(client):
    user1 = User(name="John Doe", email="john.doe@example.com")
    user2 = User(name="Jane Doe", email="jane.doe@example.com")
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    rv = client.get('/api/users/all')
    assert rv.status_code == 200
    assert b'John Doe' in rv.data
    assert b'Jane Doe' in rv.data


@pytest.mark.parametrize("user_data, expected_status, expected_response", [
    ({"name": "John Doe", "email": "john.doe@example.com"}, 200, b'successfully created user'),
    ({"name": "Jane Smith", "email": "jane.smith@example.com"}, 200, b'successfully created user'),
    ({"name": "Alice Johnson", "email": "alice.johnson@example.com"}, 200, b'successfully created user')
])
def test_add_user_with_valid_data(client, user_data, expected_status, expected_response):
    rv = client.post('/api/users/add', 
                     data=json.dumps(user_data), 
                     content_type='application/json')
    assert rv.status_code == expected_status
    assert expected_response in rv.data


def test_add_user_with_missing_data(client):
    rv = client.post('/api/users/add', 
                     data=json.dumps({"name": "John Doe"}), 
                     content_type='application/json')
    assert rv.status_code == 400
    assert b'error' in rv.data
    assert b'Name or Email missing' in rv.data

@pytest.mark.skip(reason='validation not done yet')
def test_add_user_with_invalid_data(client):
    rv = client.post('/api/users/add', 
                     data=json.dumps({"name": "", "email": "john.doe@example.com"}), 
                     content_type='application/json')
    assert rv.status_code == 400
    assert b'error' in rv.data


@pytest.mark.xfail
def test_add_user_with_no_json_header(client):
    rv = client.post('/api/users/add', 
                     data=json.dumps({"name": "John Doe", "email": "john.doe@example.com"}))
    assert rv.status_code == 200 # originally 415 but to perform xfail, intentionally failing test
    assert b'Success' in rv.data # originally 'error' instead of success but to xfail changed it
    # assert b'JSON type header missing or incorrect' in rv.data # commeted out to perform xfail


# def test_invalid_scenario():
#     with pytest.raises(ValueError, match="Invalid value for a parameter"):
#         func('something', 'x')
