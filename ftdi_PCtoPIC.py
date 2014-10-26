#!/usr/bin/env python3

import sys, math, time
from pylibftdi import Device


def main ():
	with Device (mode = 't') as dev:
		dev.baudrate = 19200
	
		boucle=0

		while boucle<7 :

			i=0

			while i<64 :
				dev.write(chr(0x00)) 
				dev.write(chr(0xFF)) 					
				i=i+1

			time.sleep(1.0) 

			i=0

			while i<64 :
		 		dev.write(chr(0xFF))
		 		dev.write(chr(0x00))
		 		i=i+1

			time.sleep(1.0) 
			
			boucle=boucle+1

#start main
if __name__ == '__main__' :
	main()
