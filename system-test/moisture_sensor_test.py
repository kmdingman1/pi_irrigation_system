import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)

# Pin assignments for the sensors
sensors = {
    1: 17,  # Sensor 1 is connected to GPIO 17
    2: 27,  # Sensor 2 is connected to GPIO 27
    3: 23,  # Sensor 3 is connected to GPIO 23
    4: 24   # Sensor 4 is connected to GPIO 24
}

# Set up each GPIO pin as an input
for sensor, pin in sensors.items():
    GPIO.setup(pin, GPIO.IN)

# Function to read the sensor values
def read_sensors():
    for sensor, pin in sensors.items():
        if GPIO.input(pin):  # If digital output is HIGH, soil is dry
            print(f"Sensor {sensor}: Dry!")
        else:  # If digital output is LOW, soil is wet
            print(f"Sensor {sensor}: Wet!")

try:
    while True:
        print("Checking moisture sensors...")
        read_sensors()  # Check the sensors
        time.sleep(2)   # Wait for 2 seconds before checking again
except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    GPIO.cleanup()  # Reset GPIO settings when exiting
