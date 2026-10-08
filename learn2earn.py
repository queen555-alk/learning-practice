
resources = [
  {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
  {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
  {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3}
]

def list_resources():
    for resource in resources:
        print(resource["id"],resource["total"],resource["available"],resource["name"], resource["category"])

list_resources()