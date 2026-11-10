# Even or odd checker, leap year checker 

#number = int(input("Enter even number: "))
#if number % 2 == 0:
#    print(f"{number} is even")
#else:
#    print(f"{number} is odd")



#import calender

#year = int(input("Enter year : "))
#if calender.isleap(year):
#   print(f"{year} is a leap year")
#else:
#   print(f"{year} not a leap year")

                            #OR



#A year is a leap year if:
#• It is divisible by 4, and
#• It is not divisible by 100, or
#• It is divisible by 400.

year = int(input("Enter year: ")) 

if (year% 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year} is a leap year")
else:
    print(f"{year} is not a leap year")