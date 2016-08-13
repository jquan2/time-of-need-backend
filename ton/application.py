from flask import Flask, abort, flash, redirect, render_template, request, url_for  # noqa
from flask.ext import restful
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib import sqla
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from flask_security.utils import encrypt_password
from wtforms.fields import PasswordField


from .models import Location, Role, User, db

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
app.db = db

# Setup api
app.api = restful.Api(app)
from .api import api_initialize  # noqa
api_initialize()


@app.route('/')
def index():
    return render_template('index.html')

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(app.db, User, Role)
security = Security(app, user_datastore)


class PasswordNotGivenError(ValueError):
    pass


class PasswordCompareError(ValueError):
    pass


class BorkCurrentUserError(ValueError):
    pass


# Create customized model view classes
class SecureView(sqla.ModelView):
    def is_accessible(self):
        """Deny access if current_user isn't a logged-in admin"""
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('Administrator'))

    def _handle_view(self, name, **kwargs):
        """Redirect users when a view is not accessible"""
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class StandardFilteredView(sqla.ModelView):
    def is_accessible(self):
        """Deny access if current_user isn't a logged-in admin"""
        return (current_user.is_active and
                current_user.is_authenticated and (
                    current_user.has_role('Administrator') or
                    current_user.has_role('Standard')))

    def _handle_view(self, name, **kwargs):
        """Redirect users when a view is not accessible"""
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

        self.can_create = self.can_delete = current_user.has_role('Administrator')  # noqa

    # Given a location id, are we allowed to edit it?
    def is_owned(self, id):
        if current_user.has_role('Administrator'):
            return True
        allowed_locations = [location.id for location in current_user.locations]
        return int(id) in allowed_locations

    # Overrides to check model ownership
    def on_model_change(self, form, model, is_created):
        if not self.is_owned(model.id):
            abort(403)

    def on_form_prefill(self, form, id):
        if not self.is_owned(id):
            abort(403)

    def on_model_delete(self, model):
        if not self.is_owned(model.id):
            abort(403)

    # Query Overrides to limit Standard Users to Locations they Own

    def get_query(self):
        allowed_locations = [location.id for location in current_user.locations]
        if current_user.has_role('Administrator'):
            return self.session.query(self.model)
        elif current_user.has_role('Standard'):
            return self.session.query(self.model).filter(
                self.model.id.in_(allowed_locations))

    def get_count_query(self):
        allowed_locations = [location.id for location in current_user.locations]
        if current_user.has_role('Administrator'):
            return super(StandardFilteredView, self).get_count_query()
        elif current_user.has_role('Standard'):
            return super(StandardFilteredView, self).get_count_query().filter(
                self.model.id.in_(allowed_locations))


class LocationModelView(StandardFilteredView):
    _list_columns = ["name", "services", "city", "state"]
    _cols = [
        ("name", "e.g. Food Bank of Alaska"),
        ("services", "Click for drop-down choices. May select multiple "
            "services. Type to filter."),
        ("description", ""),
        ("address_line1", "e.g. 123 Main St."),
        ("address_line2", "e.g. Ste. 200"),
        ("address_line3", "e.g. Fairbanks, AK 99775"),
        ("phone", "e.g. xxx-xxx-xxxx"),
        ("contact_email", "e.g. example@email.com"),
        ("website", "e.g. wehelppeople.org or www.wehelppeople.org"),
        ("opening_time", "Useful for locations with regular hours."),
        ("closing_time", "Useful for locations with regular hours."),
        ("days_of_week", "Useful for locations with regular hours."),
        ("city", "Useful for sorting locations.  Not sent to mobile devices."),
        ("state", "Useful for sorting locations.  Not sent to mobile devices."),
    ]
    can_view_details = True
    column_details_list = [name for name, _ in _cols]
    column_default_sort = "name"
    column_descriptions = dict(_cols)
    column_editable_list = ["city", "state"]
    column_list = _list_columns  # List view only
    form_columns = [name for name, _ in _cols if name not in ["city", "state"]]


class UserModelView(SecureView):
    _cols = [
        ("username", "Account Name"),
        ("roles", "User Permissions"),
        ("locations", "Locations Standard user is allowed to edit"),
        ("email", "Email Address (used for login)"),
        ("password", "User Password"),
        ("active", "Is login permitted?"),
    ]
    column_default_sort = "username"
    column_descriptions = dict(_cols)

    # Sub in a non-db-backed field for passwords
    column_descriptions["new_password"] = "Enter new password here"
    column_descriptions["confirm_password"] = "Confirm new password"
    column_exclude_list = form_excluded_columns = ['password', ]

    def scaffold_form(self):
        """Add new_password field to form"""
        form_class = super(UserModelView, self).scaffold_form()
        form_class.new_password = PasswordField('New Password')
        form_class.confirm_password = PasswordField('Confirm Password')
        return form_class

    def on_model_change(self, form, model, is_created):
        """Use new_password field.  Block self-deactivation."""
        # This problem already nailed a user.
        model.username = model.username.strip()
        model.email = model.email.strip()

        if is_created and not model.new_password:
            raise PasswordNotGivenError("You must give new users a password.")

        if model == current_user and not model.active:
            raise BorkCurrentUserError("You may not deactivate your own account.")  # noqa
        if model.new_password:
            if model.new_password == model.confirm_password:
                model.password = encrypt_password(model.new_password)
            else:
                raise PasswordCompareError("Passwords do not match.")

    def on_model_delete(self, model):
        """Block self-deletion"""
        if model == current_user:
            raise BorkCurrentUserError("You may not delete your own account.")

    def handle_view_exception(self, exc):
        validation_exceptions = [
            PasswordNotGivenError,
            PasswordCompareError,
            BorkCurrentUserError,
        ]
        for e in validation_exceptions:
            if isinstance(exc, e):
                flash(str(exc), 'error')
                return True
        return super(UserModelView, self).handle_view_exception(exc)


# Setup Flask-Admin
admin = Admin(app, name='Time of Need Admin', template_mode='bootstrap3',
              base_template='my_master.html')
admin.add_view(LocationModelView(Location, db.session, name="Locations"))
admin.add_view(UserModelView(User, db.session, name="Users"))


# Define a context processor for merging flask-admin's template context into
# the flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )
