try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name='Developer Sensor Plugin',
    version='1.0',
    author='Balaji1',
    author_email='balaji.career1@gmail.com',
    color='#2c3e50',
    description='Dummy sensor plugin for easy to test developers',
    long_description='This sensor plugin is used for developer use.',
    packages=['sensorplugin'],
    package_dir = {'':'src'},
	entry_points={ \
		'telldus.startup': ['s = sensorplugin:SensorPlugin [cREQ]']
	},
	extras_require = dict(cREQ = 'Base>=0.1\nTelldus>=0.1'),
)