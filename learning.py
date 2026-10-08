import json

resources = [
    {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
    {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
    {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3},
]
fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
borrow_records = []  # each record: fellow_id, resource_id, borrowed, returned


def find_resource(resource_id):
    for r in resources:
        if r["id"] == resource_id:
            return r
    return None


def add_resource(resource_id, name, category, total):
    if find_resource(resource_id) is not None:
        print("Error: that resource ID already exists.")
        return
    if not total.isdigit() or int(total) <= 0:
        print("Error: total must be a positive whole number.")
        return
    total = int(total)
    resources.append({"id": resource_id, "name": name, "category": category,
                      "total": total, "available": total})
    print("Resource added.")


def list_resources(items):
    if len(items) == 0:
        print("No resources found.")
        return
    for r in items:
        print(r["id"], "|", r["name"], "|", r["category"],
              "| total:", r["total"], "| available:", r["available"])


def borrow(fellow_id, resource_id, quantity):
    if fellow_id not in fellows:
        print("Error: fellow ID not found.")
        return
    resource = find_resource(resource_id)
    if resource is None:
        print("Error: resource ID not found.")
        return
    if not quantity.isdigit() or int(quantity) <= 0:
        print("Error: quantity must be a positive whole number.")
        return
    quantity = int(quantity)
    if quantity > resource["available"]:
        print("Error: only", resource["available"], "available.")
        return
    resource["available"] = resource["available"] - quantity
    borrow_records.append({"fellow_id": fellow_id, "resource_id": resource_id,
                           "borrowed": quantity, "returned": 0})
    print(fellows[fellow_id], "borrowed", quantity, resource["name"])


def units_on_loan(fellow_id, resource_id):
    count = 0
    for rec in borrow_records:
        if rec["fellow_id"] == fellow_id and rec["resource_id"] == resource_id:
            count = count + rec["borrowed"] - rec["returned"]
    return count


def return_item(fellow_id, resource_id, quantity):
    if fellow_id not in fellows:
        print("Error: fellow ID not found.")
        return
    resource = find_resource(resource_id)
    if resource is None:
        print("Error: resource ID not found.")
        return
    if not quantity.isdigit() or int(quantity) <= 0:
        print("Error: quantity must be a positive whole number.")
        return
    quantity = int(quantity)
    on_loan = units_on_loan(fellow_id, resource_id)
    if quantity > on_loan:
        print("Error: this fellow only has", on_loan, "on loan.")
        return
    resource["available"] = resource["available"] + quantity
    left = quantity
    for rec in borrow_records:
        if left == 0:
            break
        if rec["fellow_id"] == fellow_id and rec["resource_id"] == resource_id:
            can_return = rec["borrowed"] - rec["returned"]
            if can_return > left:
                can_return = left
            rec["returned"] = rec["returned"] + can_return
            left = left - can_return
    print(fellows[fellow_id], "returned", quantity, resource["name"])


def search_by_name(text):
    found = []
    for r in resources:
        if text.lower() in r["name"].lower():
            found.append(r)
    return found


def filter_by_category(category):
    found = []
    for r in resources:
        if r["category"].lower() == category.lower():
            found.append(r)
    return found


def report():
    total_units = 0
    available_units = 0
    for r in resources:
        total_units = total_units + r["total"]
        available_units = available_units + r["available"]
    borrowed_units = total_units - available_units

    print("Total units:", total_units)
    print("Available units:", available_units)
    print("Units currently borrowed:", borrowed_units)

    print("Resources with fewer than 3 available:")
    found_low = False
    for r in resources:
        if r["available"] < 3:
            print(" -", r["name"], "(" + str(r["available"]) + ")")
            found_low = True
    if not found_low:
        print(" none")

    # units currently borrowed for each resource
    most = 0
    amounts = {}
    for r in resources:
        amount = r["total"] - r["available"]
        amounts[r["id"]] = amount
        if amount > most:
            most = amount
    if most == 0:
        print("Most borrowed: nothing is on loan")
    else:
        print("Most borrowed (" + str(most) + " units):")
        for r in resources:
            if amounts[r["id"]] == most:
                print(" -", r["name"])


def save_data():
    with open("data.json", "w") as f:
        json.dump({"resources": resources, "borrow_records": borrow_records}, f)


def load_data():
    try:
        with open("data.json") as f:
            data = json.load(f)
        resources[:] = data["resources"]
        borrow_records[:] = data["borrow_records"]
    except (FileNotFoundError, ValueError, KeyError):
        pass  # no saved data yet, use the starting data


def run_demo():
    print("1. F001 borrows 2 laptops")
    borrow("F001", "R001", "2")
    print("2. F002 borrows 3 keyboards")
    borrow("F002", "R002", "3")
    print("3. F001 returns 1 laptop")
    return_item("F001", "R001", "1")
    print("4. F003 requests 4 headsets")
    borrow("F003", "R003", "4")
    print("5. F002 tries to return 4 keyboards")
    return_item("F002", "R002", "4")
    print("6. Search for LAPtop")
    list_resources(search_by_name("LAPtop"))
    print("7. Report")
    report()


def main():
    load_data()
    while True:
        print()
        print("1. List resources")
        print("2. Add resource")
        print("3. Borrow")
        print("4. Return")
        print("5. Search by name")
        print("6. Filter by category")
        print("7. Report")
        print("8. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            list_resources(resources)
        elif choice == "2":
            add_resource(input("ID: ").strip().upper(), input("Name: ").strip(),
                         input("Category: ").strip(), input("Total units: ").strip())
        elif choice == "3":
            borrow(input("Fellow ID: ").strip().upper(),
                   input("Resource ID: ").strip().upper(),
                   input("Quantity: ").strip())
        elif choice == "4":
            return_item(input("Fellow ID: ").strip().upper(),
                        input("Resource ID: ").strip().upper(),
                        input("Quantity: ").strip())
        elif choice == "5":
            list_resources(search_by_name(input("Name: ").strip()))
        elif choice == "6":
            list_resources(filter_by_category(input("Category: ").strip()))
        elif choice == "7":
            report()
        elif choice == "9":
            run_demo()
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Invalid choice, enter 1-8.")
            continue
        save_data()


main()import json

resources = [
    {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
    {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
    {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3},
]
fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
borrow_records = []  # each record: fellow_id, resource_id, borrowed, returned


def find_resource(resource_id):
    for r in resources:
        if r["id"] == resource_id:
            return r
    return None


def add_resource(resource_id, name, category, total):
    if find_resource(resource_id) is not None:
        print("Error: that resource ID already exists.")
        return
    if not total.isdigit() or int(total) <= 0:
        print("Error: total must be a positive whole number.")
        return
    total = int(total)
    resources.append({"id": resource_id, "name": name, "category": category,
                      "total": total, "available": total})
    print("Resource added.")


def list_resources(items):
    if len(items) == 0:
        print("No resources found.")
        return
    for r in items:
        print(r["id"], "|", r["name"], "|", r["category"],
              "| total:", r["total"], "| available:", r["available"])


def borrow(fellow_id, resource_id, quantity):
    if fellow_id not in fellows:
        print("Error: fellow ID not found.")
        return
    resource = find_resource(resource_id)
    if resource is None:
        print("Error: resource ID not found.")
        return
    if not quantity.isdigit() or int(quantity) <= 0:
        print("Error: quantity must be a positive whole number.")
        return
    quantity = int(quantity)
    if quantity > resource["available"]:
        print("Error: only", resource["available"], "available.")
        return
    resource["available"] = resource["available"] - quantity
    borrow_records.append({"fellow_id": fellow_id, "resource_id": resource_id,
                           "borrowed": quantity, "returned": 0})
    print(fellows[fellow_id], "borrowed", quantity, resource["name"])


def units_on_loan(fellow_id, resource_id):
    count = 0
    for rec in borrow_records:
        if rec["fellow_id"] == fellow_id and rec["resource_id"] == resource_id:
            count = count + rec["borrowed"] - rec["returned"]
    return count


def return_item(fellow_id, resource_id, quantity):
    if fellow_id not in fellows:
        print("Error: fellow ID not found.")
        return
    resource = find_resource(resource_id)
    if resource is None:
        print("Error: resource ID not found.")
        return
    if not quantity.isdigit() or int(quantity) <= 0:
        print("Error: quantity must be a positive whole number.")
        return
    quantity = int(quantity)
    on_loan = units_on_loan(fellow_id, resource_id)
    if quantity > on_loan:
        print("Error: this fellow only has", on_loan, "on loan.")
        return
    resource["available"] = resource["available"] + quantity
    left = quantity
    for rec in borrow_records:
        if left == 0:
            break
        if rec["fellow_id"] == fellow_id and rec["resource_id"] == resource_id:
            can_return = rec["borrowed"] - rec["returned"]
            if can_return > left:
                can_return = left
            rec["returned"] = rec["returned"] + can_return
            left = left - can_return
    print(fellows[fellow_id], "returned", quantity, resource["name"])


def search_by_name(text):
    found = []
    for r in resources:
        if text.lower() in r["name"].lower():
            found.append(r)
    return found


def filter_by_category(category):
    found = []
    for r in resources:
        if r["category"].lower() == category.lower():
            found.append(r)
    return found


def report():
    total_units = 0
    available_units = 0
    for r in resources:
        total_units = total_units + r["total"]
        available_units = available_units + r["available"]
    borrowed_units = total_units - available_units

    print("Total units:", total_units)
    print("Available units:", available_units)
    print("Units currently borrowed:", borrowed_units)

    print("Resources with fewer than 3 available:")
    found_low = False
    for r in resources:
        if r["available"] < 3:
            print(" -", r["name"], "(" + str(r["available"]) + ")")
            found_low = True
    if not found_low:
        print(" none")

    # units currently borrowed for each resource
    most = 0
    amounts = {}
    for r in resources:
        amount = r["total"] - r["available"]
        amounts[r["id"]] = amount
        if amount > most:
            most = amount
    if most == 0:
        print("Most borrowed: nothing is on loan")
    else:
        print("Most borrowed (" + str(most) + " units):")
        for r in resources:
            if amounts[r["id"]] == most:
                print(" -", r["name"])


def save_data():
    with open("data.json", "w") as f:
        json.dump({"resources": resources, "borrow_records": borrow_records}, f)


def load_data():
    try:
        with open("data.json") as f:
            data = json.load(f)
        resources[:] = data["resources"]
        borrow_records[:] = data["borrow_records"]
    except (FileNotFoundError, ValueError, KeyError):
        pass  # no saved data yet, use the starting data


def run_demo():
    print("1. F001 borrows 2 laptops")
    borrow("F001", "R001", "2")
    print("2. F002 borrows 3 keyboards")
    borrow("F002", "R002", "3")
    print("3. F001 returns 1 laptop")
    return_item("F001", "R001", "1")
    print("4. F003 requests 4 headsets")
    borrow("F003", "R003", "4")
    print("5. F002 tries to return 4 keyboards")
    return_item("F002", "R002", "4")
    print("6. Search for LAPtop")
    list_resources(search_by_name("LAPtop"))
    print("7. Report")
    report()


def main():
    load_data()
    while True:
        print()
        print("1. List resources")
        print("2. Add resource")
        print("3. Borrow")
        print("4. Return")
        print("5. Search by name")
        print("6. Filter by category")
        print("7. Report")
        print("8. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            list_resources(resources)
        elif choice == "2":
            add_resource(input("ID: ").strip().upper(), input("Name: ").strip(),
                         input("Category: ").strip(), input("Total units: ").strip())
        elif choice == "3":
            borrow(input("Fellow ID: ").strip().upper(),
                   input("Resource ID: ").strip().upper(),
                   input("Quantity: ").strip())
        elif choice == "4":
            return_item(input("Fellow ID: ").strip().upper(),
                        input("Resource ID: ").strip().upper(),
                        input("Quantity: ").strip())
        elif choice == "5":
            list_resources(search_by_name(input("Name: ").strip()))
        elif choice == "6":
            list_resources(filter_by_category(input("Category: ").strip()))
        elif choice == "7":
            report()
        elif choice == "9":
            run_demo()
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Invalid choice, enter 1-8.")
            continue
        save_data()


main()