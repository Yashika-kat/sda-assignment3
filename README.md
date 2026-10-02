# E-Commerce Data Streaming Pipeline – Assignment 3

## Project Overview

This project implements an e-commerce data streaming pipeline using **Apache Kafka, Python, MongoDB Atlas, and Streamlit**.

The system takes e-commerce data from CSV files, streams it through Kafka topics, consumes the data using a Python Kafka consumer, stores it in MongoDB Atlas, and visualizes the data through an interactive Streamlit dashboard.

## Architecture
CSV Sample Data
      ↓
Kafka Producer
      ↓
Apache Kafka Topics
      ↓
Kafka Consumer
      ↓
MongoDB Atlas
      ↓
Streamlit Dashboard

Technologies Used
Python
Apache Kafka
MongoDB Atlas
PyMongo
Streamlit
Pandas
Plotly
Docker
Git & GitHub


Kafka Topics

The project uses four Kafka topics:

orders
inventory
payments
deliveries


Project Structure
sda-assignment3/
│
├── consumer.py
├── producer.py
├── dashboard.py
├── .gitignore
│
└── sample_data/
    ├── orders.csv
    ├── inventory.csv
    ├── payments.csv
    └── deliveries.csv

Data Flow
Sample e-commerce data is stored in CSV files.
producer.py reads the CSV files and publishes records to Kafka topics.
consumer.py consumes the Kafka messages.
The consumed records are stored in MongoDB Atlas.
dashboard.py retrieves the data from MongoDB Atlas.
Streamlit and Plotly are used to create an interactive analytics dashboard.

Dashboard Features

The Streamlit dashboard provides:

Total Orders
Total Revenue
Units Ordered
Successful Payments
Orders by City
Order Status Distribution
Revenue by Product Category
Payment Method Analysis
Inventory Status
Delivery Status
Recent Orders

How to Run
1. Start Kafka

Make sure the Kafka Docker container is running.

2. Send Data to Kafka
python3 producer.py

3. Consume Data into MongoDB
python3 consumer.py

4. Launch the Dashboard
streamlit run dashboard.py

The dashboard will open in the browser.

Database

MongoDB Atlas is used to store the processed Kafka data.

Database:

sda_assignment3

Collections:

orders
inventory
payments
deliveries

Security

MongoDB credentials are stored in a local .env file and are excluded from Git using .gitignore.

Credentials should never be committed to the repository.

Conclusion

This project demonstrates an end-to-end e-commerce data pipeline integrating streaming, database storage, and interactive data visualization using Kafka, MongoDB Atlas, Python, and Streamlit.
