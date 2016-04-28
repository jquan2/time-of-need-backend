from flask import Flask, abort, redirect, render_template, request, url_for
from flask.ext import restful

from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib import sqla

from flask_security import SQLAlchemyUserDatastore, Security, current_user

from .models import Location, Role, User, db

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
app.db = db

# Setup api
app.api = restful.Api(app)
from .api import api_initialize
api_initialize()


@app.route('/')
def index():
    return render_template('index.html')

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(app.db, User, Role)
security = Security(app, user_datastore)


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


class LocationModelView(SecureView):
    _list_columns = ["name", "services", "city", "state"]
    _form_columns = [
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
    can_view_details = True  # Add a "View" option for records
    column_list = _list_columns  # List view
    column_default_sort = "name"
    form_columns = [name for name, _ in _form_columns]  # Form view
    column_descriptions = dict(_form_columns)  # Form view


# Setup Flask-Admin
admin = Admin(app, name='Time of Need Admin', template_mode='bootstrap3',
              base_template='my_master.html')
admin.add_view(LocationModelView(Location, db.session, name="Locations"))


# Define a context processor for merging flask-admin's template context into
# the flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )
