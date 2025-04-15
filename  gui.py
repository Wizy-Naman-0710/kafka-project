import tkinter as tk
from tkinter import messagebox
import client


root = tk.Tk()
root.title("LMS Login")
root.geometry("300x300")

tk.Label(root, text="Username:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Password:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)


role_var = tk.StringVar(value="student")
tk.Label(root, text="Select Role:").pack(pady=5)
tk.Radiobutton(root, text="Student", variable=role_var, value="student").pack()
tk.Radiobutton(root, text="Instructor", variable=role_var, value="instructor").pack()


def register():
    username = entry_username.get()
    password = entry_password.get()
    role = role_var.get()
    
    if not username or not password:
        messagebox.showerror("Error", "Please enter all fields!")
        return
    
    response = client.send_request(f"REGISTER {role} {username} {password}")
    messagebox.showinfo("Response", response)


def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password!")
        return
    
    response = client.send_request(f"LOGIN {username} {password}")
    
    if "Login successful" in response:
        role = response.split()[-1]
        open_dashboard(role)
    else:
        messagebox.showerror("Login Failed", response)


def open_dashboard(role):
    root.withdraw()  # Hide login window
    dashboard = tk.Toplevel()
    dashboard.title(f"{role.capitalize()} Dashboard")
    dashboard.geometry("300x300")
    
    tk.Label(dashboard, text=f"Welcome, {role.capitalize()}!").pack(pady=10)

    if role == "student":
        # tk.Button(dashboard, text="Take Quiz", command=lambda: messagebox.showinfo("Quiz", "Quiz Feature")).pack()
        # tk.Button(dashboard, text="Rate Course", command=lambda: messagebox.showinfo("Rate", "Rating Feature")).pack()
        #Should have textbox for coourse id 
        tk.Button(dashboard, text="View Courses", command=lambda: messagebox.showinfo("Courses", "Course List")).pack()
        tk.Button(dashboard,text="Get Course Resources",command=lambda:messagebox.showinfo("Resources","Get Course Resources")).pack()
        
    elif role == "instructor":
        # tk.Button(dashboard, text="Add Quiz", command=lambda: messagebox.showinfo("Quiz", "Add Quiz Feature")).pack()
        # tk.Button(dashboard, text="Evaluate Quiz", command=lambda: messagebox.showinfo("Evaluate", "Evaluation Feature")).pack()
        # tk.Button(dashboard, text="Add Test", command=lambda: messagebox.showinfo("Test", "Add Test Feature")).pack()
        #Should have textbox for coourse id and havbe to send poster_id and resource(url/pdf to be decided) along with it 
        tk.Button(dashboard, text="Upload Course Resources", command=lambda: messagebox.showinfo("Resources", "Upload Course Resources")).pack()
    tk.Button(dashboard, text="Logout", command=lambda: [dashboard.destroy(), root.deiconify()]).pack()


tk.Button(root, text="Register", command=register).pack(pady=5)
tk.Button(root, text="Login", command=login).pack(pady=5)

root.mainloop()






