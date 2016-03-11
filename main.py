import os
from subprocess import call

from flask.ext.script import Manager, Server

from ton import models
from ton.application import app

manager = Manager(app)
server = Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port='8000'
)


@manager.command
def initialize_db():
    # Flush the database
    app.db.drop_all()
    app.db.create_all()

    # Add roles
    admin_role = models.Role(name='Administrator')
    app.db.session.add(admin_role)
    admin = models.User(
        username='admin',
        email='admin@example.com',
        password='supersecret',
        roles=[admin_role],
        active=True)
    app.db.session.add(admin)

    # Cities
    fbx = models.City(name="Fairbanks")
    app.db.session.add(fbx)

    # Zip codes
    for z in ["99701", "99706", "99707", "99708", "99709", "99710", "99711",
              "99712", "99775", "99790"]:
        fbx.zip_codes.append(models.Zipcode(zip=z))

    # Days of week
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                "Saturday", "Sunday"]:
        app.db.session.add(models.DayOfWeek(day=day))

    # Save
    app.db.session.commit()

manager.add_command('runserver', server)


@manager.command
def generate_erd():
    """
    Generate UML that represents an ERD

    Command wrapper for sadisplay. Must have graphviz installed.
    See https://bitbucket.org/estin/sadisplay/wiki/Home
    """
    import sadisplay
    from ton import models

    desc = sadisplay.describe([getattr(models, attr) for attr in dir(models)])
    with open('schema.dot', 'w') as f:
        f.write(sadisplay.dot(desc))
    ret = call("dot -Tpng schema.dot > schema.png", shell=True)
    if ret == 0:
        os.remove("schema.dot")


if __name__ == '__main__':
    manager.run()
