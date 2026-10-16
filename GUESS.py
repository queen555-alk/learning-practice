import random


print("I'm thinking of a number between 1 and 20.")

while True:
    answer = input("Your guess: ")

    if not answer.isdigit():
        print("Please type a number.")
        continue

    guess = int(answer)
    tries += 1

    if