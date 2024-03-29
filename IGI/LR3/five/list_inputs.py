import inputs
import random

def input_list(list):

    """
    Takes user input to create a list of numbers.

    Args:
        lst (list): An empty list to store user input.

    Returns:
        list: A list containing user-provided numbers.
    """

    size = inputs.try_input_int("Enter the size of list")

    while True:
        if size == 0:
            break
        number = inputs.try_input_float("Enter the number")
        list.append(number)
        size -= 1

    return list

def random_list(list):

    """
    Generates a list of random integers within a specified range.

    Args:
        lst (list): An empty list to store random numbers.

    Returns:
        list: A list containing randomly generated integers.
    """

    size = inputs.try_input_int("Enter the size of list")

    while True:
        if size == 0:
            break
        num = random.randint(-25, 25)
        list.append(num)
        size -= 1
    
    return list

def simple_generator():
    left_lim = -25
    right_lim = 25
    i = left_lim
    while i <= right_lim:
        yield i
        i += 1

def from_generator():
    """
    initializes list using generator
    """

    list = []
    for x in simple_generator():
        list.append(x)
    return list