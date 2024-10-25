from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from auth import auth as auth_blueprint # Import the auth blueprint
from stock import bp as stock_blueprint  # Import the stock blueprint
from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object('Config')

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# User loader
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

app.register_blueprint(auth_blueprint, url_prefix='/auth')  # Handles user authentication
app.register_blueprint(stock_blueprint, url_prefix='/stock')  # Handles stock routes

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
