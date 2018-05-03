

class Punta:
    def __init__(self):
        self.microsteps= 32
        self.estacion = 'REACTIVO'
        """Inicializacion de motor de movimiento horizontal"""        
        sleep(0.5)
        self.MotorPuntaH = L6470(20,16)
        sleep(0.5)
        """ Configuraciones iniciales """
        self.MotorPuntaH.setMicroSteps(self.microsteps)
        self.MotorPuntaH.setCurrent(40, 100, 100, 100)
        self.MotorPuntaH.setMaxSpeed(200)
        self.MotorPuntaH.setMinSpeed(190)
        self.MotorPuntaH.setOverCurrent(2250)
        self.MotorPuntaH.free()
        self.MotorPuntaH.setParam(LReg.CONFIG,( LReg.CONFIG_PWM_DIV_1 |
                        LReg.CONFIG_PWM_MUL_2 |
                        LReg.CONFIG_SR_180V_us |
                        LReg.CONFIG_OC_SD_ENABLE |
                        LReg.CONFIG_VS_COMP_DISABLE |
                        LReg.CONFIG_SW_USER |
                        LReg.CONFIG_INT_16MHZ))
        
        """Inicializacion de motor de movimiento vertical"""
        sleep(0.5)
        self.MotorPuntaV = L6470(24,23)
        sleep(0.5)
        """ Configuraciones iniciales """
        self.MotorPuntaV.setMicroSteps(self.microsteps)
        self.MotorPuntaV.setCurrent(40, 100, 100, 100)
        self.MotorPuntaV.setMaxSpeed(200)
        self.MotorPuntaV.setMinSpeed(130)
        self.MotorPuntaV.setOverCurrent(2250)
        self.MotorPuntaV.free()
        self.MotorPuntaV.setParam(LReg.CONFIG,( LReg.CONFIG_PWM_DIV_1 |
                        LReg.CONFIG_PWM_MUL_2 |
                        LReg.CONFIG_SR_180V_us |
                        LReg.CONFIG_OC_SD_ENABLE |
                        LReg.CONFIG_VS_COMP_DISABLE |
                        LReg.CONFIG_SW_HARD_STOP |
                        LReg.CONFIG_INT_16MHZ))
        
        """Constante de pines de Raspberry"""
        sleep(1)
        self.PIN_s2H = 21
        self.PIN_s1V = 18
        self.PIN_s2V = 12
        self.PIN_detLiq = 26
        """ configuracion de GPIO como entrada"""        
        gpio.setup(self.PIN_s2H, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.PIN_s1V, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.PIN_s2V, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.PIN_detLiq, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        
        """Posiciones contructivas en termino de pasos en pasos completos"""
        self.posLavado = 212 
        self.posDispensado = 142
        self.descensoMaximo = 70
        
    def incializacion():
        pass
    def homeH(self):
	"""Movimiento horizontal de la punta a la posicion cero vertical"""
        self.homeV()
        sleep(1)
        if gpio.input(self.PIN_s2H):
            print "Esta a la izq"
            direccion = LReg.FWD
        else:
            direccion = LReg.REV
            print "Esta a la derecha"
        self.MotorPuntaH.run(direccion, 150)
        gpio.wait_for_edge(self.PIN_s2H, gpio.BOTH)
        self.MotorPuntaH.softStop()
    def homeV(self):
	"""Movimiento vertical de la punta a la posicion cero vertical"""
        if not gpio.input(self.PIN_s1V):
            print "Ya esta en HOME vertical"
            return
        self.MotorPuntaV.run(LReg.REV, 150)
        gpio.wait_for_edge(self.PIN_s1V, gpio.BOTH)
        self.MotorPuntaV.softStop()
    def moverAEstacionMuestra(self):
	"""Movimiento horizontal de la punta a la estacion muestra"""
        self.homeV()
        sleep(1)
        if not ((self.MotorPuntaH.getStatus() & LReg.STATUS_SW_F) >> 2) and self.estacion == 'MUESTRA' :
            print "Se encuentra en pos Muestras"
            return
        self.MotorPuntaH.goUntilRelease(LReg.ACTION_RESET, LReg.REV) #REVISAR DIRECCIONES HORIZONTALES
        self.MotorPuntaH.waitMoveFinish()
        self.estacion = 'MUESTRA' 
    def moverAEstacionReactivo(self):
	"""Movimiento horizontal de la punta a la estacion reactivo"""
        self.homeV()
        sleep(1)
        if not ((self.MotorPuntaH.getStatus() & LReg.STATUS_SW_F) >> 2) and self.estacion == 'REACTIVO':
            print "Se encuentra en pos Reactivo"
            return
        self.MotorPuntaH.goUntilRelease(LReg.ACTION_RESET, LReg.FWD) #REVISAR DIRECCIONES HORIZONTALES
        self.MotorPuntaH.waitMoveFinish()
        self.estacion = 'REACTIVO'
    def moverAEstacionLavado(self):
	"""Movimiento horizontal de la punta a la estacion de lavado"""
        if self.estacion == 'LAVADO':
            print "Ya se encuentra en lavado"
            return
        self.homeV()
        if not gpio.input(self.PIN_s2H):
            self.homeH()
            #print self.MotorPuntaH.getPosition()
            self.MotorPuntaH.move(-30*self.microsteps)
            self.MotorPuntaH.waitMoveFinish()
            #print self.MotorPuntaH.getPosition()
        elif self.estacion == 'MUESTRA':
            #print "ELSE"
            pos = self.MotorPuntaH.getPosition()
            #print pos
            self.MotorPuntaH.move(abs (pos - (self.posLavado*self.microsteps)))
            self.MotorPuntaH.waitMoveFinish()
        else:
            self.MotorPuntaH.move(70*self.microsteps)
            self.MotorPuntaH.waitMoveFinish()   
        self.estacion = 'LAVADO'       
    def moverAEstacionDispensado(self):
	"""Movimiento horizontal de la punta a la estacion de dispensado"""
        if self.estacion == 'DISPENSADO':
            print "Ya se encuentra en dispensado"
            return
        self.homeV()
        if not (gpio.input(self.PIN_s2H)):
            self.homeH()
            #print self.MotorPuntaH.getPosition()
            self.MotorPuntaH.move(-110*self.microsteps)
            self.MotorPuntaH.waitMoveFinish()
        else:
            pos = self.MotorPuntaH.getPosition()
            self.MotorPuntaH.move(abs (pos - (self.posDispensado*self.microsteps)))
            self.MotorPuntaH.waitMoveFinish()
        self.estacion = 'DISPENSADO'
    def descensoPrimario(self):
	"""Descenso vertical hasta la primera marca en la guia de la punta"""
        self.proteccion(False)
        if gpio.input(self.PIN_s2V):
            self.MotorPuntaV.run(LReg.FWD, 150)
            gpio.wait_for_edge(self.PIN_s2V, gpio.FALLING)
            self.MotorPuntaV.softStop()
        else:
            self.MotorPuntaV.run(LReg.REV, 150)
            gpio.wait_for_edge(self.PIN_s2V, gpio.RISING)
            self.MotorPuntaV.softStop()
    def proteccion(self, estado):
	"""Esta funcion deshabilita y habilita la parada de emergencia 
	del SW asociada a la cubierta de la punta(sV3) al detectar en flanco 
	descendente"""
        self.MotorPuntaV.free()
        if estado:
            self.MotorPuntaV.setParam(LReg.CONFIG,LReg.CONFIG_PWM_DIV_1 \
                                                   | LReg.CONFIG_PWM_MUL_2 \
                                                   |LReg.CONFIG_SR_180V_us \
                                                   |LReg.CONFIG_OC_SD_ENABLE \
                                                   |LReg.CONFIG_VS_COMP_DISABLE \
                                                   |LReg.CONFIG_SW_HARD_STOP \
                                                   |LReg.CONFIG_INT_16MHZ)
            #print self.MotorPuntaV.getParam(LReg.CONFIG)
        else:
            self.MotorPuntaV.setParam(LReg.CONFIG, LReg.CONFIG_PWM_DIV_1 \
                                                    |LReg.CONFIG_PWM_MUL_2 \
                                                    |LReg.CONFIG_SR_180V_us\
                                                    |LReg.CONFIG_OC_SD_ENABLE\
                                                    |LReg.CONFIG_VS_COMP_DISABLE\
                                                    |LReg.CONFIG_SW_USER\
                                                    |LReg.CONFIG_INT_16MHZ)
            #print self.MotorPuntaV.getParam(LReg.CONFIG)
            
    def descensoAdaptado(self):
	"""Descenso vertical hasta tomar liquido"""
##        self.proteccion(False)
        #sleep(0.5)
##        self.MotorPuntaH.setMaxSpeed(80)
        self.MotorPuntaV.move(self.descensoMaximo*self.microsteps)
        #print "Moviendo"
        estado = gpio.wait_for_edge(self.PIN_detLiq, gpio.BOTH,timeout=2000)
        if estado is None:
            print "No hay liquido"
        else:
            self.MotorPuntaV.softStop()
            time.sleep(1)
        self.homeV()
##        self.MotorPuntaV.setMaxSpeed(180)
        self.proteccion(True)
    def ascensoPrimario(self):
        self.MotorPuntaV.run(LReg.REV, 160)
        gpio.wait_for_edge(self.PIN_s2V, gpio.BOTH)
        self.MotorPuntaV.softStop()
        
    def paradaDeEmergencia(self):
        self.MotorPuntaH.free()
        self.MotorPuntaV.free()
