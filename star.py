#for i in range(1,6):
#   print("#" * i)


pin = input("Enter 4 digit pin: ").strip()
if len(pin) == 4 and not pin.isalnum() and not pin.isalpha():
    print("succesfully Entered")
else:
    print("invalid pin")
