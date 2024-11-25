import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)

# Pin assignments
MOISTURE_SENSORS = {
    1: {'sensor': 17, 'pump': 4},    # Sensor 1 -> GPIO 17, Pump 1 -> GPIO 4
    2: {'sensor': 27, 'pump': 22},   # Sensor 2 -> GPIO 27, Pump 2 -> GPIO 22
    3: {'sensor': 23, 'pump': 6},    # Sensor 3 -> GPIO 23, Pump 3 -> GPIO 6
    4: {'sensor': 24, 'pump': 26}    # Sensor 4 -> GPIO 24, Pump 4 -> GPIO 26
}

# Set up GPIO pins
for station in MOISTURE_SENSORS.values():
    GPIO.setup(station['sensor'], GPIO.IN)
    GPIO.setup(station['pump'], GPIO.OUT)
    GPIO.output(station['pump'], GPIO.LOW)  # Ensure pumps are off initially

# Check moisture leve, activate pump if moisture is dry
# Return true if watering is performed
def check_and_water(station_number, pump_duration=3):

    station = MOISTURE_SENSORS[station_number]
    
    # Check moisture sensor
    if GPIO.input(station['sensor']):  # HIGH --> dry soil
        print(f"Station {station_number}: Dry - Running pump")
        
        # Activate pump
        GPIO.output(station['pump'], GPIO.HIGH)
        time.sleep(pump_duration)
        GPIO.output(station['pump'], GPIO.LOW)
        
        print(f"Station {station_number}: Watering complete")
        return True
    else:
        print(f"Station {station_number}: Wet - No watering needed")
        return False

def main():
    PUMP_DURATION = 3  # Seconds to run pump when soil is dry
    CHECK_INTERVAL = 300  # Seconds between checking moisture (5 minutes)
    
    try:
        while True:
            print("\nChecking all stations...")
            watering_performed = False
            
            # Check each station
            for station_num in MOISTURE_SENSORS:
                watering_performed |= check_and_water(station_num, PUMP_DURATION)
            
            # If any station was watered, wait a bit longer before next check
            if watering_performed:
                print(f"\nWaiting {CHECK_INTERVAL * 2} seconds before next check...")
                time.sleep(CHECK_INTERVAL * 2)
            else:
                print(f"\nWaiting {CHECK_INTERVAL} seconds before next check...")
                time.sleep(CHECK_INTERVAL)
            

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up")

if __name__ == "__main__":
    main()