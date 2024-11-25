import RPi.GPIO as GPIO
import time
from config import MOISTURE_SENSORS

class GPIOHandler:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self._setup_pins()

    def _setup_pins(self):
        """Initialize all GPIO pins"""
        for station in MOISTURE_SENSORS.values():
            GPIO.setup(station['sensor'], GPIO.IN)
            GPIO.setup(station['pump'], GPIO.OUT)
            GPIO.output(station['pump'], GPIO.LOW)

    def check_moisture(self, plant_id):
        """Check moisture level for a specific plant"""
        if plant_id not in MOISTURE_SENSORS:
            raise ValueError(f"Invalid plant ID: {plant_id}")
        
        sensor_pin = MOISTURE_SENSORS[plant_id]['sensor']
        return "Dry" if GPIO.input(sensor_pin) else "Wet"

    def water_plant(self, plant_id, duration):
        """Water a specific plant for the given duration"""
        if plant_id not in MOISTURE_SENSORS:
            raise ValueError(f"Invalid plant ID: {plant_id}")
        
        pump_pin = MOISTURE_SENSORS[plant_id]['pump']
        try:
            GPIO.output(pump_pin, GPIO.HIGH)
            time.sleep(duration)
            GPIO.output(pump_pin, GPIO.LOW)
            return True
        except Exception as e:
            print(f"Unable to water plant {plant_id}: {str(e)}")
            return False

    def cleanup(self):
        """Clean up GPIO pins"""
        GPIO.cleanup()