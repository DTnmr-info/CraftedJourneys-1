import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Set up database base class
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# Create the app
app = Flask(__name__)

# Configure the app
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql://CRaft_owner:npg_Sa6Dm9nYyXlf@ep-late-forest-a16y2ixe-pooler.ap-southeast-1.aws.neon.tech/CRaft?sslmode=require")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions with the app
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Import models and create tables
with app.app_context():
    from models import User, Package, Location, Inquiry, Image
    db.create_all()

# Register blueprints
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# Setup login manager loader
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
