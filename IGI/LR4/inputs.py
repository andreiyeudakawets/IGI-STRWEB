def input_float(string):
    
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
        except Exception as e:
            print(f"\nError: {e}. Try again.")

    return x

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

def input_color(colors):
    
    while True:
        c = input(f"Select one of these colors: {colors}\n")
        if c in colors:
            return c
        else:
            print("Try again")