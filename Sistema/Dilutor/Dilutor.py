class Dilutor:
    def __init__(self, arduino):
        """constantes de control e informacion"""
        self.arduino = arduinoN
        self.microsteps= 32
        self.posicion = 0
        """Inicializacion de motor de carrusel de muestras"""        
        sleep(0.5)
        self.MotorDilutor = L6470(24,23)
        sleep(0.5)
        """ Configuraciones iniciales """
        self.MotorDilutor.setMicroSteps(self.microsteps)
        self.MotorDilutor.setCurrent(40, 90, 90, 90)
        self.MotorDilutor.setMaxSpeed(180)
        self.MotorDilutor.setMinSpeed(170)
        self.MotorDilutor.setOverCurrent(2250)
        self.MotorDilutor.free()
        self.MotorDilutor.setParam(LReg.CONFIG,( LReg.CONFIG_PWM_DIV_1 |
                        LReg.CONFIG_PWM_MUL_2 |
                        LReg.CONFIG_SR_180V_us |
                        LReg.CONFIG_OC_SD_ENABLE |
                        LReg.CONFIG_VS_COMP_DISABLE |
                        LReg.CONFIG_SW_USER |
                        LReg.CONFIG_INT_16MHZ))       
    def home(self):
	"""Movimiento del embolo dilutor a la posicion de menor volumen de liquido en su camara"""
        if ((self.MotorFeeder.getStatus() & LReg.STATUS_SW_F) >> 2):
			self.MotorDilutor.goUntilRelease(LReg.ACTION_RESET,LReg.REV)
			self.MotorDilutor.waitMoveFinish()
			self.MotorDilutor.setAsHome()
			self.posicion = 0
		else:
			print "Ya esta en home"
    def aspirar(self, pasos=32000):
	"""Funcion que aspira cierta cantidad de volumen. La relacion pasos/volumen es 78 pasospormicrolitro"""
        self.MotorDilutor.move(pasos)
        self.MotorDilutor.waitMoveFinish()
        self.posicion = pasos
    def dispensar(self):
        pass
    def ingresoH20(self, pasos):
	"""Accionamiento de bomba de H20 con apertura de la valvula solenoide permitiendo en ingreso de agua a la punta"""
        self.arduino.write(pasos)
        sleep(4)
    def lavado(self):
	"""Accionamiento de bombas ambas bombas con apertura de valvula solenoide direccionando el flujo a la zona de lavado"""
        self.arduino.write('a')
    def paradaDeEmergencia(self):
        self.MotorDilutor.free()
