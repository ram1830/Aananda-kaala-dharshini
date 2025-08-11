from tkinter import *
from tkinter import messagebox
import pymysql
import credentials as cr
import importlib.util
import sys
import os

class EnhancedLogin:
    def __init__(self, root):
        self.window = root
        self.window.title("Enhanced Login System")
        self.window.geometry("500x400")
        self.window.config(bg="#ecf0f1")
        self.window.resizable(False, False)
        
        # Create main frame with better styling
        self.main_frame = Frame(self.window, bg="white", relief="raised", bd=2)
        self.main_frame.place(x=75, y=50, width=350, height=300)
        
        # Header section
        header_frame = Frame(self.main_frame, bg="#34495e", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        Label(header_frame, text="LOGIN SYSTEM", 
              font=("Arial", 16, "bold"), 
              bg="#34495e", fg="white").pack(expand=True)
              
        # Form section
        form_frame = Frame(self.main_frame, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Email
        Label(form_frame, text="Email Address:", 
              font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
        self.email_entry = Entry(form_frame, font=("Arial", 11), width=35, relief="solid")
        self.email_entry.pack(pady=(0, 15), ipady=5)
        
        # Password  
        Label(form_frame, text="Password:", 
              font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
        self.password_entry = Entry(form_frame, font=("Arial", 11), width=35, 
                                   show="*", relief="solid")
        self.password_entry.pack(pady=(0, 20), ipady=5)
        
        # CONTINUE BUTTON - LARGE AND VISIBLE
        self.continue_button = Button(form_frame, text="CONTINUE", 
                                     command=self.check_credentials,
                                     font=("Arial", 14, "bold"),
                                     bg="#27ae60", fg="white",
                                     width=20, height=2,
                                     relief="flat", cursor="hand2",
                                     activebackground="#2ecc71")
        self.continue_button.pack(pady=10)
        
        # Status display
        self.status_label = Label(form_frame, text="Enter credentials and click Continue",
                                 font=("Arial", 10), bg="white", fg="#7f8c8d")
        self.status_label.pack(pady=5)
        
        # Bind Enter key to continue button
        self.window.bind('<Return>', lambda event: self.check_credentials())

    def load_homepage(self, user_email):
        """Load and run homepage.py from the specific path"""
        try:
            # Your specific homepage.py path
            homepage_path = r"C:\Users\srira\Desktop\hore_proj\login-page-using-Python-and-MySQL-main\homepage.py"
            
            # Check if homepage.py exists at the specified path
            if not os.path.exists(homepage_path):
                messagebox.showerror("Error", f"homepage.py file not found at:\n{homepage_path}")
                return False

            # Import homepage module dynamically from the specific path
            spec = importlib.util.spec_from_file_location("homepage", homepage_path)
            homepage_module = importlib.util.module_from_spec(spec)
            sys.modules["homepage"] = homepage_module
            spec.loader.exec_module(homepage_module)
            
            # Create new window for homepage and run it
            homepage_root = Tk()
            
            # Check if homepage has the expected class (adjust class name if needed)
            if hasattr(homepage_module, 'PanchangamDashboard'):
                homepage_module.PanchangamDashboard(homepage_root, user_email)
            elif hasattr(homepage_module, 'HomePage'):
                homepage_module.HomePage(homepage_root, user_email)
            else:
                # If no specific class found, just run the homepage module
                messagebox.showinfo("Info", "Homepage loaded successfully!")
            
            homepage_root.mainloop()
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load homepage: {str(e)}")
            return False
        
    def check_credentials(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Update status
        self.status_label.config(text="Checking credentials...", fg="#f39c12")
        self.window.update()
        
        if not email or not password:
            self.status_label.config(text="❌ Please enter both email and password", fg="red")
            messagebox.showerror("Error", "All fields are required!")
            return
            
        try:
            # Connect to database
            conn = pymysql.connect(
                host=cr.host,
                user=cr.user,
                password=cr.password, 
                database=cr.database
            )
            cursor = conn.cursor()
            
            # Validate credentials AND check email verification
            cursor.execute("SELECT customer_id, first_name, last_name, email, email_verified FROM user_info WHERE email=%s AND password=%s", (email, password))
            user_data = cursor.fetchone()
            conn.close()
            
            if user_data:
                self.status_label.config(text="✅ VALID - Login Successful!", fg="green")
                
                # Check if email is verified - but allow login regardless
                if user_data[4] == 1:  # email_verified column
                    # Email is verified - normal login
                    messagebox.showinfo("Welcome Back!", f"Hello {user_data[1]}!\n\nCustomer ID: {user_data[0]}\nEmail Status: ✅ Verified")
                    
                else:
                    # Email is NOT verified - show warning but still allow login
                    messagebox.showwarning("Email Verification Reminder", 
                        f"Hello {user_data[1]}!\n\n⚠️ Your email is not yet verified.\n\nCustomer ID: {user_data[0]}\n\n📧 Please check your email and click the verification link to complete your account setup.\n\nYou can still use the dashboard, but we recommend verifying your email for security.")
                
                # **REDIRECT TO HOMEPAGE USING SPECIFIC PATH**
                self.window.destroy()  # Close login window
                self.load_homepage(email)  # Load homepage from specific path
                
            else:
                self.status_label.config(text="❌ INVALID - Incorrect credentials", fg="red")
                messagebox.showerror("Invalid Login", "Email or password is incorrect!")
                
        except Exception as e:
            self.status_label.config(text="❌ Database connection failed", fg="red")
            messagebox.showerror("Database Error", f"Connection failed: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = EnhancedLogin(root)
    root.mainloop()
