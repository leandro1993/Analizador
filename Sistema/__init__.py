
import serial

#include the spi dev drivers and check if spi is enabled
try:
  import spidev as spidev
except ImportError:
  raise ImportError("Cannot load spidev library")


#include the gpio drivers
try:
  import RPi.GPIO as gpio
except ImportError:
  raise ImportError("Cannot load the Raspberry Pi GPIO drivers")
