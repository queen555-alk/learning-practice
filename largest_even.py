def largest_even(numbers):
    largest = None
    for number in numbers:
        if number % 2 == 0:
            if largest is None or number > largest:
                largest = number
    return largest

print(largest_even([3, 8, 15, 22, 7, 14]))