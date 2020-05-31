#!/usr/bin/python

from Crypto.Util.number import long_to_bytes


line = open("../translation/lights.txt", "r").read().split('\n')
print(line[0])
num_normal = line[0].replace('\t', '').replace(' ', '')
num_xor = line[0].replace('\t', '').replace(' ', '').replace('0', 'a').replace('1','0').replace('a', '1')


print(int(num_normal,2))
print(int(num_xor,2))
print(str(long_to_bytes(int(num_normal,2))))
print(str(long_to_bytes(int(num_xor,2))))