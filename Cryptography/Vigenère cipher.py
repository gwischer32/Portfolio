def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.upper()
    key = key.upper()
    ciphertext = ""
    
    # Iterate over each character in the plaintext
    for i in range(len(plaintext)):
        # Get the numerical values of the current plaintext character and key character
        plaintext_value = ord(plaintext[i]) - ord('A')
        key_value = ord(key[i % len(key)]) - ord('A')
        # Apply the cipher encryption formula

        encrypted_value = (plaintext_value + key_value) % 26
    
        # Convert the encrypted value back to a character and append it to the ciphertext
        ciphertext += chr(encrypted_value + ord('A'))
    
    return ciphertext
plaintext = "Were no strangers to love You know the rules and so do I full commitments what Im thinking of You wouldnt get this from any other guy I just wanna tell you how Im feeling Gotta make you understand Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you"
plaintext2 = ''
for letter in plaintext:
    if letter != ' ':
        plaintext2+=letter
plaintext2 = plaintext2.lower()

key = "obiwankenobi"
ciphertext = vigenere_encrypt(plaintext2, key)
print('Plaintext:', plaintext2)
print("Ciphertext:", ciphertext)
def vigenere_dencrypt(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = key.upper()
    plaintext = ""
    ciphertext2 = ''
    # Iterate over each character in the plaintext
    for i in range(len(ciphertext)):
        # Get the numerical values of the current plaintext character and key character
        ciphertext_value = ord(ciphertext[i]) - ord('A')
        key_value = ord(key[i % len(key)]) - ord('A')
        # Apply the cipher encryption formula

        decrypted_value = ((ciphertext_value - key_value)+26) % 26
    
        # Convert the encrypted value back to a character and append it to the ciphertext
        ciphertext2 += chr(decrypted_value + ord('A'))
    
    return ciphertext2
decrypted = vigenere_dencrypt(ciphertext, key)
#print(f'decrypted text: {decrypted}')
print(f'key: {key}')
