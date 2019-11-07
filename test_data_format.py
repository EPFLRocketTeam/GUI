
from ctypes import *

import math
import Functions
#from Functions.drag import *
#from Functions.bisection import *
#from Functions.Thrust import *
#from Functions.drag_shuriken import *
#from Functions.rocketReader import *
#from Functions.environnementReader import *
from numpy import *
from scipy import interpolate
#from Functions.stdAtmos import *

# Communication with the CAN

import struct

class TPCANMsg(Structure):
	_fields_ = [("DATA", c_ubyte * 8)]

	def test_write(self, data, id_):

		array = [data >> 24, data >> 16, data >> 8, data >> 0, id_, 0, 0, 0]

		for i, elem in enumerate(array):
			self.DATA[i] = c_ubyte(elem)

	def test_read(self):
		data = 0
		for i in range(4):
			data_i = str(self.DATA[i])
			data += int(data_i) * (256**(4-1-i))
		msg_id = str(self.DATA[4])
		print(msg_id)


a = TPCANMsg()
a.test_write(24500, 14)
a.test_read()

