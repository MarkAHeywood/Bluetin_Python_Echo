Ultrasonic HC-SR04 Sensor Python Library for Raspberry Pi GPIO
==============================================================

This sensor uses sound waves to provide a means to measure the 
distance between the sensor and an object. It is not the most 
accurate distance sensor available, but many projects do not 
need pinpoint accuracy. After a quick look at Banggood website, 
you can get five HC-SR04 sensors for 5.07 GBP (6.86 USD). And 
while the sensor is not the most compact, its low price means 
a robot vehicle can have a full sensor kit fitted very cheaply.

You can find the article here for more details:

`Article <https://www.bluetin.io/sensors/python-library-ultrasonic-hc-sr04>`__.

Example Code
------------

Simplest Program for Distance Measuring:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # Import necessary libraries.
    from Bluetin_Echo import Echo
 
    # Define GPIO pin constants.
    TRIGGER_PIN = 16
    ECHO_PIN = 12
    # Initialise Sensor with pins, speed of sound.
    speed_of_sound = 315
    echo = Echo(TRIGGER_PIN, ECHO_PIN, speed_of_sound)
    # Measure Distance 5 times, return average.
    samples = 5
    result = echo.read('cm', samples)
    # Print result.
    print(result, 'cm')
    # Reset GPIO Pins.
    echo.stop()

Example for Taking Multiple Distance Measurements:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    """File: echo_loop.py"""
    # Import necessary libraries.
    from Bluetin_Echo import Echo
 
    # Define GPIO pin constants.
    TRIGGER_PIN = 16
    ECHO_PIN = 12
    # Initialise Sensor with pins, speed of sound.
    speed_of_sound = 315
    echo = Echo(TRIGGER_PIN, ECHO_PIN, speed_of_sound)
    # Measure Distance 5 times, return average.
    samples = 5
    # Take multiple measurements.
    for counter in range(0, 10):
        result = echo.read('cm', samples)
        # Print result.
        print(result, 'cm')

    # Reset GPIO Pins.
    echo.stop()

Loop Through Multiple Sensors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    """File: echo_multi_sensor.py"""
    # Import necessary libraries.
    from time import sleep
 
    from Bluetin_Echo import Echo
 
    # Define pin constants
    TRIGGER_PIN_1 = 16
    ECHO_PIN_1 = 12
    TRIGGER_PIN_2 = 26
    ECHO_PIN_2 = 19
 
    # Initialise two sensors.
    echo = [Echo(TRIGGER_PIN_1, ECHO_PIN_1)
            , Echo(TRIGGER_PIN_2, ECHO_PIN_2)]
 
    def main():
        sleep(0.1)
        for counter in range(1, 6):
            for counter2 in range(0, len(echo)):
                result = echo[counter2].read('cm', 3)
                print('Sensor {} - {} cm'.format(counter2, round(result,2)))
 
        echo[0].stop()
 
    if __name__ == '__main__':
        main()

