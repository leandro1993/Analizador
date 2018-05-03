from Fotometro import *
class Transporte:
    def __init__(self, arduino):
	"""Inicializacion de motor del camino principal"""
        self.MotorCamino = L6470(21,16)
        sleep(0.5)
        """ Configuraciones iniciales"""
        self.MotorCamino.setMicroSteps(32)
        self.MotorCamino.setCurrent(40, 120, 120, 120)
        self.MotorCamino.setMaxSpeed(120)
        self.MotorCamino.setMinSpeed(100)
        self.MotorCamino.setOverCurrent(2250)
        self.MotorCamino.free()
        self.MotorCamino.setParam(LReg.CONFIG,( LReg.CONFIG_PWM_DIV_1 |
                        LReg.CONFIG_PWM_MUL_2 |
                        LReg.CONFIG_SR_180V_us |
                        LReg.CONFIG_OC_SD_ENABLE |
                        LReg.CONFIG_VS_COMP_DISABLE |
                        LReg.CONFIG_SW_USER |
                        LReg.CONFIG_INT_16MHZ))
        """Inicializacion de motor del camino principal"""
        sleep(0.5)
        self.MotorFeeder = L6470(24,23)
        sleep(0.5)
        """ Configuraciones iniciales"""
        self.MotorFeeder.setMicroSteps(1)
        self.MotorFeeder.setCurrent(20, 90, 90, 90)
        self.MotorFeeder.setMaxSpeed(100)
        self.MotorFeeder.setMinSpeed(80)
        self.MotorFeeder.setOverCurrent(2250)
        self.MotorFedeer.free()
        self.MotorFeeder.setParam(LReg.CONFIG,( LReg.CONFIG_PWM_DIV_1 |
                        LReg.CONFIG_PWM_MUL_2 |
                        LReg.CONFIG_SR_180V_us |
                        LReg.CONFIG_OC_SD_ENABLE |
                        LReg.CONFIG_VS_COMP_DISABLE |
                        LReg.CONFIG_SW_USER |
                        LReg.CONFIG_INT_16MHZ))
        """Constante de pines de Raspberry"""
        self.detBorde = 12
        """ configuracion de GPIO como entrada"""
        gpio.setup(self.detBorde, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        """ Declaracion de constantes """
        self.numCubetas = 0
        """Creacion del objeto fotometro"""
        fotometro = Fotometro(arduino)
        
    def home(self):
	"""Movimiento del alimentador de cubetas hacia la posicion cero correspondiente a la maxima capacidad de ingresar cubetas"""
        if ((self.MotorFeeder.getStatus() & LReg.STATUS_SW_F) >> 2):
            self.MotorFeeder.goUntilRelease(LReg.ACTION_RESET, LReg.FWD)
            self.MotorFeeder.waitMoveFinish()
    def vaciarCamino(self):
	"""Accionamiento del motor del camino principal para expulsar todas las cubetas"""
        self.MotorCamino.move(-83250)
        self.MotorCamino.waitMoveFinish()
    def ingresoCubetas(self):
	"""Ingreso de la primera cubeta al camino principal"""
        self.MotorFeeder.free()
        self.MotorCamino.free()
        self.MotorFeeder.move(-240)
        self.MotorFeeder.waitMoveFinish()
        print self.MotorFeeder.getPosition()
        self.MotorCamino.move(1100)
        self.MotorCamino.waitMoveFinish()
        while not ((self.MotorCamino.getStatus() & LReg.STATUS_SW_F) >> 2):
            if gpio.input(self.detBorde):
                return True
            time.sleep(1)
            self.MotorFeeder.move(-235)
            self.MotorFeeder.waitMoveFinish()
            self.MotorFeeder.move(10)
            self.MotorFeeder.waitMoveFinish()
            self.MotorCamino.move(1100)
            self.MotorCamino.waitMoveFinish()
        self.MotorCamino.free()
        self.MotorCamino.move(-1100)
        self.MotorCamino.waitMoveFinish()
        self.MotorCamino.move(-3640)
        print "Hay cubeta"
        self.numCubetas+=1
        return False
		
	def moverAEstacionFotometro(self):
		pass
    def paradaDeEmergencia(self):
        self.MotorCamino.free()
        self.MotorFeeder.free()

            
