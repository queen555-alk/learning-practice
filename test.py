price = input("Enter the price of an item: ")

try:
    price_number = float(price)
    print(price_number * 2)
except ValueError:
    print("Please enter a valid number.")