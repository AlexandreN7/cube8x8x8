#!/usr/bin/env python3

import sys, math
from time import sleep
from pylibftdi import Device


def main ():
	with Device (mode = 't') as dev:
		dev.baudrate = 19200
	
		boucle=0

		while boucle<256 :

			i=0

			while i<128 :
				dev.write(chr(0x00)) 
				dev.write(chr(boucle)) 					
				i=i+1

			sleep(0.001)

			i=0

			while i<256 :
		 		dev.write(chr(0x00))
		 		i=i+1

			sleep(0.001)			 

			i=0

			while i<128 :
		 		dev.write(chr(boucle))
		 		dev.write(chr(0x00))
		 		i=i+1

			sleep(0.001)

			i=0

			while i<256 :
		 		dev.write(chr(0x00))
		 		i=i+1

			sleep(0.001)			

			i=0

			while i<256 :
		 		dev.write(chr(boucle))

		 		i=i+1

			sleep(0.001)

			i=0

			while i<256 :
		 		dev.write(chr(0x00))
		 		i=i+1

			sleep(0.001)						 

			boucle=boucle+1

#start main
if __name__ == '__main__' :
	main()
