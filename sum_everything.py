# Description
# Write a function named sum_above(numbers, limit) that returns the total of all numbers in the list that are strictly greater than limit.
# Constraints
# Do not use Python's built-in sum() function.
# Do not build a second list.
# Return 0 if no number is above the limit, or if the list is empty.
# Aim for O(n) time complexity.
# Examples
# Example 1 Input: numbers = [10, 3, 25, 8, 40], limit = 9 Output: 75
# Example 2 Input: numbers = [-5, 4, -1, 6], limit = -2 Output: 9
# Example 3 Input: numbers = [1, 2, 3], limit = 10 Output: 0
# Example 4 Input: numbers = [], limit = 5 Output: 0
# Hints
# Create a variable that starts at 0.
# Decide, for each number, whether it should be added at all.
# Is a number equal to the limit included?


def sum_above(numbers, limit):
    total = 0

    for number in numbers:
        if number > limit:
            total += number

    return total
print(sum_above(numbers = [10, 3, 25, 8, 40], limit = 9 ))