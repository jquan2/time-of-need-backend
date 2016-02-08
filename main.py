from flask.ext.script import Manager, Server

from ton.models import User, Role

print('Hello World')

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

    app.db.drop_all()
    app.db.create_all()
    admin_role = Role(name='Administrator')
    app.db.session.add(admin_role)
    admin = User(username='admin', email='admin@example.com', password='supersecret', roles=[admin_role], active=True)
    app.db.session.add(admin)
    app.db.session.commit()

manager.add_command('runserver', server)

if __name__ == '__main__':
    manager.run()

