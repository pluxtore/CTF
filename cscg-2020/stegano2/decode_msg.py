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
