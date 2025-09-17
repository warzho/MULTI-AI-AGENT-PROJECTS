import requests
import json

API_URL = "http://127.0.0.1:9999"


def test_health():
    try:
        response = requests.get(f"{API_URL}/")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")


def test_chat():
    payload = {
        "model_name": "llama-3.3-70b-versatile",  # Use one of your allowed models
        "system_prompt": "You are a helpful assistant",
        "messages": ["Hello"],
        "allow_search": False
    }

    try:
        response = requests.post(f"{API_URL}/chat", json=payload)
        print(f"Chat test: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Chat test failed: {e}")


if __name__ == "__main__":
    print("Testing backend...")
    test_health()
    test_chat()
