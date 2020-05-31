# Intro to Stegano 2

## Information
Category: Stegano   
Difficulty: Baby   
Author: explo1t   
First Blood: lolsalat   

## Solution

![](chall.jpg)


Unlike last time, strings gives no useful information. Also, we do not find hidden files via binwalk.
Our current strategy is now to find out how the image has been tampered with to encode our flag, so we 
aim at finding the original image. We can do this via a reverse image search, and in fact, we find the 
original!

![](orig.jpg)

Seeing that the Skyscraper on the left is a little different, we interpret the lights as binary, and note it all down nicely in a txt file. 

![](message.jpg)


The lights on the top left corner correspond to this binary message:


```txt
01000011
01010011
01000011
01000111
01111011
01100001
01011111
01000110
01101100
00110100
01100111
01111101
00000000
00000000
```


Our python script merely interprets our txt file and gives us the ascii representation of the message

```python
#!/usr/bin/python

txt = open("secret_message.txt").read()
_bytes = txt.split("\n")
res = []
i = 0
while i<len(_bytes)-2:
    res.append ( int(_bytes[i], 2) ) 
    i+=1

print(res)
intext = ""
for x in res:
    intext += chr(x)
print(intext)
```

and we get the flag: CSCG{a_Fl4g}


## Prevention

 If we wish to truly like to send a secret message such that it is unnoticed, we could just use steghide with a pre-settled strong password.