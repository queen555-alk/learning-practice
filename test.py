#price = input("Enter the price of an item: ")

#try:
    #price_number = float(price)
    #print(price_number * 2)
#except ValueError:
    #print("Please enter a valid number.")


#the modified version of the one above
while True:
    price = input("Enter the price of an item: ")

    try:
        price_number = float(price)
        if price_number < 0:
            print("Price cannot be negative. Please try again.")
            continue
        print(f"Double the price: {price_number * 2:.2f}")
        break
    except ValueError:
        print("Please enter a valid number.")