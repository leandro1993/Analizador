
class Fotometro():
	def __init__(self, arduino):
		self.arduino = arduino
		
	def medir_absorbancia(self):
		self.arduino.write('d')
		sleep(1)
		for i in range(8):
			c  = self.arduino.read()
			if c == '\r' or c == '\n':
				if A != '':

					Decoder.append(int(A))
					print A
				break
			A+=c
		self.arduino.reset_input_buffer()
		#sleep(1)
		return A

		
