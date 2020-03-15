class config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'fan'


def get_db(db_info):
    eng = db_info.get('eng') or 'sqlite'
    diver = db_info.get('diver') or ''
    user = db_info.get('user') or ''
    password = db_info.get('password') or ''
    host = db_info.get('host') or ''
    port = db_info.get('port') or ''
    db = db_info.get('db') or 'test.db'
    return '{}{}://{}{}{}{}/{}'.format(eng, diver, user, password, host, port, db)


class development(config):
    DEBUG = True
    db_info = {
        'eng': 'sqlite',
        'diver': '',
        'user': '',
        'password': '',
        'host': '',
        'port': '',
        'db': ''
    }
    SQLALCHEMY_DATABASE_URI = get_db(db_info)


class TestConfig(config):
    db_info = {
        'eng': 'sqlite',
        'diver': '',
        'user': '',
        'password': '',
        'host': '',
        'port': '',
        'db': ''
    }
    SQLALCHEMY_DATABASE_URI = get_db(db_info)


envs = {
    'development': development,
    'testing': TestConfig
}
