import math

from inputs import try_input_float

#my factorial.
def fact(a):
    res = 1.0
    while True:
        if a != 0:
            res *= a
        a-=1
        if a <= 0.0:
            break

    return res    

def task1():

    """
    Calculates the arcsin(x) using the Taylor series expansion.

    User inputs:
    - x: A float within the range (-1, 1).
    - eps: A positive float representing the desired precision.

    (Prints the result and intermediate steps).
    """

    while True:
        x = try_input_float("-1 < x < 1")
        if x > 1 or x < -1:
            print("\nError")
            continue
        break

    #print(math.degrees(math.asin(x))).

    arcsin = math.asin(x)

    #print(math.asin(x)).

    while True:
        eps = try_input_float("Set precision eps")
        if eps <= 0 or eps > 1:
            print("\nError")
            continue
        break    

    n = 0.0
    max = 500.0
    result = 0.0
    current = 0.0
#99
    while True:    
        
        try:
            current = (fact(2*n)*math.pow(x,2*n+1)) / math.pow(4,n)/math.pow(fact(n), 2)/(2*n+1)
            result += (fact(2*n)*math.pow(x,2*n+1))/math.pow(4,n)/math.pow(fact(n), 2)/(2*n+1)    
        except Exception:
            print("Argumement for factorial is too big. Try decreasing the precision")
            result = None
            break

        if math.fabs(current) < eps:
            break
        if n == max:
            print("maximum iterations reached")
            break;
        n += 1.0

    print("x\tn\tf(x)\tMath.f(x)")
    print(f"{x}\t{n}\t{result}\t{arcsin}")


