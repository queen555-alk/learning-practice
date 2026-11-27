def count_letter(text, letter):
    counter = 0

    for char in text:
        if char.lower() == letter.lower():
            counter+= 1

    return counter
print(count_letter("Banana", letter = "a"))