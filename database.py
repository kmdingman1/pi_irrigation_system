import sqlite3
from datetime import datetime
from config import DATABASE_PATH

class DatabaseHandler:
    def __init__(self):
        self.init_db()

    def init_db(self):
        """Initialize the database and create tables if they don't exist"""
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS watering_history
                        (plant_id INTEGER,
                         timestamp DATETIME,
                         moisture_level TEXT)''')
            conn.commit()

    def log_watering(self, plant_id, moisture_level):
        """Log a watering event"""
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO watering_history VALUES (?, ?, ?)",
                     (plant_id, datetime.now(), moisture_level))
            conn.commit()

    def get_last_watering(self, plant_id):
        """Get the last watering event for a specific plant"""
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute("""SELECT timestamp, moisture_level 
                        FROM watering_history 
                        WHERE plant_id = ? 
                        ORDER BY timestamp DESC LIMIT 1""",
                     (plant_id,))
            result = c.fetchone()
            return result if result else (None, None)

    def get_watering_history(self, plant_id, limit=10):
        """Get recent watering history for a specific plant"""
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute("""SELECT timestamp, moisture_level 
                        FROM watering_history 
                        WHERE plant_id = ? 
                        ORDER BY timestamp DESC LIMIT ?""",
                     (plant_id, limit))
            return c.fetchall()