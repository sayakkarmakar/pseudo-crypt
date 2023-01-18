
from __future__ import print_function
from lib2to3.pytree import generate_matches
import numpy as np
import sys
SYMBOLS = r""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""

def main():
    message = input('Enter message: ')
    key = int(input('Enter key : '))
    mode = input('Encrypt/Decrypt [E/D]: ')
    if mode.lower().startswith('e'):
              mode = 'encrypt'
              translated = encryptMessage(key, message)
    elif mode.lower().startswith('d'):
              mode = 'decrypt'
              translated = decryptMessage(key, message)
    print('\n%sed text: \n%s' % (mode.title(), translated))
def getKeyParts(k):
    key = generate(k)
    keyA = key // len(SYMBOLS)
    keyB = key % len(SYMBOLS)
    return (keyA, keyB)
def encryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'encrypt')
    print(keyA,keyB)
    cipherText = ''
    for symbol in message:
        if symbol in SYMBOLS:
            symIndex = SYMBOLS.find(symbol)
            cipherText += SYMBOLS[(symIndex * keyA + keyB) % len(SYMBOLS)]
        else:
            cipherText += symbol
    return cipherText
def decryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'decrypt')
    plainText = ''
    modInverseOfkeyA = findModInverse(keyA, len(SYMBOLS))
    for symbol in message:
        if symbol in SYMBOLS:
            symIndex = SYMBOLS.find(symbol)
            plainText += SYMBOLS[(symIndex - keyB) * modInverseOfkeyA % len(SYMBOLS)]
        else:
            plainText += symbol
    return plainText
def checkKeys(keyA, keyB, mode):
    if keyA == 1 and mode == 'encrypt':
        sys.exit('The affine cipher becomes weak when key A is set to 1. Choose different key')
    if keyB == 0 and mode == 'encrypt':
        sys.exit('The affine cipher becomes weak when key A is set to 1. Choose different key')
    if keyA < 0 or keyB < 0 or keyB > len(SYMBOLS) - 1:
        sys.exit('Key A must be greater than 0 and key B must be between 0 and %s.' % (len(SYMBOLS) - 1))
    if gcd(keyA, len(SYMBOLS)) != 1:
        sys.exit('Key A %s and the symbol set size %s are not relatively prime. Choose a different key.' % (keyA, len(SYMBOLS)))
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def findModInverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q *v3), v1, v2, v3
    return u1 % m     
def memristor(xinit, yinit, zinit, num_steps):

    dt = 0.01

    # Initializing 3 empty lists
    xs = np.empty(num_steps + 1)
    ys = np.empty(num_steps + 1)
    zs = np.empty(num_steps + 1)

    xs[0], ys[0], zs[0] = (xinit, yinit, zinit)

    a=1/10**6
    b=4.7*10**3
    c=10**3
    d=1/10**-8
    e=22*10**3

    for i in range(num_steps):
        xs[i + 1] = xs[i]+(( (ys[i]+zs[i])) * dt)
        ys[i + 1] = ys[i]+(a*(-xs[i] -((ys[i])**3*b+c)) * dt)
        zs[i + 1] = zs[i]+(( d* ys[i]/e) * dt)
    return xs, ys, zs
def generate(k):
    xkey, ykey, zkey = memristor(10*k,20*k,30*k,1)
    key = abs(int(zkey[1]+xkey[1]*ykey[1]))
    if ((key)>10000): 
        while(key>10000):
            key = key//10
    elif (key<999):
            while(key<999):
                key = key*10
    else:
        if(key>9000):key = key-2000
        elif(key<2000):key = key+2000
    return(key)
if __name__ == '__main__':
    main()