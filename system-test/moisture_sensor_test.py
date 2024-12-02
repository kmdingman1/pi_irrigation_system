import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Sensor GPIO pins
sensors = {
    1: 17,  # Sensor 1 
    2: 27,  # Sensor 2
    3: 23,  # Sensor 3 
    4: 24   # Sensor 4 
}

# Set up GPIO pins as an input
for sensor, pin in sensors.items():
    GPIO.setup(pin, GPIO.IN)

# Read sensor values
def read_sensors():
    for sensor, pin in sensors.items():
        if GPIO.input(pin):  # If digital output is HIGH, soil is dry
            print(f"Sensor {sensor}: Dry!")
        else:  # If digital output is LOW, soil is wet
            print(f"Sensor {sensor}: Wet!")

try:
    while True:
        print("Checking moisture sensors...")
        read_sensors()  # Check sensors
        time.sleep(2)   # Wait for 2 sec before checking again
finally:
    GPIO.cleanup()  
