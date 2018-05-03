from L6470 import *
from Punta import *
from Carrusel import *
from Transporte import *
from Dilutor import *
from Test import *

class Sistema:
	def __init__(self):
		arduinoNano = Arduino()
		self.punta = Punta()
		self.dilutor = Dilutor(arduinoNano)
		self.transporte = Transporte(arduinoNano)
		self.carrusel = Carrusel(arduinoNano)
		#self.Pin_sensorH2O = 2135
		#self.Pin_sensorDesecho = 21345
		#gpio.setup(self.Pin_sensorH2O, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        #gpio.setup(self.Pin_sensorDesecho, gpio.IN, pull_up_down=gpio.PUD_DOWN)
		print "Iniciando"
		self.aire_GAP = 500
		self.Codigos = []
	def Lavado_completo(self):
		self.punta.moverAEstacionLavado()
		self.punta.descensoPrimario()
		self.punta.descensoAdaptado()
		#self.dilutor.home()
		self.dilutor.ingresoH2O('b2080')
		self.dilutor.lavado()
		self.punta.homeH()
	def Lavado_externo(self):
		self.punta.moverAEstacionLavado()
		self.punta.descensoPrimario()
		self.punta.descensoAdaptado()
		self.dilutor.lavado()
		self.punta.homeV()
	def mover_punta_a_estacion_muestra(self):
		self.punta.moverAEstacionMuestra()
	def mover_punta_a_estacion_reactivos(self):
		self.punta.moverAEstacionReactivo()
	def mover_punta_a_estacion_dispensado_de_mezcla(self):
		self.punta.moverAEstacionDispensado()
	def mover_punta_a_estacion_lavado(self):
		self.punta.moverAEstacionLavado()
	def mover_carrusel_M(self, pos):
		self.carrusel.irAposicionM(pos)
	def mover_carrusel_R(self, pos):
		self.carrusel.irAposicionR(pos)
	def aspirar_volumen(self, vol):
		self.dilutor.aspirar(vol)
	def dispensar_volumen(self, vol):
		self.dilutor.aspirar(vol)
		self.dilutor.home()
		
	def Procedimiento(self, volumenR = 8000 , volumenM = 8000):
		"""Procedimiento general de tratamiento de las muestras"""
		self.dilutor.aspirar((32000-(volumenR + volumenM + 2*self.aire_GAP)))
		self.Lavado_completo()
		self.dilutor.aspirar(self.aire_GAP)
		self.punta.moverAEstacionMuestra()
		self.punta.descensoPrimario()
		self.punta.descensoAdaptado()
		
		self.dilutor.aspirar(volumenM)
		
		self.Lavado_externo()
		self.dilutor.aspirar(self.aire_GAP)
		
		self.punta.moverAEstacionReactivo()
		self.punta.descensoPrimario()
		self.punta.descensoAdaptado()
		
		self.dilutor.aspirar(volumenR)
		
		self.punta.moverAEstacionDispensado()
		self.punta.descensoPrimario()
		self.punta.descensoAdaptado()
		
		self.dilutor.home()
	def Inicio_dia(self):
		if gpio.input(self.Pin_sensorDesecho):
			print "ERROR - VACIE LA BOTELLA DE DESECHOS"
		if gpio.input(self.Pin_sensorH2O):
			print "ERROR - VACIE LA BOTELLA DE DESECHOS"
		
		self.transporte.vaciarCamino()
		self.transporte.home()
		
		self.Lavado_completo()
		
		self.carrusel.homeR()
		self.carrusel.homeM()
		
	def Demostracion(self):
		self.carrusel.irAposicionR(10)
		self.carrusel.irAposicionM(10)
		
		while not self.transporte.ingresoCubetas(): pass
		
		self.Procedimiento()
		
		self.transporte.moverAEstacionFotometro()
		medicion = self.transporte.realizarMedicion()
		
		self.punta.homeH()
		return medicion
	def Leer_reactivos(self):
		return self.carrusel.leerCodigosR()
	def Rutina(self, posM, test):
		if not self.Codigos:
			self.Codigos = self.Leer_reactivos()
		if test.reactivo in self.Codigos:
			posR = self.Codigos.index(test.reactivo) + 1
		else:
			print "REACTIVO NO ENCONTRADO"
		
		self.carrusel.irAposicionM(posM)
		self.carrusel.irAposicionR(posR)
		
		while not self.transporte.ingresoCubetas(): pass
		
		self.Procedimiento(test.volumenR, test.volumenM)
		
		self.transporte.moverAEstacionFotometro()
		return self.transporte.realizarMedicion()
		

		
		
		
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	def OM_Punta(self, estacion):
		pass
	def OM_Dilutor_aspirar(self, volumen):
		pass
	def OM_Dilutir_dispensar(self, volumen):
		pass
	def OM_Ir_a_posicion_R(self, pos):
		pass
	def OM_Ir_a_posicion_M(self, pos):
		pass
	def Leer_reactivos(self):
		pass
	def Rutina(self, paciente):
		pass

		
		
		
	
