price = input("Enter the price of an item: ")
quantity = input("Enter the quantity: ")

try:
    price_number = float(price)
    quantity_number = float(quantity)
    total = price_number / quantity_number
except ValueError:
    print("Please enter valid numbers.")
except ZeroDivisionError:
    print("Quantity can't be zero.")
except Exception as e:
    print(f"Something unexpected happened: {e}")
else:
    print(f"Price per unit: {total}")
finally:
    print("Calculation attempt finished.")