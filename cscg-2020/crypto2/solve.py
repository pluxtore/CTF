#!/usr/bin/python

import os
import math
from Crypto.Util.number import long_to_bytes
import gmpy2 as gmpy2

#################### FUNCTIONS #######################
def isPerfectSquare(x): 
    n = gmpy2.mpz(x)
    return gmpy2.is_square(n)
    
def getIntSquare(x):
    n = gmpy2.mpz(x)
    return gmpy2.isqrt(n)

def multiplicative_inverse(e, phi): # taken from external source
# https://gist.githubusercontent.com/JonCooperWorks/5314103/raw/a5b868644ee4cbfac349d6b2a9a4f4c651f2cd53/rsa.py
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi


def computeD(modulo,p): # modulo, p factor
    q = modulo/p
    phi = (p-1)*(q-1)
    d = multiplicative_inverse(2**16+1,phi)
    return d


def WriteResult(d,c,modulo): # d, ciphertext, modulo
    modulo = pow(c,d,modulo)
    modulo = long_to_bytes(modulo)
    print("[*]  decrypted message")
    print("[*]  flag: " + modulo)





os.system("openssl rsa -pubin -in ../resources/pubkey.pem -text -noout > ../translation/pk.txt")
modulo_file = open("../translation/pk.txt")
modulo_file.readline()
modulo_file.readline()
modulo = modulo_file.read().split("E")[0]
modulo = modulo.replace(' ', '')
modulo = modulo.replace('\n', '')
modulo = modulo.replace(':', '')
modulo = int(modulo, 16)
open("../translation/modulo.txt", "w").write(str(modulo))
encrypted_message = str(open("../resources/message.txt").read())
decrypted_message = 0
encrypted_message = int(encrypted_message, 10)



isr = getIntSquare(modulo)
print("[*] approx. integer square root: " + str(isr)[:66] + " ... ")

i = isr-1
print("[*] testing for two factors roughly the same...")
while i<(isr+2**16+2):
    if gmpy2.is_prime((gmpy2.mpz(i))):
        if modulo%i==0:
            print("[*]  WIN!!!")
            print("[*] factor is: " + str(i)[:66] + " ... ")
            print("[*] saving to file ...")
            d = computeD(modulo, i)
            WriteResult(d, encrypted_message,modulo)
            exit(0)
    i+=1

