class config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/todo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'