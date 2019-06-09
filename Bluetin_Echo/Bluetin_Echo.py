# Copyright (c) 2018 Mark A Heywood
# Author: Mark A Heywood
# https://www.bluetin.io/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Python 2 & 3 print function compatibility
from __future__ import print_function

from time import time
from time import monotonic
from time import sleep
import RPi.GPIO as GPIO

GOOD = 0
OUT_OF_RANGE = 1
NOT_READY = 2

class Echo(object):
    # Use over 50ms measurement cycle. 
    def __init__(self, trigger_pin, echo_pin, mPerSecond = 343):
        self._trigger_pin = trigger_pin # Trigger Pin
        self._echo_pin = echo_pin # Echo Pin

        self._mPerSecond = mPerSecond
        self._sensor_rest = 0.06 # Sensor rest time between reads
        self._last_read_time = 0
        self._last_read = 0
        self._maxScanDist = 0
        self._defaultUnit = 'cm'
        self._triggerTimeout = 0.06 # Trigger Timeout
        """ Set default maximum scan distance (3m) """
        self._maxDistanceTime = (1 / mPerSecond) * 6
        self._maxDistTimeOffset = 0.00067
        self._errorCode = 0

        # Configure GPIO Pins
        try:
            # Use Broadcom (BCM) pin numbering for the GPIO pins.
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self._trigger_pin, GPIO.OUT)
            GPIO.setup(self._echo_pin, GPIO.IN)      
            # Trigger 10us pulse for initial sensor cycling.
            GPIO.output(self._trigger_pin, False)
            sleep(0.5)
            GPIO.output(self._trigger_pin, True)
            sleep(0.00001)
            GPIO.output(self._trigger_pin, False)
        except Exception as e:
            print(e)

        self._last_read_time = monotonic()

    """
    For one shot distance measuring, first set the prefered units of
    measure (default = cm). Distance measurement will return zero
    if the sensor is not ready or timeout occurred.
    """
    def send(self):
        echoTime = self._read()
        return self._valueToUnit(echoTime, self._defaultUnit)

    """
    This method returns an average from multiple sensor readings.
    The samples parameter allows you to choose how many sensor readings
    you want in the average sum. Failed sensor readings are excluded, and the
    number of successful sensor readings is returned as the second parameter. 
    """
    def samples(self, samples = 10):
        # Take more than one sensor reads to get an average result.
        samplesTotal = 0
        goodSamples = 0
        if samples > 0:
            for sample in range(0, samples):
                echoResult = self._read()
                if echoResult > 0:
                    samplesTotal = samplesTotal + echoResult
                    goodSamples = goodSamples + 1
                    
                sleep(self._sensor_rest) # Rest the sensor

            if goodSamples > 0:
                # Return the average of all the samples made.
                return  self._valueToUnit((samplesTotal / goodSamples), self._defaultUnit), goodSamples
            else:
                return 0, 0
        else:
            return 0, 0
            
    """
    You use this method for either one-shot distance measuring, or to 
    get an average from multiple distance measurements.
    Pass in parameters to change units of measure and number of measuring
    samples to take.
    """
    def read(self, unit = 'cm', samples = 1):
        if samples < 2: # Take one sensor reading
            echoTime = self._read()
            return self._valueToUnit(echoTime, unit)
        
        # Take more than one sensor reads to get an average result.
        samplesTotal = 0
        goodSamples = 0
        if samples > 1:
            for sample in range(0, samples):
                echoResult = self._read()
                if echoResult > 0:
                    samplesTotal = samplesTotal + echoResult
                    goodSamples = goodSamples + 1
                    
                sleep(self._sensor_rest) # Rest the sensor

            if goodSamples > 0:
                # Return the average of all the samples made.
                return  self._valueToUnit((samplesTotal / goodSamples), unit)
            else:
                return 0

    """
    Activate the sensor and return a new echo period.
    """
    def _read(self):
        # Check if enough time has passed before triggering device.
        if (monotonic() - self._last_read_time) > self._sensor_rest:
            # Reset values
            timeout = False
            echoStart = 0.0
            echoStop = 0.0
            # Trigger 10us pulse
            GPIO.output(self._trigger_pin, True)
            sleep(0.00001)
            GPIO.output(self._trigger_pin, False)
            echoTimeout = self._maxDistanceTime + self._maxDistTimeOffset
            self._last_read_time = monotonic()
            # Get most recent time before pin rises.
            while GPIO.input(self._echo_pin) == 0:
                echoStart = monotonic()
                if (monotonic() - self._last_read_time) > self._triggerTimeout:
                    timeout = True
                    break

            # Get most recent time before pin falls.
            while GPIO.input(self._echo_pin) == 1:
                echoStop = monotonic()
                if (monotonic() - self._last_read_time) > echoTimeout:
                    timeout = True
                    break

            if timeout == True:
                # No object was detected
                echoTime = 0
                self._errorCode = OUT_OF_RANGE
            else:
                # Calculate pulse length.
                echoTime = echoStop - echoStart
                self._errorCode = GOOD

        else:
            # Device not rested enough, use last value.
            echoTime = 0
            self._errorCode = NOT_READY
        
        # Return reading
        return echoTime

    """
    Convert echo time to distance unit of measure.
    """
    def _valueToUnit(self, value = 0.0, unit = 'cm'):
        if value > 0:
            if unit == 'mm':
                # return mm
                distance = (value * self._mPerSecond * 1000) / 2
            elif unit == 'cm':
                # return cm
                distance = (value * self._mPerSecond * 100) / 2
            elif unit == 'm':
                # return m
                distance = (value * self._mPerSecond) / 2
            elif unit == 'inch':
                # return inch
                distance = (value * self._mPerSecond * 39.3701) / 2
        else:
            distance = 0
            
        return distance

    
    def stop(self):
        # Reset GPIO settings
        GPIO.cleanup()
        
    """
    Calculate the speed of sound by measuring a known distance with the
    sensor.
    """
    def calibrate(self, dValue = 200, unit = 'mm', samples = 10):
        distance = self.read(unit, samples)
        if unit == 'mm':
            multiplier = 1000
        elif unit == 'cm':
            multiplier = 100
        else: # Must be inch then
            multiplier = 39.3701
            
        self._mPerSecond = ((dValue * 2) / multiplier / self._last_read)
        return self._mPerSecond

    """
    You can set the maximum distance boundary you want to measure. Smaller
    the sensor detection boundary, quicker the sensor operates. If the
    sensor reaches beyond this range setting, the method returns a 0
    measurement and will produce an out of range error code (1).
    Supported scan distance units are: mm, cm, m and inch.
    """
    def max_distance(self, value = 3, unit = 'm'):
        timePerM = 1 / self._mPerSecond
        if value > 0:
            if unit == 'mm':
                self._maxScanDist = value / 1000
                self._maxDistanceTime = self._maxScanDist * timePerM * 2
            elif unit == 'cm':
                self._maxScanDist = value / 100
                self._maxDistanceTime = self._maxScanDist * timePerM * 2
            elif unit == 'm':
                self._maxScanDist = value
                self._maxDistanceTime = self._maxScanDist * timePerM * 2
            elif unit == 'inch':
                self._maxScanDist = (value * 2.54) / 100
                self._maxDistanceTime = self._maxScanDist * timePerM * 2
            else:
                # Bad values passed by user
                pass
            
        else:
            # Bad values passed by user
            pass

    """
    You can poll the sensor to check that the sensor is ready
    to take the next distance measurement. This property either
    returns True or False.
    """
    @property
    def is_ready(self):
        if (monotonic() - self._last_read_time) > self._sensor_rest:
            return True
        else:
            return False
    
    """
    poll to return error code for the last sensor reading.
    0 = Good, 1 = Out of range and 2 = Not ready.
    """
    @property
    def error_code(self):
        return self._errorCode

    """
    You can adjust the speed of sound to suit environmental conditions.
    Integer value in m/s.
    """
    @property
    def speed(self):
        return self._mPerSecond

    
    @speed.setter
    def speed(self, speedOfSound):
        self._mPerSecond = speedOfSound
        if self._maxScanDist > 0:
            self.max_distance(self._maxScanDist, 'm')
        else:
            self._maxDistanceTime = (1 / self._mPerSecond) * 6

    """
    The sensor hardware needs a rest period between each trigger
    operations. If the rest period is too short, subsequent readings
    may become unstable.
    """
    @property
    def rest(self):
        return self._sensor_rest

    
    @rest.setter
    def rest(self, sDelay):
        self._sensor_rest = sDelay

    """
    This property exists just in case. This timeout feature prevents
    an infinite program loop in case the sensor trigger pin does not
    change state, or the program missed the state change.
    """
    @property
    def trigger_timeout(self):
        return self._triggerTimeout

        
    @trigger_timeout.setter
    def trigger_timeout(self, timeout):
        self._triggerTimeout = timeout

    """
    You can use a time value to set maximum echo return time out.
    Using this property will overwrite the max distance setting.
    The program will stop listening for a return echo if this timeout
    is reached first.
    """
    @property
    def echo_timeout(self):
        return self._maxDistanceTime

        
    @echo_timeout.setter
    def echo_timeout(self, timeout):
        self._maxDistanceTime = timeout
    
    """
    This offset adds a bit of time to the Max distance setting time.
    Add a bit more time to the offset value if the sensor goes out
    of range before the max distance setting is reached.
    The default value should be close to where it needs to be.

    """
    @property
    def echo_return_offset(self):
        return self._maxDistTimeOffset


    @echo_return_offset.setter
    def echo_return_offset(self, value = 0.00067):
        self._maxDistTimeOffset = value

    """
    You can set the default units of measure for the send() and
    samples() methods. On class initialisation, cm is the default
    setting.
    """
    @property
    def default_unit(self):
        return self._defaultUnit

    
    @default_unit.setter
    def default_unit(self, unit):
        unitPass = False
        if unit == 'mm':
            unitPass = True
        elif unit == 'cm':
            unitPass = True
        elif unit == 'm':
            unitPass = True
        elif unit == 'inch':
            unitPass = True

        if unitPass == True:
            self._defaultUnit = unit
        else:
            raise RuntimeError("Incorrect Unit for Default Unit")
