#!/usr/bin/env python3

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api"


def test_mugswap_api():
    print("🧪 Testing Mugswap API with new data format...")

    # Test user registration
    print("\n1. Registering test user...")
    register_data = {
        "email": "test@mugswap.com",
        "name": "Test User",
        "age": 25,
        "bio": "Testing the new format!",
        "password": "testpass",
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 200:
            data = response.json()
            token = data["access_token"]
            print(f"✅ User registered successfully!")

            # Test getting mugs
            print("\n2. Fetching mugs with new format...")
            headers = {"Authorization": f"Bearer {token}"}

            mugs_response = requests.get(f"{BASE_URL}/mugs", headers=headers)
            if mugs_response.status_code == 200:
                mugs = mugs_response.json()
                print(f"✅ Found {len(mugs)} mugs!")

                # Show first 3 mugs
                print("\n📝 Sample mugs with people's names:")
                for i, mug in enumerate(mugs[:3], 1):
                    print(f"\n{i}. {mug['name']}")
                    print(f"   Description: {mug['description']}")
                    print(f"   Image: {mug['image_url']}")
                    # Confirm no price/color/etc fields
                    removed_fields = [
                        field
                        for field in ["price", "color", "size", "material"]
                        if field in mug
                    ]
                    if removed_fields:
                        print(f"   ❌ Still has: {removed_fields}")
                    else:
                        print(f"   ✅ Clean format (no product details)")

                print(
                    f"\n🎉 Success! Mugswap now features people instead of product details!"
                )
                return True
            else:
                print(f"❌ Failed to get mugs: {mugs_response.text}")
        else:
            print(f"❌ Registration failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

    return False


if __name__ == "__main__":
    test_mugswap_api()
