import L6470_Reg as LReg

class L6470:
                
                def __init__(self,Pin_RST,Pin_CE):
                                self.chipSelect = Pin_CE
                                self.RST = Pin_RST
                                

                                self.spi = spidev.SpiDev()
                                self.initSPI()

                                self.initGPIOState()
                                
                                if (self.getParam(LReg.CONFIG) == 0x2e88):
                                                print "Conexion exitosa"
                                                self.setParam(LReg.CONFIG, CONFIG_PWM_DIV_1 |
                                                                LReg.CONFIG_PWM_MUL_2 |
                                                                LReg.CONFIG_SR_180V_us |
                                                                LReg.CONFIG_OC_SD_ENABLE |
                                                                LReg.CONFIG_VS_COMP_DISABLE |
                                                                LReg.CONFIG_SW_USER |
                                                                LReg.CONFIG_INT_16MHZ)

                                else:
                                                print "Error de coneccion SPI"
                                                print self.getParam(LReg.CONFIG)
                                
                def initGPIOState(self):
                                gpio.setmode(gpio.BCM)
                                gpio.setwarnings(False)
                                gpio.setup(self.chipSelect, gpio.OUT)
                                gpio.output(self.chipSelect, gpio.HIGH)
                                gpio.setup(self.RST, gpio.OUT)

                                
                                
                                gpio.output(self.RST, gpio.LOW)
                                sleep(.1)
                                gpio.output(self.RST, gpio.HIGH)    
                                sleep(.1)
                                
                
                def initSPI(self):
                                #spi = spidev.SpiDev()
                                self.spi.open(0,1)
                                self.spi.max_speed_hz = 100000
                                self.spi.bits_per_word = 8
                                self.spi.loop = False
                                self.spi.mode = 3
                def BUSY(self):
                                gpio.wait_for_edge(self.BUSY, gpio.RISING)


                                

                def isBusy(self):
                                status = self.getStatus()
                                return (not ((status >> 1) & 0b1))
                    
                def waitMoveFinish(self):
                                status = 1
                                while status:
                                                status = self.getStatus()
##                                                print self.getPosition()
                                                status = not((status >> 1) & 0b1)

                def setMicroSteps(self, microSteps):
                                self.free()
                                stepVal = 0

                                for stepVal in range(0, 8):
                                    if microSteps == 1:
                                                break
                                    microSteps = microSteps >> 1;
                    
                                self.setParam(LReg.STEP_MODE, (0x00 | stepVal | LReg.SYNC_SEL_1))

                def setThresholdSpeed(self, thresholdSpeed):
                                if thresholdSpeed == 0:
                                    self.setParam(LReg.FS_SPD, 0x3ff)
                                else:
                                    self.setParam(LReg.FS_SPD, self.fsCalc(thresholdSpeed))
                                    
                def setCurrent(self, hold, run, acc, dec):
                                self.setParam(LReg.KVAL_RUN, run)
                                self.setParam(LReg.KVAL_ACC, acc)
                                self.setParam(LReg.KVAL_DEC, dec)
                                self.setParam(LReg.KVAL_HOLD, hold)

                def setMaxSpeed(self, speed):
                                self.setParam(LReg.MAX_SPEED, self.maxSpdCalc(speed))

                def setMinSpeed(self, speed):
                                self.setParam(LReg.MIN_SPEED, self.minSpdCalc(speed))

                def setAccel(self, acceleration):
                                accelerationBytes = self.accCalc(acceleration)
                                self.setParam(LReg.ACC, accelerationBytes)

                def setDecel(self, deceleration):
                                decelerationBytes = self.decCalc(deceleration)
                                self.setParam(LReg.DEC, decelerationBytes)

                def getPosition(self):
                                return self.convert(self.getParam(LReg.ABS_POS))
                def getMark(self):
                                return self.convert(self.getParam(LReg.MARK))
                
                def getSpeed(self):
                                return self.getParam(LReg.SPEED)

                def setOverCurrent(self, ma_current):
                                OCValue = math.floor(ma_current/375)
                                if OCValue > 0x0f: OCValue = 0x0f
                                self.setParam((LReg.OCD_TH), OCValue)

                def setStallCurrent(self, ma_current):
                                STHValue = round(math.floor(ma_current/31.25))
                                if(STHValue > 0x80): STHValue = 0x80
                                if(STHValue < 0): STHValue = 9
                                self.setParam((LReg.STALL_TH), STHValue)

                def setLowSpeedOpt(self, enable):
                                self.xfer(LReg.SET_PARAM | LReg.MIN_SPEED[0])
                                if enable: self.param(0x1000, 13)
                                else: self.param(0, 13)

                def run(self, dir, spd):
                                speedVal = self.spdCalc(spd)
                                print speedVal
                                self.xfer(LReg.RUN | dir)
                                if speedVal > 0xfffff: speedVal = 0xfffff
                                self.xfer(int(speedVal) >> 16)
                                self.xfer(int (speedVal) >> 8)
                                self.xfer(speedVal)
                

                def stepClock(self, dir):
                                self.xfer(LReg.STEP_CLOCK | dir)

                def move(self, nStep):
                                dir = 0

                                if nStep >= 0:
                                    dir = LReg.FWD
                                else:
                                    dir = LReg.REV

                                n_stepABS = abs(nStep)

                                self.xfer(LReg.MOVE | dir)
                                if n_stepABS > 0x3fffff: nStep = 0x3fffff
                                self.xfer(n_stepABS >> 16)
                                self.xfer(n_stepABS >> 8)
                                self.xfer(n_stepABS)
                                
                def goTo(self, pos):
                                self.xfer(LReg.GOTO)
                                if pos > 0x3fffff: pos = 0x3fffff
                                self.xfer(pos >> 16)
                                self.xfer(pos >> 8)
                                self.xfer(pos)

                def goToDir(self, dir, pos):
                                self.xfer(LReg.GOTO_DIR)
                                if pos > 0x3fffff: pos = 0x3fffff
                                self.xfer(pos >> 16)
                                self.xfer(pos >> 8)
                                self.xfer(pos)

                def goUntilPress(self, act, dir, spd):
                                self.xfer(LReg.GO_UNTIL | act | dir)
                                if spd > 0x3fffff: spd = 0x3fffff
                                self.xfer(spd >> 16)
                                self.xfer(spd >> 8)
                                self.xfer(spd)

                def goUntilRelease(self, act, dir):
                                self.xfer(LReg.RELEASE_SW | act | dir)

                def goHome(self):
                                self.xfer(LReg.GO_HOME)

                def goMark(self):
                                self.xfer(LReg.GO_MARK)

                def setMark(self, value):

                                if value == 0: value = self.getPosition()
                                self.xfer(LReg.MARK)
                                if value > 0x3fffff: value = 0x3fffff
                                if value < -0x3fffff: value = -0x3fffff

                                self.xfer(value >> 16)
                                self.xfer(value >> 8)
                                self.xfer(value)

                def setAsHome(self):
                                self.xfer(LReg.RESET_POS)
                def reset(self):
                                gpio.output(self.RST, gpio.LOW)
                                sleep(.1)
                                gpio.output(self.RST, gpio.HIGH)    
                                sleep(.1)

                def resetDev(self):
                                self.xfer(LReg.RESET_DEVICE)
                                #if self.boardInUse == 1: self.setParam([0x1A, 16], 0x3608) 

                def softStop(self):
                                self.xfer(LReg.SOFT_STOP)

                def hardStop(self):
                                self.xfer(LReg.HARD_STOP)

                def softFree(self):
                                self.xfer(LReg.SOFT_HIZ)

                def free(self):
                                self.xfer(LReg.HARD_HIZ)

                def getStatus(self):
                                temp = 0;
                                self.xfer(LReg.GET_STATUS)
                                temp = self.xfer(0) << 8
                                temp += self.xfer(0)
                                return temp

                def accCalc(self, stepsPerSecPerSec):
                                temp = float(stepsPerSecPerSec) * 0.137438
                                if temp > 4095.0: return 4095
                                else: return round(temp)

                def decCalc(self, stepsPerSecPerSec):
                                temp = float(stepsPerSecPerSec) * 0.137438
                                if temp > 4095.0: return 4095
                                else: return round(temp)

                def maxSpdCalc(self, stepsPerSec):
                                temp = float(stepsPerSec) * 0.065536
                                if temp > 1023.0: return 1023
                                else: return round(temp)

                def minSpdCalc(self, stepsPerSec):
                                temp = float(stepsPerSec) * 4.1943
                                if temp > 4095.0: return 4095
                                else: return round(temp)

                def fsCalc(self, stepsPerSec):
                                temp = (float(stepsPerSec) * 0.065536) - 0.5
                                if temp > 1023.0: return 1023
                                else: return round(temp)

                def intSpdCalc(self, stepsPerSec):
                                temp = float(stepsPerSec) * 4.1943
                                if temp > 16383.0: return 16383
                                else: return round(temp)

                def spdCalc(self, stepsPerSec):
                                temp = float(stepsPerSec) * 67.106
                                if temp > float(0x000fffff): return 0x000fffff
                                else: return round(temp)

                def param(self, value, bit_len):
                                ret_value = 0

                                byte_len = bit_len/8
                                if (bit_len%8 > 0): byte_len +=1

                                mask = 0xffffffff >> (32 - bit_len)
                                if value > mask:
                                    value = mask

                                if byte_len >= 3.0:
                                    temp = self.xfer(int(value) >> 16)
                                    ret_value |= temp << 16
                                if byte_len >= 2.0:
                                    temp = self.xfer(int(value) >> 8)
                                    ret_value |= temp << 8
                                if byte_len >= 1.0:
                                    temp = self.xfer(value)
                                    ret_value |= temp
       
                                return (ret_value & mask)

                def xfer(self, data):
                                data = (int(data) & 0xff)
                                gpio.output(self.chipSelect, gpio.LOW)
                                response = self.spi.xfer2([data])
                                gpio.output(self.chipSelect, gpio.HIGH)        

                                return response[0]

                def setParam(self, param, value):
                                self.xfer(LReg.SET_PARAM | param[0])
                                return self.paramHandler(param, value)

                def getParam(self, param):
                                self.xfer(LReg.GET_PARAM | param[0])
                                return self.paramHandler(param, 0)

                def convert(self, val):
                                if val > 0x400000/2:
                                    val = val - 0x400000
                                return val

                def paramHandler(self, param, value):
                                return self.param(value, param[1])
                
            

                
