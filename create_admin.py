import os
import sys
from app import app, db
from models import User

def create_admin_user(username, email, password):
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            print(f"User with username '{username}' or email '{email}' already exists!")
            return
        
        # Create new admin user
        admin = User(username=username, email=email, is_admin=True)
        admin.set_password(password)
        
        # Add to database
        db.session.add(admin)
        db.session.commit()
        
        print(f"Admin user '{username}' created successfully!")

if __name__ == "__main__":
    # Default credentials if not provided
    default_username = "admin"
    default_email = "admin@craftedjourneys.com"
    default_password = "Admin@123"
    
    # Use command line arguments if provided
    username = sys.argv[1] if len(sys.argv) > 1 else default_username
    email = sys.argv[2] if len(sys.argv) > 2 else default_email
    password = sys.argv[3] if len(sys.argv) > 3 else default_password
    
    create_admin_user(username, email, password)