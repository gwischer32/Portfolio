def jacobi(a, n):
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd number.")

    a = a % n
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

        a = a % n

    if n == 1:
        return result
    else:
        return 0


def modular_sqrt(a, p):
    """Find a quadratic residue (mod p) of 'a'. p must be an odd prime.
    Solve the congruence of the form:
        x^2 ≡ a (mod p)
    And returns x. Note that p - x is also a root.
    Returns 0 if no solution exists.
    """
    # Check if a is a quadratic residue modulo p
    if jacobi(a, p) != 1:
        return 0

    # Simple cases
    if a == 0:
        return 0
    if p == 2:
        return a % 2
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Factor p-1 as q * 2^s
    s = 0
    q = p - 1
    while q % 2 == 0:
        s += 1
        q //= 2

    # Find a non-residue z
    z = 2
    while jacobi(z, p) != -1:
        z += 1

    # Initialize variables
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)

    while t != 0 and t != 1:
        # Find the least i such that t^(2^i) ≡ 1 (mod p)
        t2i = t
        i = 0
        for i in range(1, m):
            t2i = pow(t2i, 2, p)
            if t2i == 1:
                break

        # Update variables
        b = pow(c, 2 ** (m - i - 1), p)
        m = i
        c = (b * b) % p
        t = (t * b * b) % p
        r = (r * b) % p

    return r

# Example usage
# a = 2123
# p = 4831
# result = modular_sqrt(a, p)
# if result == 0:
#     print(f"No modular square root exists for {a} modulo {p}.")
# else:
#     print(f"Modular square roots of {a} modulo {p} are {result} and {p - result}.")

# # Testing the function
#print(jacobi(1002, 9907))  # Example usage
