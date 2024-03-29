from inputs import try_input_int

def task2():

    """ Calculates the sum of every second number entered by the user.   """

    tot = 0
    counter = 0

    while True:
        number = try_input_int("Enter the number(0 to stop)")
        if number == 0:
            break

        if counter % 2 == 1:
            tot += number

        counter += 1
    
    total = tot
    #total = totl.total()

    if total == 0:
        print("\nNot enough elements entered")
    else:
        print(f"\nSum of the every second number: {total}")
