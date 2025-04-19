from kafka import KafkaProducer, KafkaConsumer
import uuid
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Unique group_id to avoid consuming old messages
consumer = KafkaConsumer(
    'lms-responses',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    group_id=f'gui-client-{uuid.uuid4()}',
    consumer_timeout_ms=5000  # Timeout if no response within 5 seconds
)

def send_request(message):
    try:
        # Send request to backend
        producer.send('lms-topic', message.encode('utf-8'))
        producer.flush()

        # Wait for a relevant response (simple: just return first one)
        for msg in consumer:
            response = msg.value.decode('utf-8')
            return response
        
        return "Error: No response from backend"
    
    except Exception as e:
        return f"Error: {str(e)}"
