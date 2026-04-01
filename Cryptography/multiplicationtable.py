import math

def count_multiplicative_inverses(mod):
    count = 0
    for i in range(mod):
        if math.gcd(i, mod) == 1:
            count += 1
    return count

mod = 12
count = count_multiplicative_inverses(mod)
print("The number of numbers in the set {0, 1, 2, ..., 18} that have multiplicative inverses modulo", mod, "is:", count)
