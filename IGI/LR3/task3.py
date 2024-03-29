

def task3():

    """ Counts the number of digits in a user-provided string.  """

    string = input("Enter your string: ")
    
    counter = 0

    for char in string:

        if char.isdigit():

            counter += 1
    

    if counter != 0:
        print(f"Number of digits in your string: {counter}")
    else:
        print("It seems your string does not contain any digits")