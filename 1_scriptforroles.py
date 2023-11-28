from app import app, db
from app.models import Role

application = app

with application.app_context():
    role_user = Role.query.filter_by(name='Пользователь').first()
    if not role_user:
        role_user = Role(name='Пользователь')
        db.session.add(role_user)

    role_moderator = Role.query.filter_by(name='Модератор').first()
    if not role_moderator:
        role_moderator = Role(name='Модератор')
        db.session.add(role_moderator)
    
    role_moderator = Role.query.filter_by(name='Администратор').first()
    if not role_moderator:
        role_moderator = Role(name='Администратор')
        db.session.add(role_moderator)

    db.session.commit()