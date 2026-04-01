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
        #print(f'value: {value}, last x: {last_x}, last y: {last_y}')
    return value, last_x, last_y

def mod_inverse(m, n):
    gcd, x, y = extended_gcd(m, n)
    if gcd != 1:
        raise ValueError("Inverse does not exist")
    return x % n

val = 23
mod = 1000
hw_val = 26
hw_val2 = 11
inverse = mod_inverse(val, mod)
hw = extended_gcd(hw_val, hw_val2)

print(f"The inverse of {val} modulo {mod} is {inverse}")

