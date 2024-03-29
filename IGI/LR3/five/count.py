def count_for5(list):

    """
    Calculates the count of positive even numbers in the list and the sum of elements
    after the last occurrence of zero.

    Args:
        lst (list): Input list of integers.

    Returns:
        tuple: A tuple containing the count of positive even numbers and the sum of elements
               after the last zero (or None if no zero is found).
    """
    positive_even_count = 0
    sum_after_zero = 0
    zero_found = False

    for num in list:
        if num > 0 and num % 2 == 0:
            positive_even_count += 1
        elif num == 0:
            zero_found = True
            sum_after_zero = 0
        elif zero_found:
            sum_after_zero += num

    return positive_even_count, sum_after_zero