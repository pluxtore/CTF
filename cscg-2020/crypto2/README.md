# Intro to Crypto 2 

## Information
Category: Crypto   
Difficulty: Baby   
Author: black-simon   
First Blood: Freax13   
Description: I learned my lesson from the mistakes made in the last challenge! Now p and q are huge, I promise!   

## Solution

The description of this challange implies that now p and q are both very large integer numbers. However they also need to be random large integer numbers!
The assumption is now that they may be huge, but still easy to factor because they are nearly the same value.   
   
Again, we need to somehow convert our resources to integers so we can work with them. The following script automates this for us:   

```python
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
```

Now, instead of starting factorization from 0, we simply take the square root of the modulus as staring value. 
We also use the is_prime function from gimpy to not test any nonprime values like in the first challange.   

```python
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
```

and we get the flag: CSCG{Ok,_next_time_I_choose_p_and_q_random...}

## Prevention

The fatal mistake was here that p and q were both two large similar integers. A hypothetical patch could involve
the prime generation to be truly random.