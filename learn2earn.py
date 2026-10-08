
resources = [
  {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
  {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
  {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3}
]

fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
borrow_records = []

def list_resources():
    for resource in resources:
        print(resource["id"],resource["total"],resource["available"],resource["name"], resource["category"])

list_resources()

def find_resource(resource_id):
    for r in resources:
        if r["id"] == resource_id:
            return r
    return None

def add_resource(resource_id, name, category, total):
    if find_resource(resource_id) is not None:
        print("Error: that resource ID already exists.")
        return
    resources.append({"id": resource_id, "name": name, "category": category,
                      "total": total, "available": total})

add_resource("R004", "Mouse", "Accessories", 8)
add_resource("R001", "Another", "Test", 5)
list_resources()

def borrow(fellow_id, resource_id, quantity):
    if fellow_id not in fellows:
        print("Error: fellow id not found")
        return
    resource = find_resource(resource_id)
    if resource is None:
        print("Error: resources id not found")
        return
    
    if quantity <= 0:
        print("Error: quantity must be more than zero")
        return
    if quantity > resource["available"]:
        print("Error: only", resource["available"], resource["name"], "available")
        return

    resource["available"] = resource["available"] - quantity
    borrow_records.append({"fellow_id": fellow_id, "resource_id": resource_id,
                           "borrowed": quantity, "returned": 0})
    print(fellows[fellow_id], "borrowed", quantity, resource["name"])

def units_on_loan(fellow_id, resource_id):
    count = 0
    for record in borrow_records:
        if record["fellow_id"] == fellow_id and record["resource_id"] == resource_id:
            count = count + record["borrowed"] - record["returned"]
    return count

