english_freq = [
    0.082,  # a
    0.015,  # b
    0.028,  # c
    0.043,  # d
    0.127,  # e
    0.022,  # f
    0.020,  # g
    0.061,  # h
    0.070,  # i
    0.002,  # j
    0.008,  # k
    0.040,  # l
    0.024,  # m
    0.067,  # n
    0.075,  # o
    0.019,  # p
    0.001,  # q
    0.060,  # r
    0.063,  # s
    0.091,  # t
    0.028,  # u
    0.010,  # v
    0.023,  # w
    0.001,  # x
    0.020,  # y
    0.001,  # z
]
from gcd import gcd

def count_letter_freqs( text: str ) -> list :
    stripped_text = text.strip()
    alpha_text = [c.upper() for c in stripped_text if c.isalpha()]

    letter_freqs = [0 for i in range(26)]

    for t in alpha_text :
        letter_freqs[ord(t)-ord('A')] += 1

    percent_freqs = []
    for i in letter_freqs :
        percent_freqs.append(i/len(alpha_text))

    return percent_freqs

def find_index_of_coincidence( text: str ) -> float :
    letter_freqs = count_letter_freqs(text)

    sqaured_freqs = [f**2 for f in letter_freqs]

    return sum(sqaured_freqs)

def find_mutual_index_of_coincidence( freqs1: list, freqs2: list ) -> float :
    if len(freqs1) != len(freqs2) :
        raise ValueError('Lists must have the same length')
    
    mic = 0
    for i in range(len(freqs1)) :
        mic += freqs1[i]*freqs2[i]

    return mic

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
    
def decrypt_affine(ciphertext, a, b) :
    if gcd(a,26) != 1 :
        raise ValueError('a must be coprime to 26')

    ciphertext_in_numbers = [ord(c) - ord('A') for c in ciphertext]
    #affice cipher: ax + b
    plaintext_in_numbers = [(modinv(a,26)*(n-b))%26 for n in ciphertext_in_numbers]
    plaintext = ''.join([chr(m + ord('A')) for m in plaintext_in_numbers])

    return plaintext.lower()

def count_letter_freqs( text: str ) -> list :
    stripped_text = text.strip()
    alpha_text = [c.upper() for c in stripped_text if c.isalpha()]

    letter_freqs = [0 for i in range(26)]

    for t in alpha_text :
        letter_freqs[ord(t)-ord('A')] += 1

    percent_freqs = []
    for i in letter_freqs :
        percent_freqs.append(i/len(alpha_text))

    return percent_freqs

def affine_cryptanalysis(ciphertext: str) -> str :
    mics = dict()

    for a in [1,3,5,7,9,11,15,17,19,21,23,25] :
        for b in range(26) :
            decr = decrypt_affine(ciphertext, a, b)
            freqs = count_letter_freqs(decr)
            mics[(a,b)] = find_mutual_index_of_coincidence(english_freq, freqs)
            print((a,b), mics[(a,b)])

    real_pair = max(mics, key=mics.get)
    print(real_pair)
    return decrypt_affine(ciphertext, real_pair[0], real_pair[1])

a=affine_cryptanalysis('ouhuriyphercuhypijixuwigsrioptuhgjuyerdyidiklgjjmiaakpaurpyotepkaptkrskrcilwigoigjdrpcupptkylhiaerwiptuhcgwkbgypoerrepujjwigtiokaluujkrccippeaesuwiggrduhyperdruxuhcirreckxuwiggzruxuhcirrejupwigdiorruxuhcirrehgrehigrderdduyuhpwigruxuhcirreaesuwigmhwruxuhcirreyewciidvwuruxuhcirrepujjejkuerdtghpwig'.upper())
print(a)









