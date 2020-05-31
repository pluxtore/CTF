# Intro to Crypto 1 

### Information
Category: Crypto   
Difficulty: Baby  
Author: black-simon  
First Blood: Freax13  
Description: For my new RSA key I used my own   
SecurePrimeService which definitely generates a HUGE prime!

## Solution

From the description and difficulty of this challenge, we can conclude that somehow, prime generation is flawed such that either p or q is extremely small.
So we can try to conduct a factorization of the modulus N. N can be obtained through various methods, but in this case, the integer representation was already
available under the following paper: https://static.allesctf.net/Intro_Crypto.html .   
   
Now, we can just hardcode all integers and write our simple script that tries to find a factor that is cleanly divisible by N using a simple for-loop.
Finding the other factor gives us the knowledge of both p and q, which in this case we need, to compute the decryption exponent d.   

```python   
for i in range(2, 1000000):
    if N % i == 0:
        print("factor found: " + str(i))
	p = i
        break

print("calculating other factor ... ")
q = N/p

```

Now, we need to find the totient of N which can be expressed as (p-1)*(q-1). I will be referring to it as phi from now on.
Next, we use e and phi to compute the multiplicative inverse of e and phi, which should be d. An Implementation I found for this is here:   
https://gist.githubusercontent.com/JonCooperWorks/5314103/raw/a5b868644ee4cbfac349d6b2a9a4f4c651f2cd53/rsa.py   

The following code block merely imports and uses that function   

```python
e = 65537 # public exponent ( is in public key )
phi = (p-1) * (q-1) # compute totient
d = multiplicative_inverse(e, phi) # derive d from totient and e

```
Lastly, we can can take the integer representation of the ciphertext c to the power mod N and we get the flag printed out:   

```python
decrypted = pow(c, d, N)
# print(decrypted)
print(long_to_bytes(decrypted))
```

flag: CSCG{factorizing_the_key=pr0f1t}

## Prevention

The fatal mistake was here that p and q were not both two large random integers. A hypothetical patch could involve
the prime generation to be truly random.