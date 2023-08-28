import math

def quadraticFormula(sign, c_1, c_2, c_3, verbos=False):
    """
    Calculates the roots of a quadratic equation using the quadratic formula.
    
    Parameters:
        sign (int): An integer representing the sign (+1 or -1) to determine the two roots.
        c_1 (float): Coefficient of the quadratic term.
        c_2 (float): Coefficient of the linear term.
        c_3 (float): Coefficient of the constant term.
        verbose (bool, optional): Flag indicating whether to print a warning message if the discriminant is negative.
    
    Returns:
        float or str: If the discriminant is negative, returns 'error'.
                      Otherwise, returns the root of the quadratic equation.
    """
    if abs(sign) != 1:
        raise ValueError('sign must be +1 or -1')

    num = c_2**2 - 4*c_1*c_3
    if num < 0:
        if verbos:
            print('WARNING: num cannot be < 0')
        return 'error'
    return ( -c_2 + sign*num**(1/2) ) / (2*c_1)

def limitAngle(angle, lower=0, upper=2*math.pi, verbos=False):
    """
    Limits an angle (theta) within a specified range.
    
    Parameters:
        theta (float): The angle to be limited.
        lower (float, optional): The lower limit for the angle. Default is `0`.
        upper (float, optional): The upper limit for the angle. Default is `2*math.pi`.
        verbose (bool, optional): Flag indicating whether to raise a ValueError if the upper limit is not greater than the lower limit.
    
    Returns:
        float: The limited angle value.
    
    Raises:
        ValueError: If the upper limit is not greater than the lower limit.
    """
    if lower >= upper:
        raise ValueError('upper must be > than lower')
        
    while angle < lower:
        angle = angle + 2*math.pi
    while angle > upper:
        angle = angle - 2*math.pi
        
    return angle