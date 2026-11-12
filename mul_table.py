maxNumber = 12

for i in range(1, maxNumber + 1):
    print(f"Multiplication Table for {i}")
    
    for j in range(1, maxNumber + 1):
        product = i * j
        print(f"{i} x {j} = {product}")
        
    print("")  # Prints a blank line to separate each table
