import pytest
import sys
sys.path.append('../')
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app import app, db
from app.models import User, Role, Location, Favorite
from werkzeug.datastructures import MultiDict
from app.forms import RegistrationForm, LoginForm

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fladmin:test@localhost:38764/flask_db'

    with app.app_context():
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        connection = engine.connect()
        trans = connection.begin()

        db.app = app
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()

        trans.rollback()
        connection.close()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200

def test_contact_page(client):
    response = client.get('/contact')
    assert response.status_code == 200

def test_favorites_page(client):
    response = client.get('/favorites')
    assert response.status_code == 200

def test_locations_page(client):
    response = client.get('/locations')
    assert response.status_code == 200

def test_location_page(client):
    response = client.get('/location/1')
    assert response.status_code == 200

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_profile_page(client):
    response = client.get('/profile')
    assert response.status_code == 200
    
def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200

def test_role_creation(client):
    with app.app_context():
        role = Role(name='Test Role')
        db.session.add(role)
        db.session.commit()

        queried_role = Role.query.filter_by(name='Test Role').first()
        assert queried_role is not None
        assert queried_role.name == 'Test Role'

def test_registration(client):
    with app.app_context():
        role_user = Role.query.filter_by(name='Пользователь').first()
        if role_user is None:
            role_user = Role(name='Пользователь')
            db.session.add(role_user)
            db.session.commit()

        form_data = MultiDict({
            'username': 'TestUser',
            'email': 'test@example.com',
            'password': 'test_password',
            'confirm_password': 'test_password'
        })

        with client as c:
            response = c.post('/register', data=form_data, follow_redirects=True)

            assert response.status_code == 200
            assert b'Registration successful! Please log in.' in response.data

            queried_user = User.query.filter_by(email='test@example.com').first()
            assert queried_user is not None
            assert queried_user.name == 'TestUser'

def test_login(client):
    with app.app_context():
        user = User(
            name='TestUser',
            email='test@example.com',
            password='test_password'
        )
        db.session.add(user)
        db.session.commit()

        form_data = MultiDict({
            'email': 'test@example.com',
            'password': 'test_password'
        })

        with client as c:
            response = c.post('/login', data=form_data, follow_redirects=True)

            assert response.status_code == 200
            assert b'Logged in successfully!' in response.data


def test_location_creation(client):
    with app.app_context():
        location = Location(
            name='Test Location',
            image='test_image.jpg',
            location='Test City',
            rental_price=100.0,
            description='Test description'
        )

        db.session.add(location)
        db.session.commit()
        
        location = Location.query.filter_by(name='Test Location').first()
        assert location is not None
        assert location.name == 'Test Location'
        assert location.image == 'test_image.jpg'
        assert location.location == 'Test City'
        assert location.rental_price == 100.0
        assert location.description == 'Test description'


# def test_add_to_favorites(client):
#     with app.app_context():
#         # Создаем тестового пользователя
#         user = User(name='TestUser', email='test@example.com', password='test_password')
#         db.session.add(user)
#         db.session.commit()

#         # Создаем тестовое место
#         location = Location(name='TestLocation', image='test_image.jpg', location='Test', rental_price=50.0)
#         db.session.add(location)
#         db.session.commit()

#         with client.session_transaction() as sess:
#             # Логинимся как тестовый пользователь
#             sess['user_id'] = user.id

#             # Отправляем POST-запрос на добавление в избранное
#             response = client.post(f'/add_to_favorites/{location.id}', follow_redirects=True)
            
#             # Проверяем, что место успешно добавлено в избранное
#             assert response.status_code == 200
#             assert 'TestLocation добавлено в избранное!' in response.data.decode('utf-8')

#             # Проверяем, что место добавлено в избранное для текущего пользователя
#             queried_favorite = Favorite.query.filter_by(user_id=user.id, location_id=location.id).first()
#             assert queried_favorite is not None

# def test_remove_from_favorites(client):
#     with app.app_context():
#         # Создаем тестового пользователя
#         user = User(name='TestUser', email='test@example.com', password='test_password')
#         db.session.add(user)
#         db.session.commit()

#         # Создаем тестовое место
#         location = Location(name='TestLocation', image='test_image.jpg', location='Test', rental_price=50.0)
#         db.session.add(location)
#         db.session.commit()

#         # Добавляем место в избранное для тестового пользователя
#         favorite = Favorite(user_id=user.id, location_id=location.id)
#         db.session.add(favorite)
#         db.session.commit()

#         with client.session_transaction() as sess:
#             # Логинимся как тестовый пользователь
#             sess['user_id'] = user.id

#             # Отправляем POST-запрос на удаление из избранного
#             response = client.post(f'/remove_from_favorites_locations/{location.id}', follow_redirects=True)
            
#             # Проверяем, что место успешно удалено из избранного
#             assert response.status_code == 200
#             assert 'TestLocation удалено из избранного!' in response.data.decode('utf-8')

#             # Проверяем, что место удалено из избранного для текущего пользователя
#             queried_favorite = Favorite.query.filter_by(user_id=user.id, location_id=location.id).first()
#             assert queried_favorite is None