from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import credentials as cr

class PanchangamDashboard:
    def __init__(self, root, user_email):
        self.window = root
        self.user_email = user_email
        self.window.title("Panchangam Dashboard")
        self.window.geometry("800x600")
        self.window.config(bg="#f8fafc")
        self.window.resizable(False, False)

        # Create main container
        self.create_header()
        self.create_main_content()
        self.create_footer()

    def create_header(self):
        """Create the header section with welcome message and user info"""
        header_frame = Frame(self.window, bg="#34495e", height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        # Welcome message with user email
        welcome_label = Label(header_frame, text=f"Welcome to Panchangam Dashboard - {self.user_email}",
                              font=("Arial", 16, "bold"), bg="#34495e", fg="white")
        welcome_label.pack(side="left", padx=30, pady=25)

        # Logout button
        logout_btn = Button(header_frame, text="Logout", command=self.logout,
                            font=("Arial", 10, "bold"), bg="#e74c3c", fg="white",
                            relief="flat", cursor="hand2", padx=15, pady=5)
        logout_btn.pack(side="right", padx=30, pady=25)

    def create_main_content(self):
        """Create the main content area with dropdown menu"""
        # Main content frame
        main_frame = Frame(self.window, bg="#f8fafc")
        main_frame.pack(fill="both", expand=True, padx=40, pady=30)

        # Title and description
        title_label = Label(main_frame, text="Select a Feature",
                            font=("Arial", 22, "bold"), bg="#f8fafc", fg="#2c3e50")
        title_label.pack(pady=(0, 10))

        subtitle_label = Label(main_frame, text="Choose from the dropdown menu to access different Panchangam features",
                               font=("Arial", 12), bg="#f8fafc", fg="#7f8c8d")
        subtitle_label.pack(pady=(0, 30))

        # Dropdown container
        dropdown_frame = Frame(main_frame, bg="white", relief="solid", bd=2)
        dropdown_frame.pack(pady=20, padx=100, fill="x")

        # Dropdown label
        Label(dropdown_frame, text="Choose Feature:",
              font=("Arial", 14, "bold"), bg="white", fg="#2c3e50").pack(pady=(20, 10))

        # Create the dropdown menu with PANCHANGAM as first option
        self.selected_feature = StringVar()
        self.feature_options = [
            "PANCHANGAM",
            "KUNDALI (Birth Chart)",
            "HOROSCOPE",
            "MUHURAT (Auspicious Times)",
            "FESTIVALS",
            "ASTROLOGY CONSULTATION",
            "CALENDAR VIEW",
            "COMPATIBILITY MATCHING",
            "MEDITATION & YOGA",
            "SETTINGS"
        ]

        self.feature_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.selected_feature,
                                             values=self.feature_options, font=("Arial", 12),
                                             state="readonly", width=30)
        self.feature_dropdown.pack(pady=10)
        self.feature_dropdown.set("Select a feature...")
        self.feature_dropdown.bind("<<ComboboxSelected>>", self.on_feature_select)

        # Action button
        self.action_btn = Button(dropdown_frame, text="Access Feature", command=self.access_feature,
                                 font=("Arial", 12, "bold"), bg="#27ae60", fg="white",
                                 relief="flat", cursor="hand2", padx=20, pady=8)
        self.action_btn.pack(pady=(10, 20))

        # Information display area
        self.info_frame = Frame(main_frame, bg="white", relief="solid", bd=2)
        self.info_frame.pack(pady=20, padx=50, fill="both", expand=True)

        self.info_label = Label(self.info_frame, text="Select a feature to see its description",
                                font=("Arial", 11), bg="white", fg="#7f8c8d",
                                wraplength=600, justify="center")
        self.info_label.pack(pady=40)

    def create_footer(self):
        """Create the footer section"""
        footer_frame = Frame(self.window, bg="#34495e", height=40)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        footer_label = Label(footer_frame, text="© 2025 Panchangam Dashboard - Hindu Calendar & Astrology System",
                             font=("Arial", 9), bg="#34495e", fg="white")
        footer_label.pack(pady=10)

    def on_feature_select(self, event=None):
        """Handle dropdown selection and show feature information"""
        selected = self.selected_feature.get()
        
        feature_info = {
            "PANCHANGAM": "PANCHANGAM - Hindu Calendar\n\nTraditional Hindu calendar showing Tithi, Nakshatra, Yoga, Karana, and Vara for each day.\n\n📅 Click 'Access Feature' to open the interactive Panchangam calendar.",
            "KUNDALI (Birth Chart)": "KUNDALI - Birth Chart Analysis\n\nGenerate detailed birth charts with planetary positions and predictions.",
            "HOROSCOPE": "HOROSCOPE - Daily Predictions\n\nPersonalized horoscope readings based on your zodiac sign.",
            "MUHURAT (Auspicious Times)": "MUHURAT - Auspicious Timings\n\nFind auspicious times for ceremonies and important activities.",
            "FESTIVALS": "FESTIVALS - Hindu Calendar Events\n\nComplete list of Hindu festivals and religious observances.",
            "ASTROLOGY CONSULTATION": "ASTROLOGY CONSULTATION\n\nConnect with experienced astrologers for guidance.",
            "CALENDAR VIEW": "CALENDAR VIEW - Monthly Overview\n\nVisual calendar with festivals and important dates.",
            "COMPATIBILITY MATCHING": "COMPATIBILITY MATCHING - Kundali Milan\n\nCheck marriage compatibility using traditional methods.",
            "MEDITATION & YOGA": "MEDITATION & YOGA - Spiritual Practices\n\nSpiritual guidance aligned with astrological timings.",
            "SETTINGS": "SETTINGS - Customize Experience\n\nPersonalize your dashboard preferences."
        }

        if selected in feature_info:
            self.info_label.config(text=feature_info[selected], justify="left")

    def access_feature(self):
        """Handle feature access when button is clicked"""
        selected = self.selected_feature.get()
        
        if not selected or selected == "Select a feature...":
            messagebox.showwarning("No Selection", "Please select a feature from the dropdown menu.")
            return

        if selected == "PANCHANGAM":
            try:
                # Open Panchangam calendar page
                self.window.destroy()  # Close current homepage window
                
                # Import and open the Panchangam page
                import panchangam_page
                panchangam_root = Tk()
                panchangam_page.PanchangamPage(panchangam_root, self.user_email)
                panchangam_root.mainloop()
                
            except ImportError:
                messagebox.showerror("Error", "Panchangam page module not found!\n\nPlease ensure 'panchangam_page.py' is in the same directory.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open Panchangam page:\n{str(e)}")
        else:
            # Show message for other features (not yet implemented)
            messagebox.showinfo("Feature Access", f"Accessing {selected}...\n\nThis feature will be available in future updates.")

    def logout(self):
        """Handle logout functionality"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.window.destroy()
            try:
                # Return to login page
                import login_page  # Import your login file (adjust the name as needed)
                root = Tk()
                login_page.EnhancedLogin(root)  # Adjust class name if different
                root.mainloop()
            except ImportError:
                # If login import fails, just close the application
                print("Login module not found. Application closing.")

# For testing homepage directly
if __name__ == "__main__":
    root = Tk()
    app = PanchangamDashboard(root, "test@email.com")
    root.mainloop()
