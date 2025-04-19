# import tkinter as tk
# from tkinter import messagebox
# import client

# # Global variable to store current user info
# current_user = {"username": "", "role": ""}

# # Main window
# root = tk.Tk()
# root.title("Learning Management System")
# root.geometry("400x350")

# # Create frames for different screens
# login_frame = tk.Frame(root)
# signup_frame = tk.Frame(root)
# student_frame = tk.Frame(root)
# instructor_frame = tk.Frame(root)

# # Function to show a frame and hide others
# def show_frame(frame):
#     login_frame.pack_forget()
#     signup_frame.pack_forget()
#     student_frame.pack_forget()
#     instructor_frame.pack_forget()
#     frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# # LOGIN SCREEN
# tk.Label(login_frame, text="Learning Management System", font=("Arial", 14, "bold")).pack(pady=10)
# tk.Label(login_frame, text="Username:").pack(pady=5)
# login_username = tk.Entry(login_frame, width=30)
# login_username.pack(pady=5)

# tk.Label(login_frame, text="Password:").pack(pady=5)
# login_password = tk.Entry(login_frame, show="*", width=30)
# login_password.pack(pady=5)

# def handle_login():
#     username = login_username.get()
#     password = login_password.get()
    
#     if not username or not password:
#         messagebox.showerror("Error", "Please enter both username and password!")
#         return
        
#     response = client.send_request(f"LOGIN {username} {password}")
    
#     if "Login successful" in response:
#         current_user["username"] = username
#         current_user["role"] = response.split()[-1]
        
#         if current_user["role"] == "student":
#             show_frame(student_frame)
#         else:
#             show_frame(instructor_frame)
#     else:
#         messagebox.showerror("Login Failed", response)

# tk.Button(login_frame, text="Login", command=handle_login).pack(pady=10)
# tk.Button(login_frame, text="Sign Up", command=lambda: show_frame(signup_frame)).pack(pady=5)

# # SIGNUP SCREEN
# tk.Label(signup_frame, text="Create Account", font=("Arial", 14, "bold")).pack(pady=10)
# tk.Label(signup_frame, text="Username:").pack(pady=5)
# signup_username = tk.Entry(signup_frame, width=30)
# signup_username.pack(pady=5)

# tk.Label(signup_frame, text="Password:").pack(pady=5)
# signup_password = tk.Entry(signup_frame, show="*", width=30)
# signup_password.pack(pady=5)

# role_var = tk.StringVar(value="student")
# tk.Label(signup_frame, text="Select Role:").pack(pady=5)
# tk.Radiobutton(signup_frame, text="Student", variable=role_var, value="student").pack()
# tk.Radiobutton(signup_frame, text="Instructor", variable=role_var, value="instructor").pack()

# def handle_signup():
#     username = signup_username.get()
#     password = signup_password.get()
#     role = role_var.get()
    
#     if not username or not password:
#         messagebox.showerror("Error", "Please enter all fields!")
#         return
        
#     response = client.send_request(f"REGISTER {role} {username} {password}")
#     messagebox.showinfo("Registration", response)
    
#     if "Successful" in response:
#         show_frame(login_frame)

# tk.Button(signup_frame, text="Sign Up", command=handle_signup).pack(pady=10)
# tk.Button(signup_frame, text="Back to Login", command=lambda: show_frame(login_frame)).pack(pady=5)

# # STUDENT DASHBOARD
# def student_welcome_label():
#     welcome_label = tk.Label(student_frame, text=f"Welcome, Student {current_user['username']}!", font=("Arial", 14, "bold"))
#     welcome_label.pack(pady=10)
#     return welcome_label

# welcome_label_student = student_welcome_label()

# def view_courses():
#     courses_window = tk.Toplevel(root)
#     courses_window.title("All Courses")
#     courses_window.geometry("300x250")
    
#     response = client.send_request("GET_COURSES")
    
#     text_area = tk.Text(courses_window, width=30, height=10)
#     text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
#     if "No courses" in response or "Error" in response:
#         text_area.insert(tk.END, response)
#     else:
#         courses = response.split("|")
#         text_area.insert(tk.END, "Available Courses:\n\n")
#         for i, course in enumerate(courses, 1):
#             text_area.insert(tk.END, f"{i}. {course}\n")
            
#     text_area.config(state=tk.DISABLED)
#     tk.Button(courses_window, text="Close", command=courses_window.destroy).pack(pady=10)

# def get_resources():
#     resources_window = tk.Toplevel(root)
#     resources_window.title("Get Course Resources")
#     resources_window.geometry("300x300")
    
#     tk.Label(resources_window, text="Enter Course ID:").pack(pady=10)
#     course_id_entry = tk.Entry(resources_window, width=20)
#     course_id_entry.pack(pady=5)
    
#     result_text = tk.Text(resources_window, width=30, height=10)
#     result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
#     def search_resources():
#         course_id = course_id_entry.get()
#         if not course_id:
#             messagebox.showerror("Error", "Please enter a Course ID!")
#             return
            
#         response = client.send_request(f"GET_RESOURCES {course_id}")
        
#         result_text.delete(1.0, tk.END)
#         if "Error" in response:
#             result_text.insert(tk.END, response)
#         else:
#             resources = response.split("|")
#             result_text.insert(tk.END, f"Resources for Course {course_id}:\n\n")
#             for i, resource in enumerate(resources, 1):
#                 result_text.insert(tk.END, f"{i}. {resource}\n")
    
#     tk.Button(resources_window, text="Search", command=search_resources).pack(pady=5)
#     tk.Button(resources_window, text="Close", command=resources_window.destroy).pack(pady=5)

# tk.Button(student_frame, text="View All Courses", command=view_courses).pack(pady=10)
# tk.Button(student_frame, text="Get Course Resources", command=get_resources).pack(pady=10)
# tk.Button(student_frame, text="Logout", command=lambda: show_frame(login_frame)).pack(pady=10)

# # INSTRUCTOR DASHBOARD
# def instructor_welcome_label():
#     welcome_label = tk.Label(instructor_frame, text=f"Welcome, Instructor {current_user['username']}!", font=("Arial", 14, "bold"))
#     welcome_label.pack(pady=10)
#     return welcome_label

# welcome_label_instructor = instructor_welcome_label()

# def upload_resource():
#     # Create a simple pop-up window to upload resource
#     upload_window = tk.Toplevel(root)
#     upload_window.title("Upload Course Resource")
#     upload_window.geometry("300x200")
    
#     tk.Label(upload_window, text="Course ID:").pack(pady=5)
#     course_id_entry = tk.Entry(upload_window, width=20)
#     course_id_entry.pack(pady=5)
    
#     tk.Label(upload_window, text="Resource URL:").pack(pady=5)
#     resource_url_entry = tk.Entry(upload_window, width=20)
#     resource_url_entry.pack(pady=5)
    
#     def handle_upload():
#         course_id = course_id_entry.get()
#         resource_url = resource_url_entry.get()
        
#         if not course_id or not resource_url:
#             messagebox.showerror("Error", "Please enter all fields!")
#             return
            
#         response = client.send_request(f"UPLOAD_RESOURCE {course_id} {resource_url} {current_user['username']}")
#         messagebox.showinfo("Upload Resource", response)
        
#         if "Successfully" in response:
#             upload_window.destroy()
    
#     tk.Button(upload_window, text="Upload", command=handle_upload).pack(pady=10)
#     tk.Button(upload_window, text="Cancel", command=upload_window.destroy).pack(pady=5)

# tk.Button(instructor_frame, text="Upload Course Resources", command=upload_resource).pack(pady=10)
# tk.Button(instructor_frame, text="View All Courses", command=view_courses).pack(pady=10)
# tk.Button(instructor_frame, text="Logout", command=lambda: show_frame(login_frame)).pack(pady=10)


# show_frame(login_frame)
# root.mainloop()

import tkinter as tk
from tkinter import messagebox, PhotoImage
import client
import time

# Global variable to store current user info
current_user = {"username": "", "role": ""}

# Mario animation class - now attaches to labels
class MarioAnimation:
    def __init__(self, parent, image_path):
        self.parent = parent
        self.canvas = None
        self.jump_timer = None
        self.current_label = None
        
        # Load the Mario image
        self.mario_image = tk.PhotoImage(file=image_path)
        
        # Scale image down if it's too large (optional)
        # Uncomment these lines if your image is too big
        width, height = 30, 30  # Desired size
        self.mario_image = self.mario_image.subsample(self.mario_image.width() // width, 
                                                      self.mario_image.height() // height)
        
    def attach_to_label(self, label):
        # If already attached to this label, do nothing
        if self.current_label == label:
            return
            
        # Remove from previous location if any
        if self.canvas:
            self.canvas.destroy()
            
        self.current_label = label
        
        # Get position of the label widget - place Mario after the label
        x = label.winfo_rootx() - self.parent.winfo_rootx() + label.winfo_width() + 5
        y = label.winfo_rooty() - self.parent.winfo_rooty() - 5
        
        # Create canvas with Mario image
        self.canvas = tk.Canvas(self.parent, 
                               width=self.mario_image.width(), 
                               height=self.mario_image.height(),
                               bg=self.parent.cget('bg'), 
                               highlightthickness=0)
        self.canvas.place(x=x, y=y)
        self.mario_id = self.canvas.create_image(self.mario_image.width()//2, 
                                                self.mario_image.height()//2, 
                                                image=self.mario_image)
        
        # Start jumping animation
        self.start_jumping()
    
    def detach(self):
        # Stop animation and remove canvas
        if self.jump_timer:
            self.parent.after_cancel(self.jump_timer)
            self.jump_timer = None
            
        if self.canvas:
            self.canvas.destroy()
            self.canvas = None
            
        self.current_label = None
    
    def start_jumping(self):
        # Initial position
        self.y_pos = 0
        self.going_up = True
        
        # Start the jump loop
        self.do_jump()
    
    def do_jump(self):
        if not self.canvas:
            return
            
        # Reduced jump height and speed
        if self.going_up:
            self.y_pos -= 1.5  # Smaller jump (was -3)
            if self.y_pos <= -5:  # Lower height (was -10)
                self.going_up = False
        else:
            self.y_pos += 1.5  # Smaller jump (was +3)
            if self.y_pos >= 0:  # Back to original position
                self.going_up = True
                
        # Move Mario
        if self.canvas and self.mario_id:
            self.canvas.coords(self.mario_id, 
                              self.mario_image.width()//2, 
                              self.mario_image.height()//2 + self.y_pos)
            
        # Continue animation loop
        self.jump_timer = self.parent.after(150, self.do_jump)  # Slower animation (was 100ms)


# Function to show an image splash screen
def show_splash_image(image_path, duration=2000, callback=None):
    # Create a toplevel window
    splash = tk.Toplevel()
    splash.overrideredirect(True)  # Remove window decorations
    
    # Calculate position to center the splash window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Load the image
    try:
        img = tk.PhotoImage(file=image_path)
        width, height = img.width(), img.height()
        
        # Center the window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        splash.geometry(f"{width}x{height}+{x}+{y}")
        
        # Display the image
        label = tk.Label(splash, image=img)
        label.image = img  # Keep a reference
        label.pack()
        
        # Close after duration
        splash.after(duration, lambda: close_splash(splash, callback))
        
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        if callback:
            callback()
        return

def close_splash(splash, callback=None):
    splash.destroy()
    if callback:
        callback()

# Main window
root = tk.Tk()
root.title("Learning Management System")
root.geometry("400x350")

# Create Mario animation controller
# Replace "mario.png" with the path to your image file
mario = MarioAnimation(root, "mario.png")  # Use mario.png or mario.jpeg as needed

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
    mario.detach()  # Detach Mario when changing frames
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# LOGIN SCREEN
tk.Label(login_frame, text="Learning Management System", font=("Arial", 14, "bold")).pack(pady=10)

# Username label - we'll save a reference to attach Mario to it
username_label = tk.Label(login_frame, text="Username:")
username_label.pack(pady=5)

login_username = tk.Entry(login_frame, width=30)
login_username.pack(pady=5)

# Password label - we'll save a reference to attach Mario to it
password_label = tk.Label(login_frame, text="Password:")
password_label.pack(pady=5)

login_password = tk.Entry(login_frame, show="*", width=30)
login_password.pack(pady=5)

# Function to attach Mario to the username label when clicked
def focus_username(event):
    mario.attach_to_label(username_label)

# Function to attach Mario to the password label when clicked
def focus_password(event):
    mario.attach_to_label(password_label)

# Bind focus events to the entry widgets
login_username.bind("<FocusIn>", focus_username)
login_password.bind("<FocusIn>", focus_password)

def handle_login():
    username = login_username.get()
    password = login_password.get()
    
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password!")
        show_splash_image("you_shall_not_pass.png", 2000)
        return
        
    response = client.send_request(f"LOGIN {username} {password}")
    
    if "Login successful" in response:
        current_user["username"] = username
        current_user["role"] = response.split()[-1]
        
        # Show welcome image before switching to appropriate frame
        if current_user["role"] == "student":
            show_splash_image("welcome.png", 2000, lambda: show_frame(student_frame))
        else:
            show_splash_image("welcome.png", 2000, lambda: show_frame(instructor_frame))
    else:
        messagebox.showerror("Login Failed", response)
        show_splash_image("you_shall_not_pass.png", 2000)

tk.Button(login_frame, text="Login", command=handle_login).pack(pady=10)
tk.Button(login_frame, text="Sign Up", command=lambda: show_frame(signup_frame)).pack(pady=5)

# SIGNUP SCREEN
tk.Label(signup_frame, text="Create Account", font=("Arial", 14, "bold")).pack(pady=10)

# Username label for signup
signup_username_label = tk.Label(signup_frame, text="Username:")
signup_username_label.pack(pady=5)

signup_username = tk.Entry(signup_frame, width=30)
signup_username.pack(pady=5)
signup_username.bind("<FocusIn>", lambda event: mario.attach_to_label(signup_username_label))

# Password label for signup
signup_password_label = tk.Label(signup_frame, text="Password:")
signup_password_label.pack(pady=5)

signup_password = tk.Entry(signup_frame, show="*", width=30)
signup_password.pack(pady=5)
signup_password.bind("<FocusIn>", lambda event: mario.attach_to_label(signup_password_label))

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
        show_splash_image("you_shall_not_pass.png", 2000)
        return
        
    response = client.send_request(f"REGISTER {role} {username} {password}")
    messagebox.showinfo("Registration", response)
    
    if "successful" in response:
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
    # Create a simple pop-up window to display courses
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
            
    text_area.config(state=tk.DISABLED)  # Make it read-only
    tk.Button(courses_window, text="Close", command=courses_window.destroy).pack(pady=10)

def get_resources():
    # Create a simple pop-up window to get resources
    resources_window = tk.Toplevel(root)
    resources_window.title("Get Course Resources")
    resources_window.geometry("300x300")
    
    # Course ID label and entry with Mario animation
    course_id_label = tk.Label(resources_window, text="Enter Course ID:")
    course_id_label.pack(pady=10)
    
    course_id_entry = tk.Entry(resources_window, width=20)
    course_id_entry.pack(pady=5)
    course_id_entry.bind("<FocusIn>", lambda event: mario.attach_to_label(course_id_label))
    
    result_text = tk.Text(resources_window, width=30, height=10)
    result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    def search_resources():
        course_id = course_id_entry.get()
        if not course_id:
            messagebox.showerror("Error", "Please enter a Course ID!")
            show_splash_image("you_shall_not_pass.png1", 2000)
            return
            
        response = client.send_request(f"GET_RESOURCES {course_id}")
        
        result_text.delete(1.0, tk.END)
        if "Error" in response:
            result_text.insert(tk.END, response)
            show_splash_image("you_shall_not_pass.png", 2000)
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
    
    # Course ID label and entry with Mario animation
    course_id_label = tk.Label(upload_window, text="Course ID:")
    course_id_label.pack(pady=5)
    
    course_id_entry = tk.Entry(upload_window, width=20)
    course_id_entry.pack(pady=5)
    course_id_entry.bind("<FocusIn>", lambda event: mario.attach_to_label(course_id_label))
    
    # Resource URL label and entry with Mario animation
    resource_url_label = tk.Label(upload_window, text="Resource URL:")
    resource_url_label.pack(pady=5)
    
    resource_url_entry = tk.Entry(upload_window, width=20)
    resource_url_entry.pack(pady=5)
    resource_url_entry.bind("<FocusIn>", lambda event: mario.attach_to_label(resource_url_label))
    
    def handle_upload():
        course_id = course_id_entry.get()
        resource_url = resource_url_entry.get()
        
        if not course_id or not resource_url:
            messagebox.showerror("Error", "Please enter all fields!")
            show_splash_image("you_shall_not_pass.png", 2000)
            return
            
        response = client.send_request(f"UPLOAD_RESOURCE {course_id} {resource_url} {current_user['username']}")
        messagebox.showinfo("Upload Resource", response)
        
        if "Successfully" in response:
            upload_window.destroy()
        else:
            show_splash_image("you_shall_not_pass.png", 2000)
    
    tk.Button(upload_window, text="Upload", command=handle_upload).pack(pady=10)
    tk.Button(upload_window, text="Cancel", command=upload_window.destroy).pack(pady=5)

tk.Button(instructor_frame, text="Upload Course Resources", command=upload_resource).pack(pady=10)
tk.Button(instructor_frame, text="View All Courses", command=view_courses).pack(pady=10)
tk.Button(instructor_frame, text="Logout", command=lambda: show_frame(login_frame)).pack(pady=10)

# Start with login screen
show_frame(login_frame)

# Run the application
root.mainloop()

