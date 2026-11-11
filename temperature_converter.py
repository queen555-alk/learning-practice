temp = float(input("Enter the Temperature: "))

unit =  input("Enter C for Celius or F for farenheit:")

#• Celsius to Fahrenheit: Multiply by 1.8 (or 9/5) and add 32.
#• Fahrenheit to Celsius: Subtract 32, then multiply by 5/9.

converted_temp = (temp * 1.8) + 32
converted_temp = (temp - 32) * 5/9

#IF unit is equal to "C":
#    SET converted_temp to (temp * 1.8) + 32
#    DISPLAY temp + "°C is equal to " + converted_temp + "°F"

#ELSE IF unit is equal to "F":
#    SET converted_temp to (temp - 32) * 5/9
#    DISPLAY temp + "°F is equal to " + converted_temp + "°C"

#ELSE:
#    DISPLAY "Invalid unit entered"

if unit == "C":
    converted_temp = (temp * 1.8) + 32
    print(f"{temp}°C is equal to {converted_temp}°F")
elif unit == "F":
    converted_temp = (temp - 32) * 5/9
    print(f"{temp}°F is equal to {converted_temp}°C")
else:
    print("Invalid unit entered")


