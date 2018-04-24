# -*- coding: utf-8 -*-

from base import Plugin, Application
from telldus import DeviceManager, Device, Sensor
from threading import Thread
import logging

class DummySensor(Sensor):
	'''All devices exported must subclass Device

	Minimal function to reimplement is:
	_command
	localId
	typeString
	methods
	'''
	def _command(self, action, value, success, failure, **kwargs):
		'''This method is called when someone want to control this device

		action is the method id to execute. This could be for instance:
		Device.TURNON or Device.TURNOFF

		value us only used for some actions, for example dim

		This method _must_ call either success or failure
		'''
		logging.debug('Sending command %s to dummy sensor device', action)
		success()

	def localId(self):
		'''Return a unique id number for this device. The id should not be
		globally unique but only unique for this device type.
		'''
		return 1

	def typeString(self):
		'''Return the device type. Only one plugin at a time may export devices using
		the same typestring'''
		return 'testsensor'

class DevPlugin(Plugin):
	'''This is the plugins main entry point and is a singleton
	Manage and load the plugins here
	'''
	def __init__(self):
		# The devicemanager is a globally manager handling all device types
		self.deviceManager = DeviceManager(self.context)

		# Load all devices this plugin handles here. Individual settings for the devices
		# are handled by the devicemanager
		self.deviceManager.addDevice(DummySensor())

		# When all devices has been loaded we need to call finishedLoading() to tell
		# the manager we are finished. This clears old devices and caches
		self.deviceManager.finishedLoading('testsensor')
		Application().registerScheduledTask(fn=self.threadTest, seconds=40, runAtOnce=True)

	def sensorTest(self):
		try:
			logging.warning("Schedule sensor test")
			#If the sensor data returned this method will call automatically
			Sensor.setSensorValue(self, Device.TEMPERATURE, 15, 0.8)
		except Exception as e:
			logging.warning("Could not fetch Sensor data")

	def threadTest(self):
		t = Thread(name='Sensor data', target=self.sensorTest)
		t.daemon = True
		t.start()



