from flask import request, render_template, redirect, url_for, flash, session, jsonify, json
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, mail, login_manager
from app.forms import RegistrationForm, LoginForm
from app.models import User, Role, Location, Favorite
from time import sleep
from flask_mail import Message
from validate_email_address import validate_email

def location_in_favorites(location_id):
    user_favorites = current_user.favorites.all()
    return any(fav.location_id == location_id for fav in user_favorites)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            login_user(user)
            session['logged_in_message'] = 'Logged in successfully!'
            return redirect('/profile')
        else:
            flash('Invalid email or password.', 'danger')
            return redirect('/login')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        role_user = Role.query.filter_by(name='Пользователь').first()

        if role_user is None:
            role_user = Role(name='Пользователь')
            db.session.add(role_user)
            db.session.commit()
        
        if not validate_email(email):
            flash('Некорректный формат почты.', 'danger')
            return redirect('/register')
        
        if password != confirm_password:
            flash('Пароли не совпадают.', 'danger')
            return redirect('/register')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Пользователь с такой почтой уже зарегистрирован.', 'danger')
            return redirect('/register')
        
        new_user = User(name=name, email=email, password=password)
        new_user.role = role_user
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect('/login')
        except Exception as e:
            print(e)
            flash('Registration failed.', 'danger')
            return redirect('/register')
    return render_template('register.html', form=form)


@app.route('/profile')
@login_required
def profile():
    message = session.pop('logged_in_message', None)
    return render_template('profile.html', user=current_user, message=message)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/send_email', methods=['POST'])
@login_required
def send_email():
    if request.method == 'POST':
        subject = request.form.get("subject")
        message = request.form.get("message")
        recipient = app.config['MAIL_DEFAULT_SENDER']

        if not subject or not message:
            flash('Пожалуйста, заполните все поля для отправки сообщения', 'error')
            return redirect('/contact')

        # Получаем сохраненные данные о выбранных локациях из sessionStorage
        selected_locations = json.loads(session.get('selectedLocations', '[]'))

        try:
            msg = Message(subject, recipients=[recipient])
            # Добавляем информацию о локациях в тело письма в формате JSON
            msg.body = f"Сообщение от клиента: {message}\n\nИзбранные локации:\n{selected_locations}"
            mail.send(msg)
            flash('Сообщение успешно отправлено!', 'success')
            
            # Очищаем sessionStorage после отправки формы
            session.pop('selectedLocations', None)
        except Exception as e:
            flash(f'Ошибка при отправке сообщения: {e}', 'error')

    return redirect('/contact')

@app.route('/get_favorite_locations', methods=['GET'])
@login_required  # Это, чтобы только авторизованные пользователи могли получить избранные локации
def get_favorite_locations():
    if current_user.is_authenticated:
        user_favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        favorite_locations = [fav.location for fav in user_favorites]
        locations_data = [{'id': location.id, 'name': location.name} for location in favorite_locations]
        return jsonify({'favoriteLocations': locations_data})
    return jsonify({'message': 'Unauthorized'}), 401

# @app.route('/send_email', methods=['POST'])
# @login_required
# def send_email():
#     if request.method == 'POST':
#         subject = request.form.get("subject")
#         message = request.form.get("message")
#         recipient = app.config['MAIL_DEFAULT_SENDER']

#         if not subject or not message:
#             flash('Пожалуйста, заполните все поля для отправки сообщения', 'error')
#             return redirect('/contact')

#         try:
#             msg = Message(subject, recipients=[recipient])
#             msg.body = f"Сообщение от клиента: {message}"
#             mail.send(msg)
#             flash('Сообщение успешно отправлено!', 'success')
#         except Exception as e:
#             flash(f'Ошибка при отправке сообщения: {e}', 'error')

#     return redirect('/contact')


@app.route('/locations')
@login_required
def show_locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations, location_in_favorites=location_in_favorites)


@app.route('/location/<int:location_id>')
@login_required
def location_details(location_id):
    location = Location.query.get_or_404(location_id)
    return render_template('location_details.html', location=location)


@app.route('/add_to_favorites/<int:location_id>', methods=['POST'])
@login_required
def add_to_favorites(location_id):
    location = Location.query.get_or_404(location_id)
    if location:
        favorite = Favorite.query.filter_by(user_id=current_user.id, location_id=location_id).first()
        if not favorite:
            new_favorite = Favorite(user_id=current_user.id, location_id=location_id)
            db.session.add(new_favorite)
            db.session.commit()
            flash(f'{location.name} добавлено в избранное!', 'success')
        else:
            flash(f'{location.name} уже есть в избранном!', 'info')
    return redirect(url_for('show_locations'))

@app.route('/remove_from_favorites_locations/<int:location_id>', methods=['POST'])
@login_required
def remove_from_favorites_locations(location_id):
    favorite = Favorite.query.filter_by(user_id=current_user.id, location_id=location_id).first()
    if favorite:
        location = Location.query.get_or_404(location_id)
        location_name = location.name
        db.session.delete(favorite)
        db.session.commit()
        flash(f'{location_name} удалено из избранного!', 'success')
    return redirect(url_for('show_locations'))

@app.route('/remove_from_favorites_favorites/<int:location_id>', methods=['POST'])
@login_required
def remove_from_favorites_favorites(location_id):
    favorite = Favorite.query.filter_by(user_id=current_user.id, location_id=location_id).first()
    if favorite:
        location = Location.query.get_or_404(location_id)
        location_name = location.name
        db.session.delete(favorite)
        db.session.commit()
        flash(f'{location_name} удалено из избранного!', 'success')
    return redirect(url_for('favorites'))

@app.route('/favorites')
@login_required
def favorites():
    user_favorites = current_user.favorites.all()
    locations = [fav.location for fav in user_favorites]
    return render_template('favorites.html', favorites=user_favorites)

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('unauthorized.html')

@app.errorhandler(403)
def forbidden(error):
    return render_template('forbidden.html'), 403