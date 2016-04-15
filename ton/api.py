from flask.ext.restful import Resource

from .application import app
from .models import LastUpdate, Location


class GetDataVersion(Resource):

    def get(self):
        dt = app.db.session.query(LastUpdate).first().last_update

        return int(dt.strftime("%Y%m%d%H%M%S")), 200


class GetLocationsResource(Resource):

    def get(self):
        locations = app.db.session.query(Location).all()

        locations_json = []
        for location in locations:
            loc = {
                "name": location.name,
            }

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

            if location.description is not None:
                loc["description"] = str(location.description)

            if location.address_line1 is not None:
                loc["address_line1"] = str(location.address_line1)

            if location.address_line2 is not None:
                loc["address_line2"] = str(location.address_line2)

            if location.address_line3 is not None:
                loc["address_line3"] = str(location.address_line3)

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
            "locations": locations_json
        }, 200)


def api_initialize():
    app.api.add_resource(GetDataVersion, '/api/getdataversion')
    app.api.add_resource(GetLocationsResource, '/api/getlocations')
