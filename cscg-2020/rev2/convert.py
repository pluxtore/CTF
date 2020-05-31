#!/usr/bin/python2

def convert77(text):
	print("Read in...:")
	new = ""
	for x in text:
		new += chr( (ord(x) + 0x77) % 256)
	new += '\n'
	return new
    

def main():
	print("starting...")
	text = open("../translation/hash.bin", "r").read()
	text = convert77(text)
	print(text)
	open("pw.bin", "w").write(text)



main()
