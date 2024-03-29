

def try_input_int(string):
    
    """
    Requests an integer input from the user and handles exceptions.

    Args:
        string (str): Message for the user.

    Returns:
        int: The integer entered by the user.
    """

    while True:
        try:
            x = int(input(f"\n{string}: "))
            break
        except Exception:
            print("\nError! Try again")

    return x

def try_input_float(string):
    
    """
    Requests a floating-point input from the user and handles exceptions.

    Args:
        string (str): Message for the user.

    Returns:
        float: The floating-point number entered by the user.
    """

    while True:
        try:
            x = float(input(f"\n{string}: "))
            break
        except Exception:
            print("\nError! Try again")

    return x
