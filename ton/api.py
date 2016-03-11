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

            if location.zip_codes != None:
                zipcodes_json = []
                for zip in location.zip_codes:
                    zipcodes_json.append(str(zip))

                loc["zipcodes"] = zipcodes_json

            if location.services != None:
                services_json = []
                for service in location.services:
                    services_json.append(str(service))

                loc["services"] = services_json

            if location.days_of_week != None:
                days_of_week_json = []
                for day in location.days_of_week:
                    days_of_week_json.append(str(day))

                loc["days"] = days_of_week_json

            if location.address != None:
                loc["address"] = str(location.address)

            if location.phone != None:
                loc["phone"] = str(location.phone)

            if location.contact_email != None:
                loc["contact_email"] = str(location.contact_email)

            if location.website != None:
                loc["website"] = str(location.website)

            if location.opening_time != None:
                loc["opening_time"] = str(location.opening_time)

            if location.closing_time != None:
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
