import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def jacobi(a, n):
    if a == 0:
        return 0
    if a == 1:
        return 1
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    return 0

def solovay_strassen(n, k=5):
    if n < 2:
        return False
    if n != 2 and n % 2 == 0:
        return False
    for _ in range(k):
        a = random.randint(2, n - 1)
        x = jacobi(a, n)
        print(x)
        if x == 0 or pow(a, (n - 1) // 2, n) != (x % n):
            return False
    return True

# Example usage:
n = 56052361  # Carmichael number (composite)
base = 55146139  # Base for testing
if solovay_strassen(n):
    print(f"{n} is probably prime")
else:
    print(f"{n} is composite")
