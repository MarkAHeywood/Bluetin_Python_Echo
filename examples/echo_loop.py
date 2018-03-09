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
