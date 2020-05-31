# Intro to Reversing 1

## Information
Category: Reverse Engineering   
Difficulty: Baby   
Author: 0x4d5a   
First Blood: BoredPerson   
Description: Once you solved the challenge locally, grab your real flag at: nc hax1.allesctf.net 9600   

## Solution

Running strings on the provided binary, we notice a suspicious string that looks like it is our passphrase.   

`y0u_5h3ll_p455`

It turns out to actually work, so we connect to the server and get the flag: CSCG{ez_pz_reversing_squ33zy}   

## Prevention

Using strong hashing algorithms such as bcrypt for verification would resolve the issue at hand.
