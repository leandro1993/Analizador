""" Clase de Tests """

test0 = Test('GLU', 22 , 6000, 3900)
test1 = Test('ALB', 38 , 8000, 4900)
test2 = Test('TSH', 37 , 3000, 6900)
test3 = Test('LDH', 54 , 3500, 4400)
test4 = Test('HDL', 111 , 6000, 3900)
test5 = Test('PROT', 19 , 6000, 3900)
test6 = Test('LIP', 62 , 6000, 3900)

test_inciales = [test0, test1, test2, test3, test4, test5, test6]

class Test:
	def __init__(nombre, reactivoNum, volM, volR):
		self.Nombre = nombre
		self.reactivo = reactivoNum
		self.volumenM = volM
		self.volumenR = volR
	def __str__(self):
		 return "Test: "+ self.Nombre + "/n"
		 + "ID Reactivo: "+ self.reactivo \
		 +"Volumen de muestra requerido: "+ self.volumenM + "/n" \
		 +"Volumen de reactivo requerido "+ self.volumenR
		

