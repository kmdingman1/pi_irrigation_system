import RPi.GPIO as GPIO
import time

# Set up
GPIO.setmode(GPIO.BCM)

# Pump GPIO pins
PUMP_PINS = [4, 22, 6, 26]

# Set up GPIO pins as outputs
for pin in PUMP_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Ensure pumps are off initially

# Function to test pumps
def run_pump(pump_number, duration):
    pin = PUMP_PINS[pump_number - 1]
    print(f"Running pump {pump_number} on GPIO {pin}")
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin, GPIO.LOW)
    print(f"Pump {pump_number} stopped")
    time.sleep(1)  # Wait 1 sec between activation

try:
    for i, pin in enumerate(PUMP_PINS, 1):
        run_pump(i, 3)  # Run each pump for 3 seconds
    
    print("Test Finished")

finally:
    GPIO.cleanup()  # Clean up GPIO on exit
