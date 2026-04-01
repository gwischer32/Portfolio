'''
Name:
COMP 2300
Date:
Homework 7
'''

# Bitwise addition and multiplication of binary numbers. Each of the two functions should take two ints as parameters, and the function should output the number as a binary string. If either of the parameters are negative, return None.

def bitwise_add(x: int, y: int) -> str:
    # Check for negative parameters
    if x < 0 or y < 0:
        return None
    
    while y != 0:
        # Calculate sum without carry
        sum_ = x ^ y
        # Calculate carry
        carry = (x & y) << 1
        # Update a and b
        x, y = sum_, carry
    
    
    return bin(x)[2:]  


def bitwise_mult(x, y): 
    # Placeholder function to do bitwise multiplication
    pass

def bitwise_mult(x: int, y: int) -> str:
    # Check for negative parameters
    if x < 0 or y < 0:
        return None
    
    result = 0
    while y > 0:
        # If the last bit of b is set, add a to the result
        if y & 1:
            result += x
        # Shift a left (multiply by 2)
        x <<= 1
        # Shift b right (divide by 2)
        y >>= 1
    
    # Return the result as a binary string
    return bin(result)[2:] 

def main():
    # Test cases to validate the implementation
    # Each test contains two numbers x and y and the expected result

    test_cases_add = [
        # Bitwise Add Cases
        (0, 0, "0"),
        (0, 1, "1"),
        (1, 0, "1"),
        (1, 1, "10"),
        (1, 2, "11"),
        (2, 1, "11"),
        (3, 3, "110"),
        (3, 4, "111"),
        (4, 3, "111"),
        (4, 4, "1000"),
        (4, 5, "1001"),
        (6, 5, "1011"),
        (6, 6, "1100"),
        (6, 7, "1101"),
        (7, 6, "1101"),
        (8, 7, "1111"),
        (8, 8, "10000"),
        (8, 9, "10001"),
        (9, 8, "10001"),
        (9, 9, "10010"),
        (10, 10, "10100"),
        (10, 11, "10101"),
        (11, 10, "10101"),
        (11, 11, "10110"),
        (11, 12, "10111"),
        (12, 11, "10111"),
        (14, 13, "11011"),
        (14, 14, "11100"),
        (14, 15, "11101"),
        (15, 14, "11101"),
        (15, 15, "11110"),
        (1365, 21, "10101101010"),
        (2706, 2187, "1001100011101"),

        # Error Cases
        (-1, 1, None),
        (1, -1, None),
        (-1, -1, None)
    ]

    test_cases_mult = [
        # Bitwise Mult Cases
        (0, 0, "0"),
        (0, 1, "0"),
        (1, 0, "0"),
        (1, 1, "1"),
        (1, 2, "10"),
        (2, 1, "10"),
        (3, 3, "1001"),
        (3, 4, "1100"),
        (4, 3, "1100"),
        (4, 4, "10000"),
        (4, 5, "10100"),
        (6, 5, "11110"),
        (6, 6, "100100"),
        (6, 7, "101010"),
        (7, 6, "101010"),
        (8, 7, "111000"),
        (8, 8, "1000000"),
        (8, 9, "1001000"),
        (9, 9, "1010001"),
        (10, 10, "1100100"),
        (10, 11, "1101110"),
        (11, 4, "101100"),
        (14, 14, "11000100"),
        (14, 15, "11010010"),
        (15, 15, "11100001"),
        (181, 121, "101010110001101"),
        (2706, 2187, "10110100100110101000110"),

        # Error Cases
        (-1, 1, None),
        (1, -1, None),
        (-1, -1, None)
    ]

    # Test Bitwise Add
    for x, y, expected in test_cases_add:
        result = bitwise_add(x, y)
        assert result == expected, f"Expected: {expected}, Got: {result}, x: {x}, y: {y}"
    print("Bitwise Add Test Cases Passed")

    # Test Bitwise Mult
    for x, y, expected in test_cases_mult:
        result = bitwise_mult(x, y)
        assert result == expected, f"Expected: {expected}, Got: {result}, x: {x}, y: {y}"
    print("Bitwise Mult Test Cases Passed")

if __name__ == "__main__":
    main()