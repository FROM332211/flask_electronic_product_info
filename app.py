import os

from APP import creat_app
from flask_script import Manager

env = os.environ.get('FLASK_ENV', 'development')
app = creat_app(env)
manager = Manager(app)

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()