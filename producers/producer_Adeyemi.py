from kafka import KafkaProducer
import json
import time
import random

# Function to create and configure a Kafka producer
def create_producer(brokers):
    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    return producer

# Function to generate simulated traffic data
def generate_traffic_data():
    # Simulate traffic data with random values
    data = {
        "timestamp": int(time.time()),
        "location": {
            "latitude": round(random.uniform(-90, 90), 6),
            "longitude": round(random.uniform(-180, 180), 6)
        },
        "traffic_volume": random.randint(0, 100),  # Simulated traffic volume
        "incident": bool(random.getrandbits(1))    # Randomly generate traffic incidents
    }
    return data

# Function to send data to a Kafka topic
def send_data(producer, topic, data):
    producer.send(topic, value=data)
    producer.flush()
    print(f"Sent data: {data}")

# Main function to run the producer
def run_producer():
    brokers = 'localhost:9092'  # Kafka broker address
    topic = 'traffic_data'      # Kafka topic to send messages to

    # Create a Kafka producer
    producer = create_producer(brokers)

    try:
        while True:
            # Generate traffic data
            data = generate_traffic_data()

            # Send data
            send_data(producer, topic, data)

            # Simulate data streaming every 5 seconds
            time.sleep(5)

    except KeyboardInterrupt:
        print("Producer stopped.")
    finally:
        producer.close()
        print("Kafka producer closed.")

# Run the producer
if __name__ == "__main__":
    run_producer()
