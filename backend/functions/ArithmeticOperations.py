import cv2
import numpy as np
from matplotlib import pyplot as plt


class ArithmeticOperations:
    def __init__(self):
        """Initializes the ImageArithmetic class."""
        pass
    """ 
    Function: Addition
    # Description: Adds two numbers
    # Input: Value1, Value2
    # Output: Added Sum
    """
    def Addition(self, variable1, variable2):
        addition= variable1+variable2
        return addition

    """
    Function: Subtraction
    # Description: Subtracts two numbers
    # Input: Value1, Value2
    # Output: Subtracted Difference
    """
    def Subtraction(self, variable1, variable2):
        subtraction= variable1-variable2
        return subtraction

    """
    Function: Division
    # Description: Divides two numbers
    # Input: Value1, Value2
    # Output: Divided Quotient
    """
    
    def Division(self, variable1, variable2):
        division= variable1/variable2
        return division
    

    """
    Function: Multiplication
    # Description: Multiplies two numbers
    # Input: Value1, Value2
    # Output: Multiplied Product
    """
    def Multiplication(self, variable1, variable2):
        multiplication= variable1*variable2
        return multiplication   
    
    """
    Function: Average
    # Description: Calculates the average of two numbers
    # Input: Value1, Value2
    # Output: Average of the two numbers
    """
    def Average(self, variable1, variable2):
        avg= (variable1+variable2)/2
        return avg
    
    """
    Function: Power
    # Description: Raises one number to the power of another
    # Input: Base, Exponent
    # Output: Result of the power operation
    """

    def power(self, variable1, variable2):
        power= variable1**variable2
        return power
    
    """
    Function: Square Root
    # Description: Calculates the square root of a number
    # Input: Number
    # Output: Square root of the number
    """
    def square_root(self, variable1):
        square_root= np.sqrt(variable1)
        return square_root
    
    """
    Function: Greater Than
    # Description: Checks if one number is greater than another
    # Input: Value1, Value2
    # Output: True if Value1 is greater than Value2, False otherwise
    """
    
    def greater_than(self, variable1, variable2):
        greater_than= variable1>variable2
        return greater_than
    
    """
    Function: Less Than
    # Description: Checks if one number is less than another
    # Input: Value1, Value2
    # Output: True if Value1 is less than Value2, False otherwise
    """
    def less_than(self, variable1, variable2):
        less_than= variable1<variable2
        return less_than
    
    """
    Function: Equal
    # Description: Checks if two numbers are equal
    # Input: Value1, Value2
    # Output: True if Value1 is equal to Value2, False otherwise
    """
    def equal(self, variable1, variable2):
        equal= variable1==variable2
        return equal
    
    """
    Function: Greater Than or Equal To
    # Description: Checks if one number is greater than or equal to another
    # Input: Value1, Value2
    # Output: True if Value1 is greater than or equal to Value2, False otherwise
    """
    def greater_than_equal (self, variable1, variable2):
        greater_than_equal= variable1>=variable2
        return greater_than_equal
    
    """
    Function: Less Than or Equal To
    # Description: Checks if one number is less than or equal to another
    # Input: Value1, Value2
    # Output: True if Value1 is less than or equal to Value2, False otherwise
    """
    def less_than_equal(self, variable1, variable2):
        less_than_equal= variable1<=variable2
        return less_than_equal
    
    """
    Function: Not Equal
    # Description: Checks if two numbers are not equal
    # Input: Value1, Value2
    # Output: True if Value1 is not equal to Value2, False otherwise
    """
    def not_equal(self, variable1, variable2):
        not_equal= variable1!=variable2
        return not_equal
    
    """
    Function: Rounding Off
    # Description: Rounds a number to the nearest integer
    # Input: Number
    # Output: Rounded number
    """
    def rounding_off(self, variable1,rounding_off):
        rounding_off= np.round(variable1,rounding_off)
        return rounding_off
    
    """
    Function: To Integer
    # Description: Converts a number to an integer
    # Input: Number
    # Output: Integer value of the number
    """
    def to_integer(self, variable1):
        to_integer= int(variable1)
        return to_integer
    
    """
    Function: Absolute Value
    # Description: Returns the absolute value of a number
    # Input: Number
    # Output: Absolute value of the number
    """
    def absolute_value(self, variable1):
        absolute_value= np.abs(variable1)
        return absolute_value
    
    """
    Function: In Range
    # Description: Checks if a number is within a specified range
    # Input: Number, Start, End
    """
    def in_range(self, variable1,a, variable2):
        in_range= a in range(variable1,variable2)
        return in_range
    
    """
    Function: Modulus Remainder
    # Description: Returns the remainder of a division
    # Input: Number, Divisor
    # Output: Remainder of the division
    """
    def modulus_remainder(self, variable1, variable2):
        modulus_remainder= variable1%variable2
        return modulus_remainder



