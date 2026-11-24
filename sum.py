def twoSum(nums: list[int], target: int) -> list[int]:
    for a in range(len(nums)):
        for p in range(a + 1, len(nums)):
            if nums[a] + nums[p] == target:
                return [a, p]

nums = [2, 7, 11, 15]
target = 9

print(twoSum(nums, target))
