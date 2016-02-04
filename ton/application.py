from flask import Flask, abort, redirect, url_for, request, render_template
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import User, Role, Location, Service

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
app.db = db

# Flask views
@app.route('/')
def index():
    return render_template('index.html')

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(app.db, User, Role)
security = Security(app, user_datastore)


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('Administrator'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


# Setup Flask-Admin
admin = Admin(app, name='Time of Need Admin', template_mode='bootstrap3')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Location, db.session))
admin.add_view(MyModelView(Service, db.session))


# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )