import random
from sympy import isprime

def generate_large_prime(n_digits):
    """Generate a random n-digit prime number."""
    lower_bound = 10**(n_digits - 1)
    upper_bound = 10**n_digits - 1

    while True:
        candidate = random.randint(lower_bound, upper_bound)
        if isprime(candidate):
            return candidate

def generate_sophie_germain_prime(n_digits):
    """Generate a Sophie Germain prime of at least n digits."""
    while True:
        p = generate_large_prime(n_digits)
        if isprime(2 * p + 1):
            return p

# Generate a Sophie Germain prime of at least 20 digits
sophie_germain_prime = generate_sophie_germain_prime(20)
print(f"Sophie Germain prime: {sophie_germain_prime}")
print(f"Corresponding prime (2p + 1): {2 * sophie_germain_prime + 1}")
