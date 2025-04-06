import requests
import json

# URL for the placement endpoint
url = "http://localhost:8000/api/placement"

# Sample test data for items and containers
test_data = {
    "items": [
        {
            "itemId": "item001",
            "name": "Test Item 1",
            "width": 10,
            "depth": 10,
            "height": 5,
            "priority": 1,
            "expiryDate": "2026-04-06",
            "usageLimit": "5",
            "preferredZone": "Storage"
        },
        {
            "itemId": "item002",
            "name": "Test Item 2",
            "width": 15,
            "depth": 8,
            "height": 12,
            "priority": 2,
            "expiryDate": "2026-05-20",
            "usageLimit": "10",
            "preferredZone": "Science"
        }
    ],
    "containers": [
        {
            "containerId": "container001",
            "zone": "Storage",
            "width": 30,
            "depth": 30,
            "height": 30
        },
        {
            "containerId": "container002",
            "zone": "Science",
            "width": 25,
            "depth": 25,
            "height": 25
        }
    ]
}

def test_placement_endpoint():
    """Test the /api/placement endpoint"""
    print("Testing /api/placement endpoint...")
    
    # Make the POST request
    response = requests.post(url, json=test_data)
    
    # Check if request was successful
    if response.status_code == 200:
        print(f"Success! Status code: {response.status_code}")
        
        # Parse the response JSON
        result = response.json()
        
        # Pretty print the response
        print("\nResponse:")
        print(json.dumps(result, indent=2))
        
        # Validate the response structure
        if result.get("success"):
            print("\nValidation:")
            print(f"- Success: {result.get('success')}")
            print(f"- Placements count: {len(result.get('placements', []))}")
            print(f"- Rearrangements count: {len(result.get('rearrangements', []))}")
        else:
            print("\nThe placement calculation was not successful.")
    else:
        print(f"Error! Status code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    test_placement_endpoint()