
from five.count import count_for5
import five.list_inputs as list_inputs

def output(list):
    for i in list:
        print(i,end=" ")

def task5():
    
    """ 
    It allows the user to choose between
    manual input or random generation of a list.
    
    Counts the number of positive even elements in a given list. 
    """

    while True:
        option = input("select initialization method\nr - random\nu - user\n")
        if option == 'u':
            list = list_inputs.input_list(list=[])
            break
        elif option == 'r':
            #list = list_inputs.random_list(list=[])
            list = list_inputs.from_generator()
            break
        print("Error. Try again")

    #list = input_list(list = [])
    c, sum = count_for5(list)
 
    print()
    output(list)
    print(f"\nCount of positive even numbers: {c}")
    print(f"Sum of elements after the last zero: {sum}")
    
    