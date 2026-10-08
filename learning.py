# Learn2Earn equipment lending system

resources = [
  {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
  {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
  {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3}
]
fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
borrow_records = []  

def print_resources(items):
    if len(items) == 0:
        print("No resources found.")
        return
    for resource in items:
        print(resource["id"], resource["name"], resource["category"],
              "total:", resource["total"], "available:", resource["available"])

def list_resources():
    print_resources(resources)

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
    print("Added", name)

def borrow(fellow_id, resource_id, quantity):
    if fellow_id not in fellows:
        print("Error: fellow id not found")
        return
    resource = find_resource(resource_id)
    if resource is None:
        print("Error: resource id not found")
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

def return_item(fellow_id, resource_id, quantity):
    if fellow_id not in fellows:
        print("Error: fellow id not found")
        return
    resource = find_resource(resource_id)
    if resource is None:
        print("Error: resource id not found")
        return
    if quantity <= 0:
        print("Error: quantity must be more than zero")
        return
    on_loan = units_on_loan(fellow_id, resource_id)
    if quantity > on_loan:
        print("Error:", fellows[fellow_id], "only has", on_loan, resource["name"], "on loan")
        return

    resource["available"] = resource["available"] + quantity

    left_to_return = quantity
    for record in borrow_records:
        if left_to_return == 0:
            break
        if record["fellow_id"] == fellow_id and record["resource_id"] == resource_id:
            can_return = record["borrowed"] - record["returned"]
            if can_return > left_to_return:
                can_return = left_to_return
            record["returned"] = record["returned"] + can_return
            left_to_return = left_to_return - can_return
    print(fellows[fellow_id], "returned", quantity, resource["name"])

def search_by_name(text):
    found = []
    for resource in resources:
        if text.lower() in resource["name"].lower():
            found.append(resource)
    return found

def filter_by_category(category):
    found = []
    for resource in resources:
        if resource["category"].lower() == category.lower():
            found.append(resource)
    return found

def report():
    total_units = 0
    available_units = 0
    for resource in resources:
        total_units = total_units + resource["total"]
        available_units = available_units + resource["available"]
    borrowed_units = total_units - available_units

    print("Total units:", total_units)
    print("Available units:", available_units)
    print("Units currently borrowed:", borrowed_units)

    print("Resources with fewer than 3 available:")
    found_low = False
    for resource in resources:
        if resource["available"] < 3:
            print(" -", resource["name"], "(" + str(resource["available"]) + ")")
            found_low = True
    if not found_low:
        print(" none")

    most = 0
    for resource in resources:
        borrowed = resource["total"] - resource["available"]
        if borrowed > most:
            most = borrowed

    if most == 0:
        print("Most borrowed: nothing is on loan")
    else:
        print("Most borrowed (" + str(most) + " units):")
        for resource in resources:      # second loop so ties are all shown
            if resource["total"] - resource["available"] == most:
                print(" -", resource["name"])

def run_demo():
    print("1. F001 borrows 2 laptops")
    borrow("F001", "R001", 2)
    print("2. F002 borrows 3 keyboards")
    borrow("F002", "R002", 3)
    print("3. F001 returns 1 laptop")
    return_item("F001", "R001", 1)
    print("4. F003 requests 4 headsets")
    borrow("F003", "R003", 4)
    print("5. F002 tries to return 4 keyboards")
    return_item("F002", "R002", 4)
    print("6. Search for LAPtop")
    print_resources(search_by_name("LAPtop"))
    print("7. Report")
    report()

def ask_number(message):
    text = input(message).strip()
    if text.isdigit():
        return int(text)
    print("Error: please enter a whole number")
    return -1

def main():
    while True:
        print()
        print("1. List resources")
        print("2. Add resource")
        print("3. Borrow")
        print("4. Return")
        print("5. Search by name")
        print("6. Filter by category")
        print("7. Report")
        print("8. Run demonstration")
        print("9. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            list_resources()
        elif choice == "2":
            resource_id = input("ID: ").strip().upper()
            name = input("Name: ").strip()
            category = input("Category: ").strip()
            total = ask_number("Total units: ")
            if total > 0:
                add_resource(resource_id, name, category, total)
            else:
                print("Error: total must be more than zero")
        elif choice == "3":
            fellow_id = input("Fellow ID: ").strip().upper()
            resource_id = input("Resource ID: ").strip().upper()
            quantity = ask_number("Quantity: ")
            if quantity != -1:
                borrow(fellow_id, resource_id, quantity)
        elif choice == "4":
            fellow_id = input("Fellow ID: ").strip().upper()
            resource_id = input("Resource ID: ").strip().upper()
            quantity = ask_number("Quantity: ")
            if quantity != -1:
                return_item(fellow_id, resource_id, quantity)
        elif choice == "5":
            print_resources(search_by_name(input("Name: ").strip()))
        elif choice == "6":
            print_resources(filter_by_category(input("Category: ").strip()))
        elif choice == "7":
            report()
        elif choice == "8":
            run_demo()
        elif choice == "9":
            print("Goodbye.")
            break
        else:
            print("Invalid choice, please enter a number from 1 to 9.")
main()