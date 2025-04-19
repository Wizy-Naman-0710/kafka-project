import sqlite3
import socket
import threading
from kafka import KafkaConsumer, KafkaProducer

conn = sqlite3.connect("lms.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id TEXT,
    resource_url TEXT,
    poster_username TEXT
)
""")

conn.commit()

# Funcn Register Users
def register_user(role, username, password):
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                      (username, password, role))
        conn.commit()
        return "Registration Successful"
    except sqlite3.IntegrityError:
        return "Error: Username already exists!"

# Funcn Login Users
def login_user(username, password):
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", 
                   (username, password))
    result = cursor.fetchone()
    if result:
        return f"Login successful {result[0]}"  # Returns role (student/instructor)
    return "Error: Invalid credentials"

# Funcn upload course resources (fixed SQL injection my removing fstri8ngs and using these param queries)
def upload_course_resources(course_id, resource_url, poster_username):
    try:
        cursor.execute("INSERT INTO courses (course_id, resource_url, poster_username) VALUES (?, ?, ?)", 
                      (course_id, resource_url, poster_username))
        conn.commit()
        return "Resource Added Successfully"
    except Exception as e:
        return f"Error: {str(e)}"

# Func get course resources (fixed SQL injection my removing fstri8ngs and using these param queries)
def get_course_resource(course_id):
    try:
        cursor.execute("SELECT resource_url FROM courses WHERE course_id=?", (course_id,))
        result = cursor.fetchall()
        if not result:
            return "Error: No resources found for this course!"
        resource_urls = "|".join([row[0] for row in result])
        return resource_urls
    except Exception as e:
        return f"Error: {str(e)}"

# Func get all courses
def get_all_courses():
    try:
        cursor.execute("SELECT DISTINCT course_id FROM courses")
        courses = cursor.fetchall()
        if not courses:
            return "No courses available"
        return "|".join([c[0] for c in courses])
    except Exception as e:
        return f"Error: {str(e)}"

consumer = KafkaConsumer(
    'lms-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='lms-group'
)

producer = KafkaProducer(bootstrap_servers='localhost:9092')

print("Kafka consumer is running and listening to 'lms-topic'...")

for message in consumer:
    request = message.value.decode('utf-8')
    parts = request.split()
    
    if parts[0] == "REGISTER":
        role, username, password = parts[1], parts[2], parts[3]
        response = register_user(role, username, password)
    elif parts[0] == "LOGIN":
        username, password = parts[1], parts[2]
        response = login_user(username, password)
    elif parts[0] == "GET_COURSES":
        response = get_all_courses()
    elif parts[0] == "GET_RESOURCES":
        course_id = parts[1]
        response = get_course_resource(course_id)
    elif parts[0] == "UPLOAD_RESOURCE":
        course_id, resource_url, poster_username = parts[1], parts[2], parts[3]
        response = upload_course_resources(course_id, resource_url, poster_username)
    else:
        response = "Invalid request!"
    
    print(f"Processed request: {request} | Response: {response}")

    # Send the response back to lms-responses topic
    producer.send('lms-responses', response.encode('utf-8'))
    producer.flush()  # Ensure the message is sent immediately
    print(f"Response sent to lms-responses: {response}")
