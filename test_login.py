"""
Test the login functionality
"""
import os
from app import app, db
from models import User
from flask_login import login_user, current_user
from flask import session

def test_login():
    with app.app_context():
        with app.test_request_context():
            print("Testing admin login...")
            
            # Find the admin user
            admin = User.query.filter_by(email='admin@craftedjourneys.com').first()
            
            if not admin:
                print("Admin user not found!")
                return
            
            # Test password verification
            password = "Admin@123"
            if admin.check_password(password):
                print("Password verification successful.")
            else:
                print("Password verification failed!")
                return
            
            # Attempt to log in the admin user
            login_result = login_user(admin)
            
            if login_result:
                print("Login successful!")
                print(f"Current user: {current_user.username}")
                print(f"Is authenticated: {current_user.is_authenticated}")
                print(f"Is admin: {current_user.is_admin}")
                
                # Print the session to help debug login issues
                print("\nSession data:", dict(session))
            else:
                print("Login failed!")

if __name__ == "__main__":
    test_login()