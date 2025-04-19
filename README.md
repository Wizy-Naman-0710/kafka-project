# Kafka Project

This project implements a Kafka-based messaging system for a Learning Management System (LMS). It includes a server that processes various requests, a client that sends messages, and a GUI interface that interacts with the backend.

## Requirements

- [Homebrew](https://brew.sh/) (for macOS)
- Apache Kafka
- Zookeeper

## Installing kafka using homebrew 
```bash 
brew install kafka 
```

## Running kafka and zookeeper 
```bash 
brew services start kafka 
```
```bash 
brew services start zookeeper
```

## Creating the topic required for this project 
```bash 
kafka-topics --create --topic lms-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
```bash 
kafka-topics --create --topic lms-responses --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

## Final Step 
If the topics are created. You are all set to go! 
Now the final step: 
```bash 
python3 server.py
```
```bash 
python3 gui.py
```