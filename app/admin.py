from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash
from app import app, db
from app.models import User, Role, Location
from flask import redirect, url_for
from flask_admin.form.upload import FileUploadField
from flask_login import current_user
from flask_admin.menu import MenuLink


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id in [2, 3]

class UserAdmin(ModelView):
    column_list = ['id', 'name', 'email', 'role.name']
    column_searchable_list = ['name', 'email', 'role.name']
    form_extra_fields = {'password': PasswordField('Password', validators=[DataRequired()])}
    form_columns = ['name', 'email', 'password', 'role']

    def on_model_change(self, form, model, is_created):
        raw_password = form.password.data
        hashed_password = generate_password_hash(raw_password)
        model.password = hashed_password
        form.password.data = None
        
    def create_model(self, form):
        try:
            name = form.name.data
            email = form.email.data
            password = form.password.data
            selected_role_id = form.role.data.id

            selected_role = Role.query.get(selected_role_id)

            if selected_role:
                new_user = User(name=name, email=email, password=password, role=selected_role)
                db.session.add(new_user)
                db.session.commit()
            else:
                flash('Role not found', 'error')

        except Exception as e:
            flash(f'Error creating user: {e}', 'error')

        return redirect(url_for('admin.index'))
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id ==3
    
        
class RoleAdmin(ModelView):
    column_list = ['id', 'name']

    def on_model_change(self, form, model, is_created):
        if 'password' in form:
            raw_password = form.password.data
            hashed_password = generate_password_hash(raw_password)
            model.password = hashed_password
            form.password.data = None

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id ==3

class LocationAdmin(ModelView):
    column_list = ['id', 'name', 'image', 'location', 'rental_price', 'description']
    form_extra_fields = {
        'image': FileUploadField('Image', base_path='app/static/images/', relative_path='locations/'),
    }
    form_columns = ['name', 'location', 'rental_price', 'description', 'image']
    
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id in [2, 3]

class BackToSiteMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id in [2, 3]

    def get_url(self):
        return url_for('index')

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3', index_view=MyAdminIndexView())

admin.add_view(UserAdmin(User, db.session))
admin.add_view(RoleAdmin(Role, db.session))
admin.add_view(LocationAdmin(Location, db.session))
admin.add_link(BackToSiteMenuLink(name='Back to Site'))