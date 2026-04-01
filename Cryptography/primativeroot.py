def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_primitive_root(g, n):
    if gcd(g, n) != 1:
        return False 
    
    phi_n = phi(n)
    print(phi_n)
    factors = prime_factors(phi_n)
    print(factors)
    
    for factor in factors:
        if pow(g, phi_n // factor, n) == 1:
            return False
    
    return True

def phi(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def prime_factors(n):
    factors = set()
    p = 2
    while p * p <= n:
        if n % p == 0:
            factors.add(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        factors.add(n)
    return factors

# Example usage:
n = 96989
a = 2
if is_primitive_root(a, n):
    print(f"{a} is a primitive root modulo {n}")
else:
    print(f"{a} is not a primitive root modulo {n}")
