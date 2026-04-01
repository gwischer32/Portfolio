'''
Name:
COMP 2300
Date:
Homework 7
'''


def square_and_multiply(base: int, exponent: int, modulus: int):
    # Check for invalid modulus
    if modulus <= 0:
        return None
    # Check for negative exponent
    if exponent < 0:
        return None
    
    new_b = base % modulus
    answer = 1
    while exponent > 0:
        if exponent % 2 == 1:
            answer = (answer * new_b) % modulus
        new_b = (new_b ** 2) % modulus
        exponent = exponent // 2

    return answer


def main():
    # Test cases to validate the implementation
    # Each test case contains base, exponent, modulus, and expected result
    test_cases = [
        # Base Tests
        (2, 5, 13, 6),      # 2^5 % 13 = 6
        (5, 3, 13, 8),      # 5^3 % 13 = 8
        (7, 4, 11, 3),      # 7^4 % 11 = 3
        (10, 3, 17, 14),    # 10^3 % 17 = 14
        (3, 6, 19, 7),      # 3^6 % 19 = 1
        (9, 5, 23, 8),      # 9^5 % 23 = 8
        (8, 7, 29, 17),     # 8^7 % 29 = 24
        (6, 4, 25, 21),     # 6^4 % 25 = 1
        (4, 9, 31, 8),      # 4^9 % 31 = 21
        (11, 3, 7, 1),      # 11^3 % 7 = 6
        (12743, 128573, 7472, 2311), # 12743^128573 % 7472 = 2311
        (1747291, 58692917, 10472, 1491), # 1747291^58692917 % 10472 = 1491

        # Additional Tests
        # Modulus is 1 - Return 0
        (123, 456, 1, 0), # 123^456 % 1 = 0

        # Modulus is Negative - Return None
        (123, 456, -10, None), # 123^456 % -10 = None

        # Exponent is Negative - Return None
        (123, -456, 10, None), # 123^-456 % 10 = None

        # Base is Negative - Return Calculated Value
        (-123, 456, 10, 1) # -123^456 % 10 = 1

    ]

    # Running test cases with assertions
    for base, exponent, modulus, expected in test_cases:
        assert square_and_multiply(base, exponent, modulus) == expected, f"Failed for {base}^{exponent} % {modulus}"
    
    print("All test cases passed.")

if __name__ == "__main__":
    main()


