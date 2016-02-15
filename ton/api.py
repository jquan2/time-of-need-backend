from flask.ext.restful import Resource

from sqlalchemy import func

from .application import app
from .models import User


class TestResource(Resource):
    def get(self):
        return ({
            'message': 'ok',
            'user_count': app.db.session.query(func.count(User.id)).scalar()
        }, 200)

app.api.add_resource(TestResource, '/api/test')
