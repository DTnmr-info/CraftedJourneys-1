"""
Verify admin user credentials in the database
"""
import os
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def verify_admin():
    with app.app_context():
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@craftedjourneys.com').first()
        
        if admin:
            print(f"Admin user found: {admin.username}")
            print(f"Email: {admin.email}")
            print(f"Is admin: {admin.is_admin}")
            print(f"Password hash length: {len(admin.password_hash)}")
            print(f"Created at: {admin.created_at}")
            
            # Test default password
            test_password = "Admin@123"
            password_check = admin.check_password(test_password)
            print(f"Default password check: {password_check}")
            
            if not password_check:
                response = input("Do you want to reset the admin password? (y/n): ")
                if response.lower() == 'y':
                    admin.set_password(test_password)
                    db.session.commit()
                    print("Admin password has been reset to the default.")
        else:
            print("Admin user not found. Creating a new admin user...")
            create_admin()

def create_admin():
    with app.app_context():
        admin = User(
            username="admin",
            email="admin@craftedjourneys.com", 
            is_admin=True
        )
        admin.set_password("Admin@123")
        
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")

if __name__ == "__main__":
    verify_admin()