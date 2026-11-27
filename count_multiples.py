def count_divisible(numbers, divisor):
    count = 0

    for num in numbers:
        if num % divisor == 0:
            count += 1

    return count
print(count_divisible( numbers = [3, 6, 7, 9, 12], divisor = 3))