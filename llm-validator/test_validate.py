import requests
import json

def test_validate():
    url = "http://localhost:8000/validate"
    
    # Test case 1: Simple string response
    data1 = {
        "prompt": "What is 2+2?",
        "response": {"answer": "4"},
        "expected_schema": {
            "type": "object",
            "properties": {
                "answer": {"type": "string"}
            }
        }
    }
    
    try:
        print("\nTest 1: Simple string response")
        response1 = requests.post(url, json=data1)
        print(f"Status: {response1.status_code}")
        if response1.status_code == 200:
            print(f"Response: {response1.json()}")
        else:
            print(f"Error: {response1.text}")
    except Exception as e:
        print(f"Error in test 1: {str(e)}")
    
    # Test case 2: JSON object response
    data2 = {
        "prompt": "Generate a user profile",
        "response": {
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com"
        },
        "expected_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"},
                "email": {"type": "string"}
            },
            "required": ["name", "age", "email"]
        }
    }
    
    try:
        print("\nTest 2: JSON object response")
        response2 = requests.post(url, json=data2)
        print(f"Status: {response2.status_code}")
        if response2.status_code == 200:
            print(f"Response: {response2.json()}")
        else:
            print(f"Error: {response2.text}")
    except Exception as e:
        print(f"Error in test 2: {str(e)}")

if __name__ == "__main__":
    test_validate() 