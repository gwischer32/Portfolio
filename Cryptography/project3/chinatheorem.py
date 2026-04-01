def extended_gcd(value, modulo):
    x = 0
    y = 1
    last_x = 1
    last_y = 0
    while modulo != 0:
        quotient = value // modulo
        remainder = value % modulo
        value, modulo = modulo, remainder
        x, last_x = last_x - quotient*x, x
        y, last_y = last_y - quotient*y, y
    return value, last_x, last_y

def mod_inverse(m, n):
    gcd, x, y = extended_gcd(m, n)
    if gcd != 1:
        raise ValueError("Inverse does not exist")
    return x % n

def solve_congruences(a1, m1, a2, m2):
    gcd, s, t = extended_gcd(m1, m2)
    if (a1 - a2) % gcd != 0:
        raise ValueError("No solution exists")
    else:
        lcm = m1 * (m2 // gcd)
        x = (a1 * (m2 // gcd) * t + a2 * (m1 // gcd) * s) % lcm
        return x
    
#solution = solve_congruences(4,7,3,11)
#print(solution)