from flask import Flask
from config import Config
from models import db
from controllers import main
from demo import demo
from dotenv import dotenv_values
import os

config = {
    **dotenv_values(".env"),  # load general variables
    **dotenv_values(".env.shared"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Initializes the app
db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database created at:", app.config['SQLALCHEMY_DATABASE_URI'])

app.register_blueprint(main)
app.register_blueprint(demo)

if __name__ == '__main__':
    app.run(debug=True)
