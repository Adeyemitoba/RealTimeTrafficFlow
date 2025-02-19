# Real-Time Traffic Data Visualization

## Project Overview
This project is dedicated to consuming and visualizing real-time traffic data from a Kafka topic. It showcases traffic volumes over time through a dynamic line chart, providing insights into traffic patterns that could inform traffic management strategies.

## Features
- **Real-Time Kafka Data Consumption**: Streams traffic data efficiently from a Kafka topic.
- **Dynamic Line Chart Visualization**: Updates a line chart in real-time to reflect traffic volumes.
- **SQLite Database Integration**: Optionally stores incoming traffic data for historical analysis.


## Installation

### Install Dependencies
Ensure Python is installed, then run:
```bash
pip install kafka-python matplotlib sqlite3 python-dotenv

## Setup Instructions

## Clone the Repository

git clone https://github.com/don4ye/SentimentStream.git
cd SentimentStream

## Set Up Virtual Environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

## Start Kafka & Zookeeper
zookeeper-server-start.sh config/zookeeper.properties  
kafka-server-start.sh config/server.properties  

## Run the Producer
python -m producers.producer_Adeyemi

## Run the Consumer
python -m consumers.consumer_Adeyemi