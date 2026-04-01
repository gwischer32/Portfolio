#turnns the letters into numbers
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
message = 'OIPPLRVBPQJXGWRUETENAXQRPCCCFTVONGZPDYXTGYQNWFLTLKFFCCUYGWIUHYOACDLEZFHDULBVOJPILFUIHRJUEXMFTZEZPMITEBEPRNICFSHNQVCHNPOEETLVXDXHRHYITIRLUGWMCNJJUXHPRDAMLPLWTRUYYAMNKRXFMCAMYTVLFVBTSFBDITKPXMCSXHGGIEMYBLXYCNXU'
key = 0
encrypted_numbers = []
for message_letter in message:
    i = -1
    for alphabet_letter in alphabet:
        i+=1
        if message_letter == alphabet_letter:
            encrypted_numbers.append((i+key)%26)
#print(encrypted_numbers)
#print(f'encrypted string of numbers = {string_of_numbers} ')
#turn numbers into letters
print('encrypted text: ', end='')
for number in encrypted_numbers:
    print(alphabet[number], end='')
print()
print()
decrypted_numbers = []
for number in encrypted_numbers:
    decrypted_numbers.append(((number-key)+26)%26)
#print(decrypted_numbers)
print('decrpyted text: ', end='')
for number in decrypted_numbers:
    print(alphabet[number], end='')

for key in range (26):
    decrypted_numbers = []
    for number in encrypted_numbers:
        decrypted_numbers.append(((number-key)+26)%26)

