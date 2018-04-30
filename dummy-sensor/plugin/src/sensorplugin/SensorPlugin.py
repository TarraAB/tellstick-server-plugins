# -*- coding: utf-8 -*-

import logging
import random

from base import Plugin, Application
from telldus import DeviceManager, Sensor

class DummySensor(Sensor):
	'''All sensors exported must subclass Device or Sensor'''

	@staticmethod
	def localId():
		'''Return a unique id number for this device. The id should not be
		globally unique but only unique for this device type.
		'''
		return 1

	@staticmethod
	def typeString():
		'''Return the device type. Only one plugin at a time may export devices using
		the same typestring'''
		return 'testsensor'

class SensorPlugin(Plugin):
	'''This is the plugins main entry point and is a singleton
	Manage and load the plugins here
	'''
	def __init__(self):
		# The devicemanager is a globally manager handling all device types
		self.deviceManager = DeviceManager(self.context)

		# Load all devices this plugin handles here. Individual settings for the devices
		# are handled by the devicemanager
		self.sensor = DummySensor()
		self.deviceManager.addDevice(self.sensor)

		# When all devices has been loaded we need to call finishedLoading() to tell
		# the manager we are finished. This clears old devices and caches
		self.deviceManager.finishedLoading('testsensor')
		Application().registerScheduledTask(fn=self.sensorTest, seconds=40, runAtOnce=True)

	def sensorTest(self):
		try:
			logging.warning("Update sensor value.")
			value = round(random.uniform(1.0, 100.0),2)
			#If the sensor data returned this method will call automatically
			self.sensor.setSensorValue(Sensor.TEMPERATURE, value, Sensor.SCALE_TEMPERATURE_CELCIUS)
		except Exception as _error:
			logging.warning("Could not fetch Sensor data")
