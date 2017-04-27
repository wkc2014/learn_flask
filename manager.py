from flask_script import Manager
from app import create_app, db
from flask_migrate import MigrateCommand, Migrate
from app.models import User,Role

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)



@manager.command
def dev():
    from livereload import Server
    liver_server = Server(app.wsgi_app)
    liver_server.watch('**/*.*')
    liver_server.serve(open_url_delay=True)

@manager.command
def test():
    "Run the unittest testcase"
    import unittest
    tests = unittest.TestLoader().discover('testCase')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
