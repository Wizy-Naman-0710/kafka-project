import sqlite3
import socket
import threading

# ✅ Initialize Database
conn = sqlite3.connect("lms.db", check_same_thread=False)
cursor = conn.cursor()

# ✅ Create Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")
conn.commit()

# ✅ Function to Register Users
def register_user(role, username, password):
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        return "Registration successful!"
    except sqlite3.IntegrityError:
        return "Error: Username already exists!"

# ✅ Function to Login Users
def login_user(username, password):
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    if result:
        return f"Login successful {result[0]}"  # Returns role (student/instructor)
    return "Error: Invalid credentials"

# ✅ Function to Handle Client Requests
def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    parts = request.split()

    if parts[0] == "REGISTER":
        role, username, password = parts[1], parts[2], parts[3]
        response = register_user(role, username, password)
    elif parts[0] == "LOGIN":
        username, password = parts[1], parts[2]
        response = login_user(username, password)
    else:
        response = "Invalid request!"

    client_socket.send(response.encode())
    client_socket.close()

# ✅ Start Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 5000))
server_socket.listen(5)

print("Server is running on port 5000...")

while True:
    client_sock, _ = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_sock,)).start()






    
