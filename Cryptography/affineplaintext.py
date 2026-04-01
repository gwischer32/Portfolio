from gcd import gcd

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def encrypt_affine( plaintext, a, b ) :
    if gcd(a,26) != 1 :
        raise ValueError('a must be coprime to 26')
    
    plaintext_in_numbers = [ord(c) - ord('a') for c in plaintext]
    #affice cipher: ax + b
    ciphertext_in_numbers = [(n*a+b)%26 for n in plaintext_in_numbers]
    ciphertext = ''.join([chr(m + ord('a')) for m in ciphertext_in_numbers])

    return ciphertext.upper()

def decrypt_affine(ciphertext, a, b) :
    if gcd(a,26) != 1 :
        raise ValueError('a must be coprime to 26')
    
    ciphertext_in_numbers = [ord(c) - ord('A') for c in ciphertext]
    #affice cipher: ax + b
    plaintext_in_numbers = [(modinv(a,26)*(n-b))%26 for n in ciphertext_in_numbers]
    plaintext = ''.join([chr(m + ord('A')) for m in plaintext_in_numbers])

    return plaintext.lower()

def main() :
    plaintext = 'lastnightidrovetoharpersferryandithoughtaboutyouthereweresignsontheroadthatwarnedmeofstopsignsthespeedlimitkeptdecreasingbytenasweenteredatownabouthalfwaythereitwasalmostrainingatthetrainstationweputourhoodsonourheadsatthetrainstationwethrewrocksintotherivertheriverunderneaththetraintracks'
    ciphertext = 'PAARCDJRWUDQCZKEDQVNDJHQD'
    c=encrypt_affine(plaintext, 3, 3)
    d=decrypt_affine(ciphertext, 23, 15)
    print(c)
    print(d)
if __name__ == '__main__' :
    main()