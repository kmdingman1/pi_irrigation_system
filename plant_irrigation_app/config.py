# Pin configurations
MOISTURE_SENSORS = {
    1: {'sensor': 17, 'pump': 4},    # Plant 1
    2: {'sensor': 27, 'pump': 22},   # Plant 2
    3: {'sensor': 23, 'pump': 6},    # Plant 3
    4: {'sensor': 24, 'pump': 26}    # Plant 4
}

# Database configuration
DATABASE_PATH = 'irrigation_history.db'

# Default watering settings
DEFAULT_PUMP_DURATION = 3  # seconds
DEFAULT_CHECK_INTERVAL = 24  # hours

# Flask configuration
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
