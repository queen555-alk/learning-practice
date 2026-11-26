numbers = [12, 43, 23, 76, 56, 64]
highest = numbers[0]
for num in numbers:
    if num > highest:
        highest = num
print("highest number is:", highest)