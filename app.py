import os
import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

# --- Logging Setup ---
logging.basicConfig(level=logging.DEBUG)

# --- Database Setup ---
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# --- Login Manager Setup ---
login_manager = LoginManager()

# --- Create the Flask Application ---
app = Flask(__name__)

# --- Application Configuration ---
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "postgresql://CRaft_owner:npg_Sa6Dm9nYyXlf@ep-late-forest-a16y2ixe-pooler.ap-southeast-1.aws.neon.tech/CRaft?sslmode=require",
)
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- Initialize Extensions ---
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# --- Register Blueprints ---
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from payment_routes import payment
from routes.admin_routes import admin_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(payment, url_prefix='/payment')

# --- Error Handlers ---
@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

# --- Login Manager User Loader ---
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# --- Database Table Creation (Run within application context) ---
with app.app_context():
    from models import User, Package, Location, Inquiry, Image, Payment
    db.create_all()

if __name__ == '__main__':
    # Consider using a proper WSGI server like Gunicorn or uWSGI for production
    app.run(debug=True)