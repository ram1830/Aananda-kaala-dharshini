from tkinter import *
from PIL import Image, ImageTk, ImageFilter
from tkinter import ttk, messagebox
import pymysql, os, secrets, smtplib, threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import credentials as cr

class BeautifulSignUp:
    def __init__(self, root):
        self.window = root
        self.window.title("Beautiful Sign Up")
        self.window.geometry("1280x800+0+0")
        self.window.config(bg="#f8fafc")
        self.window.resizable(False, False)

        # Load and set background image
        self.load_background_image()
        # Create main container
        self.create_main_container()
        # Create form elements
        self.create_form_elements()

    def load_background_image(self):
        """Load and display background image"""
        try:
            # Load your specific image
            original_image = Image.open(r"C:\Users\srira\Desktop\s1.jpg")
            # Resize to fit window
            resized_image = original_image.resize((1280, 800), Image.Resampling.LANCZOS)
            # Apply subtle blur for modern effect
            blurred_image = resized_image.filter(ImageFilter.GaussianBlur(radius=2))
            self.bg_img = ImageTk.PhotoImage(blurred_image)

            # Create background label
            self.bg_label = Label(self.window, image=self.bg_img)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        except Exception as e:
            print(f"Could not load image: {e}")
            # Use gradient background as fallback
            self.window.config(bg="#667eea")

    def create_main_container(self):
        """Create the main container with modern styling"""
        # Main container frame with modern styling
        self.main_frame = Frame(
            self.window, 
            bg="white",
            relief="flat",
            bd=0
        )
        self.main_frame.place(x=390, y=100, width=500, height=600)

        # Add subtle shadow effect using a slightly offset frame
        shadow_frame = Frame(
            self.window, 
            bg="#e2e8f0",  # Light gray shadow instead of transparent
            relief="flat", 
            bd=0
        )
        shadow_frame.place(x=395, y=105, width=500, height=600)

        # Bring main frame to front
        self.main_frame.lift()

    def create_form_elements(self):
        """Create all form elements with beautiful styling"""

        # Header section
        header_frame = Frame(self.main_frame, bg="white", height=100)
        header_frame.pack(fill="x", padx=40, pady=(40, 20))
        header_frame.pack_propagate(False)

        # Title
        title_label = Label(
            header_frame,
            text="Create Account",
            font=("Segoe UI", 28, "bold"),
            bg="white",
            fg="#1e293b"
        )
        title_label.pack(anchor="w")

        # Subtitle
        subtitle_label = Label(
            header_frame,
            text="Join our community today",
            font=("Segoe UI", 12),
            bg="white",
            fg="#64748b"
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))

        # Form container
        form_frame = Frame(self.main_frame, bg="white")
        form_frame.pack(fill="both", expand=True, padx=40)

        # First Name and Last Name Row
        name_frame = Frame(form_frame, bg="white")
        name_frame.pack(fill="x", pady=(0, 20))

        # First Name
        fname_container = Frame(name_frame, bg="white")
        fname_container.pack(side="left", fill="both", expand=True, padx=(0, 10))

        Label(
            fname_container,
            text="First Name",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(anchor="w", pady=(0, 5))

        fname_frame = Frame(fname_container, bg="#f1f5f9", relief="flat", bd=1)
        fname_frame.pack(fill="x", ipady=8)

        self.fname_txt = Entry(
            fname_frame,
            font=("Segoe UI", 11),
            bg="#f1f5f9",
            fg="#1e293b",
            relief="flat",
            bd=0
        )
        self.fname_txt.pack(fill="x", padx=15)

        # Last Name  
        lname_container = Frame(name_frame, bg="white")
        lname_container.pack(side="right", fill="both", expand=True, padx=(10, 0))

        Label(
            lname_container,
            text="Last Name",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(anchor="w", pady=(0, 5))

        lname_frame = Frame(lname_container, bg="#f1f5f9", relief="flat", bd=1)
        lname_frame.pack(fill="x", ipady=8)

        self.lname_txt = Entry(
            lname_frame,
            font=("Segoe UI", 11),
            bg="#f1f5f9",
            fg="#1e293b",
            relief="flat",
            bd=0
        )
        self.lname_txt.pack(fill="x", padx=15)

        # Email
        email_container = Frame(form_frame, bg="white")
        email_container.pack(fill="x", pady=(0, 20))

        Label(
            email_container,
            text="Email Address",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(anchor="w", pady=(0, 5))

        email_frame = Frame(email_container, bg="#f1f5f9", relief="flat", bd=1)
        email_frame.pack(fill="x", ipady=8)

        self.email_txt = Entry(
            email_frame,
            font=("Segoe UI", 11),
            bg="#f1f5f9",
            fg="#1e293b",
            relief="flat",
            bd=0
        )
        self.email_txt.pack(fill="x", padx=15)

        # Password
        password_container = Frame(form_frame, bg="white")
        password_container.pack(fill="x", pady=(0, 20))

        Label(
            password_container,
            text="Password",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(anchor="w", pady=(0, 5))

        password_frame = Frame(password_container, bg="#f1f5f9", relief="flat", bd=1)
        password_frame.pack(fill="x", ipady=8)

        self.password_txt = Entry(
            password_frame,
            font=("Segoe UI", 11),
            bg="#f1f5f9",
            fg="#1e293b",
            relief="flat",
            bd=0,
            show="*"
        )
        self.password_txt.pack(fill="x", padx=15)

        # Terms checkbox
        terms_frame = Frame(form_frame, bg="white")
        terms_frame.pack(fill="x", pady=(10, 30))

        self.terms = IntVar()
        terms_check = Checkbutton(
            terms_frame,
            text="I agree to the Terms & Conditions",
            variable=self.terms,
            font=("Segoe UI", 10),
            bg="white",
            fg="#64748b",
            activebackground="white",
            activeforeground="#3b82f6",
            selectcolor="#3b82f6"
        )
        terms_check.pack(anchor="w")

        # Sign Up Button
        signup_btn = Button(
            form_frame,
            text="Create Account",
            command=self.signup_func,
            font=("Segoe UI", 12, "bold"),
            bg="#3b82f6",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#2563eb",
            activeforeground="white"
        )
        signup_btn.pack(fill="x", ipady=12, pady=(0, 20))

        # Login link
        login_frame = Frame(form_frame, bg="white")
        login_frame.pack(fill="x")

        login_text = Label(
            login_frame,
            text="Already have an account? Sign In",
            font=("Segoe UI", 10),
            bg="white",
            fg="#3b82f6",
            cursor="hand2"
        )
        login_text.pack()

    def generate_verification_token(self):
        """Generate a secure verification token"""
        return secrets.token_urlsafe(32)

    def send_verification_email(self, email, first_name, customer_id, token):
        """Send verification email to user"""
        try:
            # Email configuration - UPDATE THESE WITH YOUR EMAIL SETTINGS
            smtp_server = "smtp.gmail.com"  # Change based on your email provider
            smtp_port = 587
            sender_email = "your_email@gmail.com"  # Replace with your email
            sender_password = "your_app_password"  # Replace with your Gmail app password

            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = "🎉 Verify Your Email - Panchangam Dashboard"

            # Email body with verification link
            verification_link = f"http://localhost:8000/verify?token={token}"
            
            body = f"""
            Dear {first_name},

            🎉 Welcome to Panchangam Dashboard!

            Your account has been created successfully with Customer ID: {customer_id}

            To complete your registration and activate your account, please verify your email address by clicking the link below:

            {verification_link}

            Or copy and paste this link in your browser.

            ✅ Click "Yes" or the link above to verify your email address.

            If you did not create this account, please ignore this email.

            Best regards,
            Panchangam Dashboard Team

            ---
            Hindu Calendar & Astrology System
            """

            msg.attach(MIMEText(body, 'plain'))

            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, email, text)
            server.quit()

            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    def send_email_async(self, email, first_name, customer_id, token):
        """Send verification email in background thread"""
        def email_thread():
            success = self.send_verification_email(email, first_name, customer_id, token)
            if not success:
                print("Failed to send verification email")
        
        # Start email sending in background
        threading.Thread(target=email_thread, daemon=True).start()

    def signup_func(self):
        """Handle signup functionality with email verification"""
        # Validate all fields
        if (self.fname_txt.get().strip() == "" or 
            self.lname_txt.get().strip() == "" or 
            self.email_txt.get().strip() == "" or 
            self.password_txt.get().strip() == ""):
            messagebox.showerror(
                "Error!", 
                "All fields are required", 
                parent=self.window
            )
            return

        # Check terms agreement
        if self.terms.get() == 0:
            messagebox.showerror(
                "Error!", 
                "Please agree to the Terms & Conditions",
                parent=self.window
            )
            return

        # Validate email format
        email = self.email_txt.get().strip()
        if "@" not in email or "." not in email:
            messagebox.showerror(
                "Error!", 
                "Please enter a valid email address",
                parent=self.window
            )
            return

        try:
            # Connect to database
            connection = pymysql.connect(
                host=cr.host, 
                user=cr.user, 
                password=cr.password, 
                database=cr.database
            )
            cur = connection.cursor()

            # Check if email already exists
            cur.execute("SELECT * FROM user_info WHERE email=%s", (email,))
            row = cur.fetchone()

            if row is not None:
                messagebox.showerror(
                    "Error!", 
                    "This email is already registered. Please use a different email.",
                    parent=self.window
                )
            else:
                # Generate verification token
                verification_token = self.generate_verification_token()
                
                # Insert new user - customer_id will be AUTO-GENERATED by MySQL trigger
                cur.execute(
                    """INSERT INTO user_info (first_name, last_name, email, password, email_verified, verification_token) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (
                        self.fname_txt.get().strip(),
                        self.lname_txt.get().strip(), 
                        email,
                        self.password_txt.get().strip(),
                        0,  # Email not verified initially
                        verification_token
                    )
                )
                connection.commit()
                
                # Get the auto-generated customer_id
                cur.execute("SELECT customer_id FROM user_info WHERE email=%s", (email,))
                customer_data = cur.fetchone()
                customer_id = customer_data[0] if customer_data else "Unknown"
                
                connection.close()

                # Send verification email in background
                self.send_email_async(email, self.fname_txt.get().strip(), customer_id, verification_token)

                # Show success message with verification instructions
                messagebox.showinfo(
                    "Account Created Successfully!", 
                    f"🎉 Welcome to Panchangam Dashboard!\n\n"
                    f"Your Customer ID: {customer_id}\n\n"
                    f"📧 IMPORTANT: A verification email has been sent to:\n{email}\n\n"
                    f"✅ Please check your email and click the verification link to activate your account.\n\n"
                    f"You must verify your email before you can login.",
                    parent=self.window
                )
                self.reset_fields()

        except Exception as es:
            messagebox.showerror(
                "Error!", 
                f"Database error: {es}",
                parent=self.window
            )

    def reset_fields(self):
        """Reset all form fields"""
        self.fname_txt.delete(0, END)
        self.lname_txt.delete(0, END)
        self.email_txt.delete(0, END)
        self.password_txt.delete(0, END)
        self.terms.set(0)

if __name__ == "__main__":
    root = Tk()
    app = BeautifulSignUp(root)
    root.mainloop()
