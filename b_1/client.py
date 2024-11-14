import requests

BASE_URL = "http://localhost:8000/items/"

# Create Item
def create_item(name: str, description: str):
    payload = {
        "name": name,
        "description": description
    }
    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 200:
        print("Item created successfully:")
        print(response.json())
    else:
        print(f"Failed to create item: {response.status_code}")
        print(response.text)

# Get All Items
def get_items():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        print("Items retrieved successfully:")
        for item in response.json():
            print(item)
    else:
        print(f"Failed to retrieve items: {response.status_code}")
        print(response.text)

# Get Item by ID
def get_item(item_id: int):
    response = requests.get(f"{BASE_URL}{item_id}")
    if response.status_code == 200:
        print("Item retrieved successfully:")
        print(response.json())
    else:
        print(f"Failed to retrieve item: {response.status_code}")
        print(response.text)

# Update Item
def update_item(item_id: int, name: str = None, description: str = None):
    payload = {}
    if name:
        payload["name"] = name
    if description:
        payload["description"] = description
    response = requests.put(f"{BASE_URL}{item_id}", json=payload)
    if response.status_code == 200:
        print("Item updated successfully:")
        print(response.json())
    else:
        print(f"Failed to update item: {response.status_code}")
        print(response.text)

# Delete Item
def delete_item(item_id: int):
    response = requests.delete(f"{BASE_URL}{item_id}")
    if response.status_code == 200:
        print("Item deleted successfully.")
    else:
        print(f"Failed to delete item: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # Example usage
    create_item("Sample Item", "This is a sample item.")
    get_items()
    get_item(1)
    update_item(1, name="Updated Sample Item", description="This is an updated description.")
    delete_item(1)
    get_items()
