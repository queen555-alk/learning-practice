def index_smallest(numbers):
    if not numbers:
        return -1

        num = 0
        for i in range(1, len(numbers)):
            if numbers[i] < numbers[num]:
                num = i
        return num
print(index_smallest([8, 3, 12, 1, 7]))
