"""
Test the session management
"""
import os
from app import app, db
from models import User

def test_session():
    """Test login and session with Flask test client."""
    with app.test_client() as client:
        print("Testing login with Flask test client...")
        
        # Check if login page is accessible
        response = client.get('/login')
        print(f"Login page status: {response.status_code}")
        
        # Try logging in with correct credentials
        login_data = {
            'email': 'admin@craftedjourneys.com',
            'password': 'Admin@123',
            'remember': False
        }
        
        # Need to get CSRF token first
        login_page = client.get('/login')
        html = login_page.data.decode()
        
        # Crude way to extract the CSRF token from the form
        csrf_token = None
        for line in html.split('\n'):
            if 'csrf_token' in line and 'value' in line:
                parts = line.split('value="')
                if len(parts) > 1:
                    csrf_token = parts[1].split('"')[0]
                    break
        
        if not csrf_token:
            print("Could not find CSRF token!")
            return
            
        print(f"Found CSRF token: {csrf_token[:10]}...")
        login_data['csrf_token'] = csrf_token
        
        # Now try to login
        login_response = client.post('/login', data=login_data, follow_redirects=True)
        print(f"Login response status: {login_response.status_code}")
        
        # Check if we're redirected to the dashboard (success) or back to login (failure)
        if '/admin' in login_response.request.path:
            print("SUCCESS: Redirected to admin dashboard!")
        else:
            print(f"FAILURE: Redirected to {login_response.request.path}")
            
        # Try to access the admin dashboard
        dashboard_response = client.get('/admin/')
        print(f"Dashboard access status: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            print("SUCCESS: Can access admin dashboard!")
        else:
            print(f"FAILURE: Cannot access admin dashboard. Status: {dashboard_response.status_code}")

if __name__ == "__main__":
    test_session()