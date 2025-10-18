#!/usr/bin/env python3

import requests
import json


def test_admin_login():
    """Test admin user login"""
    print("🧪 Testing admin user login...")

    # Wait a moment for services to start
    import time

    time.sleep(3)

    try:
        # Test admin login
        login_data = {"email": "admin@example.com", "password": "test"}

        response = requests.post(
            "http://localhost:8000/api/auth/login", json=login_data
        )

        if response.status_code == 200:
            data = response.json()
            user = data.get("user", {})
            print(f"✅ Admin login successful!")
            print(f"   User ID: {user.get('id')}")
            print(f"   Email: {user.get('email')}")
            print(f"   Name: {user.get('name')}")
            print(f"   Token: {data.get('access_token', '')[:20]}...")
            return True
        else:
            print(f"❌ Admin login failed: {response.status_code} - {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure containers are running.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    test_admin_login()
