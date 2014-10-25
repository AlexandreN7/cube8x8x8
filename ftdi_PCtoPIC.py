#!/usr/bin/env python3

import sys, math
from pylibftdi import Device



def main ():
	with Device (mode = 't') as dev:
		dev.baudrate = 19200
		i=0

		while i<128 :
			dev.write(chr(0xFF)) 
			i=i+1







#start main
if __name__ == '__main__' :
	main()
