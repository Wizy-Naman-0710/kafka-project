import tkinter as tk
from tkinter import messagebox
import client

# Global variable to store current user info
current_user = {"username": "", "role": ""}

# Main window
root = tk.Tk()
root.title("Learning Management System")
root.geometry("400x350")

# Create frames for different screens
login_frame = tk.Frame(root)
signup_frame = tk.Frame(root)
student_frame = tk.Frame(root)
instructor_frame = tk.Frame(root)

# Function to show a frame and hide others
def show_frame(frame):
    login_frame.pack_forget()
    signup_frame.pack_forget()
    student_frame.pack_forget()
    instructor_frame.pack_forget()
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# LOGIN SCREEN
tk.Label(login_frame, text="Learning Management System", font=("Arial", 14, "bold")).pack(pady=10)
tk.Label(login_frame, text="Username:").pack(pady=5)
login_username = tk.Entry(login_frame, width=30)
login_username.pack(pady=5)

tk.Label(login_frame, text="Password:").pack(pady=5)
login_password = tk.Entry(login_frame, show="*", width=30)
login_password.pack(pady=5)

def handle_login():
    username = login_username.get()
    password = login_password.get()
    
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password!")
        return
        
    response = client.send_request(f"LOGIN {username} {password}")
    
    if "Login successful" in response:
        current_user["username"] = username
        current_user["role"] = response.split()[-1]
        
        if current_user["role"] == "student":
            show_frame(student_frame)
        else:
            show_frame(instructor_frame)
    else:
        messagebox.showerror("Login Failed", response)

tk.Button(login_frame, text="Login", command=handle_login).pack(pady=10)
tk.Button(login_frame, text="Sign Up", command=lambda: show_frame(signup_frame)).pack(pady=5)

# SIGNUP SCREEN
tk.Label(signup_frame, text="Create Account", font=("Arial", 14, "bold")).pack(pady=10)
tk.Label(signup_frame, text="Username:").pack(pady=5)
signup_username = tk.Entry(signup_frame, width=30)
signup_username.pack(pady=5)

tk.Label(signup_frame, text="Password:").pack(pady=5)
signup_password = tk.Entry(signup_frame, show="*", width=30)
signup_password.pack(pady=5)

role_var = tk.StringVar(value="student")
tk.Label(signup_frame, text="Select Role:").pack(pady=5)
tk.Radiobutton(signup_frame, text="Student", variable=role_var, value="student").pack()
tk.Radiobutton(signup_frame, text="Instructor", variable=role_var, value="instructor").pack()

def handle_signup():
    username = signup_username.get()
    password = signup_password.get()
    role = role_var.get()
    
    if not username or not password:
        messagebox.showerror("Error", "Please enter all fields!")
        return
        
    response = client.send_request(f"REGISTER {role} {username} {password}")
    messagebox.showinfo("Registration", response)
    
    if "Successful" in response:
        show_frame(login_frame)

tk.Button(signup_frame, text="Sign Up", command=handle_signup).pack(pady=10)
tk.Button(signup_frame, text="Back to Login", command=lambda: show_frame(login_frame)).pack(pady=5)

# STUDENT DASHBOARD
def student_welcome_label():
    welcome_label = tk.Label(student_frame, text=f"Welcome, Student {current_user['username']}!", font=("Arial", 14, "bold"))
    welcome_label.pack(pady=10)
    return welcome_label

welcome_label_student = student_welcome_label()

def view_courses():
    courses_window = tk.Toplevel(root)
    courses_window.title("All Courses")
    courses_window.geometry("300x250")
    
    response = client.send_request("GET_COURSES")
    
    text_area = tk.Text(courses_window, width=30, height=10)
    text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    if "No courses" in response or "Error" in response:
        text_area.insert(tk.END, response)
    else:
        courses = response.split("|")
        text_area.insert(tk.END, "Available Courses:\n\n")
        for i, course in enumerate(courses, 1):
            text_area.insert(tk.END, f"{i}. {course}\n")
            
    text_area.config(state=tk.DISABLED)
    tk.Button(courses_window, text="Close", command=courses_window.destroy).pack(pady=10)

def get_resources():
    resources_window = tk.Toplevel(root)
    resources_window.title("Get Course Resources")
    resources_window.geometry("300x300")
    
    tk.Label(resources_window, text="Enter Course ID:").pack(pady=10)
    course_id_entry = tk.Entry(resources_window, width=20)
    course_id_entry.pack(pady=5)
    
    result_text = tk.Text(resources_window, width=30, height=10)
    result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    def search_resources():
        course_id = course_id_entry.get()
        if not course_id:
            messagebox.showerror("Error", "Please enter a Course ID!")
            return
            
        response = client.send_request(f"GET_RESOURCES {course_id}")
        
        result_text.delete(1.0, tk.END)
        if "Error" in response:
            result_text.insert(tk.END, response)
        else:
            resources = response.split("|")
            result_text.insert(tk.END, f"Resources for Course {course_id}:\n\n")
            for i, resource in enumerate(resources, 1):
                result_text.insert(tk.END, f"{i}. {resource}\n")
    
    tk.Button(resources_window, text="Search", command=search_resources).pack(pady=5)
    tk.Button(resources_window, text="Close", command=resources_window.destroy).pack(pady=5)

tk.Button(student_frame, text="View All Courses", command=view_courses).pack(pady=10)
tk.Button(student_frame, text="Get Course Resources", command=get_resources).pack(pady=10)
tk.Button(student_frame, text="Logout", command=lambda: show_frame(login_frame)).pack(pady=10)

# INSTRUCTOR DASHBOARD
def instructor_welcome_label():
    welcome_label = tk.Label(instructor_frame, text=f"Welcome, Instructor {current_user['username']}!", font=("Arial", 14, "bold"))
    welcome_label.pack(pady=10)
    return welcome_label

welcome_label_instructor = instructor_welcome_label()

def upload_resource():
    # Create a simple pop-up window to upload resource
    upload_window = tk.Toplevel(root)
    upload_window.title("Upload Course Resource")
    upload_window.geometry("300x200")
    
    tk.Label(upload_window, text="Course ID:").pack(pady=5)
    course_id_entry = tk.Entry(upload_window, width=20)
    course_id_entry.pack(pady=5)
    
    tk.Label(upload_window, text="Resource URL:").pack(pady=5)
    resource_url_entry = tk.Entry(upload_window, width=20)
    resource_url_entry.pack(pady=5)
    
    def handle_upload():
        course_id = course_id_entry.get()
        resource_url = resource_url_entry.get()
        
        if not course_id or not resource_url:
            messagebox.showerror("Error", "Please enter all fields!")
            return
            
        response = client.send_request(f"UPLOAD_RESOURCE {course_id} {resource_url} {current_user['username']}")
        messagebox.showinfo("Upload Resource", response)
        
        if "Successfully" in response:
            upload_window.destroy()
    
    tk.Button(upload_window, text="Upload", command=handle_upload).pack(pady=10)
    tk.Button(upload_window, text="Cancel", command=upload_window.destroy).pack(pady=5)

tk.Button(instructor_frame, text="Upload Course Resources", command=upload_resource).pack(pady=10)
tk.Button(instructor_frame, text="View All Courses", command=view_courses).pack(pady=10)
tk.Button(instructor_frame, text="Logout", command=lambda: show_frame(login_frame)).pack(pady=10)


show_frame(login_frame)
root.mainloop()



