def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp = exp // 2
    return result

# Given values
d = 7829
n = 7533
ciphertext = [92, 7031, 759, 2380]

# Decrypt each ciphertext value
plaintext = [mod_exp(c, d, n) for c in ciphertext]
print(plaintext)
