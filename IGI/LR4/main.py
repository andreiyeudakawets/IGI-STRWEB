import task1
import task2.task2 as task2
import task3
import task4
import task5
from inputs  import try_input_int

def main():
    """ Allows the user to choose a task (1-5) and performs the corresponding action.    """

    print("\n1. CSV/PKL")
    print("2. Text analyzer")
    print("3. Plots")
    print("4. My Figure")
    print("5. NumPy")

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
    print("\n\nВыполнил Евдоковец Андрей, группа 253505\n\n")
    while True:
        main()
        stop = input("Enter 0 if you want to stop ")
        if stop == '0':
            break; 