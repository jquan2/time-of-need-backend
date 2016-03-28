from flask.ext.restful import Resource

from sqlalchemy import func

from .application import app
from .models import User, Location


class GetLocationsResource(Resource):

    def get(self):
        locations = app.db.session.query(Location).all()

        locations_json = []
        for location in locations:
            loc = {
                "name": location.name,
            }

            if location.zip_codes is not None:
                zipcodes_json = []
                for zip in location.zip_codes:
                    zipcodes_json.append(str(zip))

                if len(zipcodes_json) > 0:
                    loc["zipcodes"] = zipcodes_json

            if location.services is not None:
                services_json = []
                for service in location.services:
                    services_json.append(str(service))

                if len(services_json) > 0:
                    loc["services"] = services_json

            if location.days_of_week is not None:
                days_of_week_json = []
                for day in location.days_of_week:
                    days_of_week_json.append(str(day))

                if len(days_of_week_json) > 0:
                    loc["days"] = days_of_week_json

            if location.address is not None:
                loc["address"] = str(location.address)

            if location.phone is not None:
                loc["phone"] = str(location.phone)

            if location.contact_email is not None:
                loc["contact_email"] = str(location.contact_email)

            if location.website is not None:
                loc["website"] = str(location.website)

            if location.opening_time is not None:
                loc["opening_time"] = str(location.opening_time)

            if location.closing_time is not None:
                loc["closing_time"] = str(location.closing_time)

            locations_json.append(loc)

        return ({
            "locations" : locations_json
        }, 200)

class TestResource(Resource):
    def get(self):
        return ({
            'message': 'ok',
            'user_count': app.db.session.query(func.count(User.id)).scalar()
        }, 200)


def api_initialize():
    app.api.add_resource(TestResource, '/api/test')
    app.api.add_resource(GetLocationsResource, '/api/getlocations')
