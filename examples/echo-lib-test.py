#!/usr/bin/env python3

from time import sleep
from Bluetin_Echo import Echo

""" Define GPIO pin constants """
TRIGGER_PIN = 17
ECHO_PIN = 18
""" Calibrate sensor with initial speed of sound m/s value """
SPEED_OF_SOUND = 343
""" Initialise Sensor with pins, speed of sound. """
echo = Echo(TRIGGER_PIN, ECHO_PIN, SPEED_OF_SOUND)


def main():
	"""
	Test class properties and methods.
	"""

	print('\n+++++ Properties +++++\n')
	
	"""
	Check that the sensor is ready to operate.
	"""
	print('Sensor ready? {}'.format(echo.is_ready))
	sleep(0.06)
	print('Sensor ready? {}'.format(echo.is_ready))

	"""
	You can adjust the speed of sound to fit environmental conditions.
	"""
	speed = echo.speed
	print('Speed of sound Setting: {}m/s'.format(speed))
	echo.speed = speed

	"""
	This setting is important because it allows a rest period between
	each sensor activation. Accessing the sensor within a rest period
	will result in a Not Ready (2) error code. Reducing the value of
	this setting can cause unstable sensor readings.
	"""
	restTime = echo.rest
	print('Sensor rest time: {}s'.format(restTime))
	echo.rest = restTime

	"""
	The default is fine for this property. This timeout prevents the
	code from getting stuck in an infinite loop in case the sensor
	trigger pin fails to change state.
	"""
	triggerTimeout = echo.trigger_timeout
	print('Sensor trigger timeout: {}s'.format(triggerTimeout))
	echo.trigger_timeout = triggerTimeout

	"""
	Read and update sensor echo timeout.
	The is an alternative way to set a maximum sensor scan distance
	using a time value.
	"""
	echoTimeout = echo.echo_timeout
	print('Sensor echo timeout: {}s'.format(echoTimeout))
	echo.echo_timeout = echoTimeout

	"""
	This property adds a time offset to the max sensor distance
	setting. Adjust this property value to stop the sensor out of range
	error appearing below the maximum distance setting during operation.
	"""
	echoOffset = echo.echo_return_offset
	print('Sensor echo time offset: {}s'.format(echoOffset))
	echo.echo_return_offset = echoOffset
	
	"""
	Read this property to get the error code following a sensor read.
	The error codes are integer values; 0 = Good, 1 = Out of Range and
	2 = Not Ready.
	"""
	errorCode = echo.error_code
	print('Error code from last sensor read: {}'.format(errorCode))

	"""
	The default sensor scan distance is set to 3m. The following property
	will allow an alternate max scan distance setting. Any sensor echos
	that fall outside the set distance will cause an out of range error.
	Units mm, cm, m and inch are supported.
	You can tune the sensor to match the max distance setting using the
	echo_return_offset property.
	"""
	echo.max_distance(30, 'cm')

	"""
	This property sets the default measuring unit, which works with
	the new send and samples methods. Set this property once with your 
	prefered unit of measure. Then use the send method to return sensor
	results in that unit you set. Class default is cm on initialisation.
	"""
	defaultUnit = echo.default_unit
	print('Current Unit Setting: {}'.format(defaultUnit))
	echo.default_unit = defaultUnit
	
	"""
	Test using each unit of measure.
	"""
	print('\n+++++ Single sample sensor reads. +++++\n')
	sleep(0.06)
	averageOf = 1
	result = echo.read('mm', averageOf)
	print('{:.2f} mm, Error: {}'.format(result, echo.error_code))
	sleep(0.06)
	result = echo.read('cm', averageOf)
	print('{:.2f} cm, Error: {}'.format(result, echo.error_code))
	sleep(0.06)
	result = echo.read('m', averageOf)
	print('{:.2f} m, Error: {}'.format(result, echo.error_code))
	sleep(0.06)
	result = echo.read('inch', averageOf)
	print('{:.2f} inch, Error: {}'.format(result, echo.error_code))

	"""
	Then, get an average of multiple reads.
	"""
	print('\n+++++ Return an average of multiple sensor reads. +++++\n')
	sleep(0.06)
	averageOf = 10
	result = echo.read('mm', averageOf)
	print('Average: {:.2f} mm'.format(result))
	sleep(0.06)
	result = echo.read('cm', averageOf)
	print('Average: {:.2f} cm'.format(result))
	sleep(0.06)
	result = echo.read('m', averageOf)
	print('Average: {:.2f} m'.format(result))
	sleep(0.06)
	result = echo.read('inch', averageOf)
	print('Average: {:.2f} inch'.format(result))

	"""
	Get a single sensor read using the default unit of measure.
	Check error codes after each sensor reading to monitor operation
	success.
	"""
	print('\n+++++ Single sensor read using the default unit of measure. +++++\n')
	sleep(0.06)
	echo.default_unit = 'm'
	result = echo.send()
	print('{:.2f} m, Error: {}'.format(result, echo.error_code))

	"""
	Get an average value from multiple sensor readings. Returns an average of
	only the good sensor reads. The average value is returned with
	the number of samples used to make the average sum calculation.
	"""
	print('\n+++++ Return an average from multiple sensor reads. +++++')
	print('+++++ Returns two values; average and good samples. +++++\n')
	sleep(0.06)
	echo.default_unit = 'm'
	result, samples = echo.samples(10)
	print('Average: {:.2f} m, From {} good samples'.format(result, samples))

	""" Reset GPIO Pins. """
	echo.stop()


if __name__ == "__main__":
	main()
