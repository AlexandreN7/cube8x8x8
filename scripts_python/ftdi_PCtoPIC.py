#!/usr/bin/env python3

import sys, math
from time import sleep
from pylibftdi import Device


with Device (mode = 't') as dev:
	dev.baudrate = 115200
	dev.write('test')
		
	