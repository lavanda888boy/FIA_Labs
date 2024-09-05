# TODO: add your imports here:
from rules import LUNA_GUESTS_RULES
from production import forward_chain

if __name__=='__main__':

    #TODO: implement your code here!
    print(forward_chain(LUNA_GUESTS_RULES, ['tim wears baggy clothes', 'tim has small luggage', 'tim is in the group of similar looking people'], verbose=True))
    
    # example how to print output:
    # print("Welcome to Expert System! TODO: implement")

    # # an example how to read input:
    # input_name = input("please write your name:\n")

    # print("Hello, ", input_name, "!")

    # # example how to read a numeric input:
    # input_age = int(input("what is your age?\n"))
    # print("Your age is", input_age)

    # print("Great! Now please implement the code for the lab :) ")