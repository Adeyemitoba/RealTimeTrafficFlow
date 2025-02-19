import json
import os
import sqlite3
import logging
import threading
import time
from kafka import KafkaConsumer
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# Specify the GUI backend for matplotlib
import matplotlib
matplotlib.use('TkAgg')

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Kafka Consumer Configuration
topic_name = os.getenv('TRAFFIC_TOPIC', 'traffic_data')
kafka_broker_address = os.getenv('KAFKA_BROKER_ADDRESS', 'localhost:9092')
consumer_group_id = os.getenv('CONSUMER_GROUP_ID', 'traffic_consumer_group')

# SQLite Database Configuration
db_path = os.getenv('SQLITE_DB_FILE_NAME', 'traffic_data.db')

# Data for plotting
data = {
    'times': [],
    'volumes': []
}

# Initialize SQLite Database and create table
def initialize_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS traffic_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            latitude REAL,
            longitude REAL,
            traffic_volume INTEGER,
            incident BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

def update_plot():
    plt.figure()
    plt.ion()  # Turn the interactive mode on
    while True:
        if data['times']:
            plt.clf()  # Clear the current figure
            plt.plot(data['times'], data['volumes'])
            plt.title('Traffic Volume Over Time')
            plt.xlabel('Timestamp')
            plt.ylabel('Volume')
            plt.pause(0.1)  # Pause a bit so that updates are visible
        time.sleep(1)

def consume_messages():
    initialize_db()  # Ensure the database and table are ready
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=[kafka_broker_address],
        auto_offset_reset='earliest',
        group_id=consumer_group_id,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    for message in consumer:
        msg_data = message.value
        logging.info(f"Received message: {msg_data}")
        data['times'].append(msg_data['timestamp'])
        data['volumes'].append(msg_data['traffic_volume'])

if __name__ == "__main__":
    # Start the plot in a separate thread
    plot_thread = threading.Thread(target=update_plot)
    plot_thread.start()

    # Start consuming messages
    consume_messages()