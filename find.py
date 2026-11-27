def find_number(numbers, target):
    count = 0
    for number in numbers:
        if number == target:
            return count
        else:
            count += 1
    return -1
print(find_number([5, 8, 5, 9], 99))