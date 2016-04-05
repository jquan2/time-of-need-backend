from flask import Flask, abort, redirect, render_template, request, url_for
from flask.ext import restful

from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib import sqla

from flask_security import SQLAlchemyUserDatastore, Security, current_user

from .models import City, Location, Role, Service, User, Zipcode, db

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


# Create customized model view class
class SecureView(sqla.ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('Administrator'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view
        is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class LocationModelView(SecureView):
    _list_columns = ["name", "services"]
    _form_columns = [
        "name",
        "address_line1",
        "address_line2",
        "address_line3",
        "phone",
        "contact_email",
        "website",
        "opening_time",
        "closing_time",
        "currency",
        "min_cost",
        "days_of_week",
        "services",
        "zip_codes",
    ]

    can_view_details = True
    column_list = _list_columns  # List view
    form_columns = _form_columns  # Form view


# Setup Flask-Admin
admin = Admin(app, name='Time of Need Admin', template_mode='bootstrap3',
              base_template='my_master.html')
admin.add_view(SecureView(Service, db.session, name="Services"))
admin.add_view(LocationModelView(Location, db.session, name="Locations"))
admin.add_view(SecureView(Zipcode, db.session, name="Zip codes"))
admin.add_view(SecureView(City, db.session, name="Cities"))


# Define a context processor for merging flask-admin's template context into
# the flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )
