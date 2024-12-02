from flask import Flask, render_template, jsonify, request
import RPi.GPIO as GPIO
import threading
import time
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Pin configurations
MOISTURE_SENSORS = {
    1: {'sensor': 17, 'pump': 4},    # Plant 1
    2: {'sensor': 27, 'pump': 22},   # Plant 2
    3: {'sensor': 23, 'pump': 6},    # Plant 3
    4: {'sensor': 24, 'pump': 26}    # Plant 4
}

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
for station in MOISTURE_SENSORS.values():
    GPIO.setup(station['sensor'], GPIO.IN) # Sensors as input
    GPIO.setup(station['pump'], GPIO.OUT) # Pump as output
    GPIO.output(station['pump'], GPIO.LOW) # Ensure pumps are off

# Database setup for watering history
def init_db():
    conn = sqlite3.connect('irrigation_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS watering_history
                 (plant_id INTEGER, timestamp TEXT, moisture_level TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Log watering events to DB
def log_watering(plant_id, moisture_level):
    conn = sqlite3.connect('irrigation_history.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO watering_history VALUES (?, ?, ?)",
              (plant_id, timestamp, moisture_level))
    conn.commit()
    conn.close()

# Get last watering time for a plant
def get_last_watering(plant_id):
    conn = sqlite3.connect('irrigation_history.db')
    c = conn.cursor()
    c.execute("SELECT timestamp, moisture_level FROM watering_history WHERE plant_id = ? ORDER BY timestamp DESC LIMIT 1",
              (plant_id,))
    result = c.fetchone()
    conn.close()
    return result if result else (None, None)

# Check moisture levels
def check_moisture(plant_id):
    sensor_pin = MOISTURE_SENSORS[plant_id]['sensor']
    return "Dry" if GPIO.input(sensor_pin) else "Wet"

# Water plant
def water_plant(plant_id, duration=4):
    pump_pin = MOISTURE_SENSORS[plant_id]['pump']
    GPIO.output(pump_pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pump_pin, GPIO.LOW)
    return True

# Automated watering system
class AutomatedWatering:
    def __init__(self):
        self.interval = 24  # Default interval is every 24 hours
        self.running = False
        self.thread = None

    # Start automated watering
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.daemon = True
            self.thread.start()

    # Stop automated watering
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    # Change interval
    def set_interval(self, hours):
        self.interval = hours

    # Automated watering loop
    def _run(self):
        while self.running:
            for plant_id in MOISTURE_SENSORS:
                moisture = check_moisture(plant_id)
                if moisture == "Dry":
                    water_plant(plant_id)
                log_watering(plant_id, moisture)
            time.sleep(self.interval * 3600)

# Initialize automated watering system
auto_water = AutomatedWatering()

# Flask route for home page
@app.route('/')
def home():
    plant_status = []
    for plant_id in MOISTURE_SENSORS:
        timestamp, moisture = get_last_watering(plant_id)
        last_watered = timestamp if timestamp else "Never"
        plant_status.append({
            'id': plant_id,
            'moisture': check_moisture(plant_id),
            'last_watered': last_watered
        })
    return render_template('template.html', 
                         plants=plant_status,
                         auto_interval=auto_water.interval)
    
# Check plant moisture
@app.route('/check_plant/<int:plant_id>')
def check_plant(plant_id):
    moisture = check_moisture(plant_id)
    timestamp, _ = get_last_watering(plant_id)
    return jsonify({
        'plant_id': plant_id,
        'moisture': moisture,
        'last_watered': timestamp if timestamp else "Never"
    })

# Water plant
@app.route('/water_plant/<int:plant_id>')
def water_plant_route(plant_id):
    moisture = check_moisture(plant_id)
    water_plant(plant_id)
    log_watering(plant_id, moisture)
    return jsonify({})

# Set watering inteval
@app.route('/set_interval', methods=['POST'])
def set_interval():
    hours = int(request.form['hours'])
    auto_water.set_interval(hours)
    return jsonify({})

# Toggle automated watering
@app.route('/toggle_auto', methods=['POST'])
def toggle_auto():
    action = request.form.get('action')
    if action == 'start':
        auto_water.start()
    elif action == 'stop':
        auto_water.stop()
    return jsonify({})


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup()
