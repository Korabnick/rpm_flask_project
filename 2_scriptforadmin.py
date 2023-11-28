from app import app, db
from app.models import User, Role

with app.app_context():
    role_admin = Role.query.filter_by(name='Администратор').first()

    if role_admin is None:
        role_admin = Role(name='Администратор')
        db.session.add(role_admin)
        db.session.commit()

    new_user = User(name="admin", email="admin@gmail.com")
    new_user.role = role_admin
    new_user.password = "admin"  # Пароль будет автоматически хешироваться

    try:
        db.session.add(new_user)
        db.session.commit()
        print("User created successfully!")
    except Exception as e:
        print(f"Failed to create user: {e}")



# from app import db, app
# from models import User
# from werkzeug.security import generate_password_hash

# new_user = User(name="admin", email="admin@gmail.com", password=generate_password_hash("admin"), role=1)
# with app.app_context():
#     db.session.add(new_user)
#     db.session.commit()