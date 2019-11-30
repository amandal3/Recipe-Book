# User Interface
import RecipeInit
from RecipeInit import *

## FOR USERS:
print("Welcome to my recipe book.")
user = int(input("To begin press 1: "))
while user == 1:
    m = MainMenu()
    m.optionOne()
    m.optionTwo()
    m.optionThree()
    m.optionFour()
    m.optionFive()
    
    user = int(input ("Press 1 to test again. Another number to exit: "))

print("Goodbye")


