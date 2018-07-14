# Matt Zhang
# 2014-01-03
# Python 3.3.3

# So this XOR thing just means converting the text to ASCII integers first, then using the
# binary integers to perform XOR addition (digitwise mod-2 addition). The symbol to do
# this in python is ^.

import numpy

encryptedFile=open('059_data.txt')
encrypted=numpy.loadtxt(encryptedFile,delimiter=',')
codeSize=len(encrypted)
# Try all keys from 'aaa' to 'zzz'. Set found=True when the correct key is found.
count=-1
found=False
punctuation='''!$%*()_-=+\/.,><:;'"?| '''
# First, XOR the first character of the key with every third character of the encryption.
# Make sure you don't get nonalphabetic characters before moving on to the next character.
for a in range(ord('a'),ord('z')+1):
    decoded=['']*codeSize
    okay=True
    for place in range(0,codeSize,3):
        decodedCharacter=chr(int(encrypted[place])^a)
        if decodedCharacter.isalpha() or decodedCharacter.isdigit() or decodedCharacter in punctuation:
            decoded[place]=decodedCharacter
        else:
            okay=False
            break
    if not okay:
        continue
    # Repeat for second character of key.
    for b in range(ord('a'),ord('z')+1):
        okay=True
        for place in range(1,codeSize,3):
            decodedCharacter=chr(int(encrypted[place])^b)
            if decodedCharacter.isalpha() or decodedCharacter.isdigit() or decodedCharacter in punctuation:
                decoded[place]=decodedCharacter
            else:
                okay=False
                break
        if not okay:
            continue
        # Repeat for third character of key.
        for c in range(ord('a'),ord('z')+1):
            okay=True
            for place in range(2,codeSize,3):
                decodedCharacter=chr(int(encrypted[place])^c)
                if decodedCharacter.isalpha() or decodedCharacter.isdigit() or decodedCharacter in punctuation:
                    decoded[place]=decodedCharacter
                else:
                    okay=False
                    break
            if not okay:
                continue
            decodedMessage=''.join(decoded)
            if decodedMessage.find('the')>-1:
                print('Key is \'',chr(a)+chr(b)+chr(c),'\'.\n',sep='')
                print('Message:',decodedMessage,'\n')
                print('ASCII sum is',str(sum(ord(i) for i in decoded))+'.')
                found=True
                break
        if found:
            break
    if found:
        break
            
encryptedFile.close()
