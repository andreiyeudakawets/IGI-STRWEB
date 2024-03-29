from inputs import try_input_int
import task1
import task2
import task3
import task4
import five.task5 as task5


def main():

    """ Allows the user to choose a task (1-5) and performs the corresponding action.    """


    print("\n1. arcsin(x) using the Taylor series expansion.")
    print("2. The sum of every second number entered by the user.")
    print("3. The number of digits in a user-provided string.")
    print("4. string handler.")
    print("5. The count of positive even numbers in the list.")

    option = try_input_int("Choose the task to perform(1-5)")
    
    if option == 1:
        task1.task1()
    elif option == 2:
        task2.task2()
    elif option == 3:
        task3.task3()
    elif option == 4:
        task4.task4()
    elif option == 5:
        task5.task5()
    else:
        print("Error")

if __name__ == "__main__":
    while True:
        main()
        stop = input("Enter 0 if you want to stop ")
        if stop == '0':
            break;    
    