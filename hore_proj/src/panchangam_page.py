from tkinter import *
from tkinter import ttk, messagebox
try:
    from tkcalendar import Calendar
except ImportError:
    messagebox.showerror("Missing Library", "Please install tkcalendar: pip install tkcalendar")
    exit()

import datetime
import math

class PanchangamPage:
    def __init__(self, root, user_email):
        self.window = root
        self.user_email = user_email
        self.window.title("Panchangam Calendar")
        self.window.geometry("1200x800")
        self.window.config(bg="#f8fafc")
        self.window.resizable(False, False)
        
        # Create the interface
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Set today's date by default
        today = datetime.date.today()
        self.calendar.selection_set(today)
        self.show_panchangam_for_date(today)

    def create_header(self):
        """Create header with title and user info"""
        header_frame = Frame(self.window, bg="#1e293b", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Title
        title_label = Label(header_frame, text="📅 Panchangam Calendar", 
                           font=("Arial", 20, "bold"), bg="#1e293b", fg="white")
        title_label.pack(side="left", padx=30, pady=25)
        
        # Back to Dashboard button
        back_btn = Button(header_frame, text="← Back to Dashboard", command=self.back_to_dashboard,
                         font=("Arial", 10, "bold"), bg="#3b82f6", fg="white",
                         relief="flat", cursor="hand2", padx=15, pady=5)
        back_btn.pack(side="right", padx=(10, 30), pady=30)
        
        # User info
        user_label = Label(header_frame, text=f"Welcome: {self.user_email}", 
                          font=("Arial", 12), bg="#1e293b", fg="#cbd5e1")
        user_label.pack(side="right", padx=(30, 10), pady=30)

    def create_main_content(self):
        """Create main content with calendar and panchangam details"""
        main_frame = Frame(self.window, bg="#f8fafc")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left side - Calendar
        left_frame = Frame(main_frame, bg="white", relief="solid", bd=1)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Calendar title
        cal_title = Label(left_frame, text="Select Date", font=("Arial", 16, "bold"), 
                         bg="white", fg="#1e293b")
        cal_title.pack(pady=20)
        
        # Calendar widget
        try:
            self.calendar = Calendar(left_frame, selectmode='day', 
                                    font=("Arial", 12), cursor="hand2",
                                    year=datetime.date.today().year,
                                    month=datetime.date.today().month,
                                    day=datetime.date.today().day)
            self.calendar.pack(padx=20, pady=20, expand=True, fill="both")
            
            # Bind calendar selection event
            self.calendar.bind("<<CalendarSelected>>", self.on_date_select)
        except Exception as e:
            error_label = Label(left_frame, text=f"Calendar Error: {str(e)}", 
                               font=("Arial", 12), bg="white", fg="red")
            error_label.pack(pady=50)
        
        # Right side - Panchangam Details
        right_frame = Frame(main_frame, bg="white", relief="solid", bd=1)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Panchangam title
        panchang_title = Label(right_frame, text="📋 Panchangam Details", 
                              font=("Arial", 16, "bold"), bg="white", fg="#1e293b")
        panchang_title.pack(pady=20)
        
        # Selected date display
        self.selected_date_var = StringVar()
        self.selected_date_label = Label(right_frame, textvariable=self.selected_date_var,
                                        font=("Arial", 14, "bold"), bg="white", fg="#2563eb")
        self.selected_date_label.pack(pady=10)
        
        # Scrollable frame for panchangam details
        canvas = Canvas(right_frame, bg="white")
        scrollbar = Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")

    def create_footer(self):
        """Create footer"""
        footer_frame = Frame(self.window, bg="#e2e8f0", height=40)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        footer_label = Label(footer_frame, text="🕉️ Traditional Panchangam Calculations", 
                            font=("Arial", 10), bg="#e2e8f0", fg="#64748b")
        footer_label.pack(pady=10)

    def on_date_select(self, event=None):
        """Handle calendar date selection"""
        try:
            selected_date = self.calendar.selection_get()
            self.show_panchangam_for_date(selected_date)
        except Exception as e:
            messagebox.showerror("Error", f"Date selection error: {str(e)}")

    def show_panchangam_for_date(self, date):
        """Calculate and display Panchangam for selected date"""
        # Clear previous content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Update selected date display
        date_str = date.strftime("%A, %B %d, %Y")
        self.selected_date_var.set(f"📅 {date_str}")
        
        try:
            # Calculate panchangam using simplified methods
            panchangam_data = self.calculate_simple_panchangam(date)
            
            # Display panchangam details
            self.display_panchangam_details(panchangam_data)
            
        except Exception as e:
            error_label = Label(self.scrollable_frame, 
                               text=f"Error calculating Panchangam: {str(e)}", 
                               font=("Arial", 12), bg="white", fg="red", wraplength=400)
            error_label.pack(pady=20)

    def calculate_simple_panchangam(self, date):
        """Calculate Panchangam using simplified astronomical methods"""
        
        # Calculate Julian Day Number
        jdn = self.date_to_jdn(date)
        
        # Calculate basic lunar information
        lunar_info = self.calculate_lunar_info(jdn)
        
        # Calculate Tithi
        tithi = self.calculate_tithi_simple(lunar_info['moon_phase'])
        
        # Calculate Nakshatra based on date pattern
        nakshatra = self.calculate_nakshatra_simple(jdn)
        
        # Calculate Yoga
        yoga = self.calculate_yoga_simple(jdn)
        
        # Calculate Karana
        karana = self.calculate_karana_simple(lunar_info['moon_phase'])
        
        # Get weekday (Vara)
        vara = self.get_vara(date.weekday())
        
        # Approximate sunrise/sunset times
        sunrise_sunset = self.calculate_sunrise_sunset(date)
        
        return {
            'date': date,
            'sunrise': sunrise_sunset['sunrise'],
            'sunset': sunrise_sunset['sunset'],
            'tithi': tithi,
            'nakshatra': nakshatra,
            'yoga': yoga,
            'karana': karana,
            'vara': vara,
            'moon_phase': f"{lunar_info['moon_phase']:.1f}°"
        }

    def date_to_jdn(self, date):
        """Convert date to Julian Day Number"""
        a = (14 - date.month) // 12
        y = date.year + 4800 - a
        m = date.month + 12 * a - 3
        jdn = date.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
        return jdn

    def calculate_lunar_info(self, jdn):
        """Calculate basic lunar information"""
        # Simplified lunar phase calculation
        days_since_new_moon = (jdn - 2451550.1) % 29.53058867  # Approximate lunar cycle
        moon_phase = (days_since_new_moon / 29.53058867) * 360
        
        return {
            'moon_phase': moon_phase,
            'days_since_new_moon': days_since_new_moon
        }

    def calculate_tithi_simple(self, moon_phase):
        """Calculate Tithi using simplified method"""
        tithi_num = int(moon_phase / 12) + 1
        if tithi_num > 30:
            tithi_num = 30
            
        tithi_names = [
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
            "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
            "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
            "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
            "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
        ]
        
        if tithi_num <= 15:
            paksha = "Shukla Paksha"
        else:
            paksha = "Krishna Paksha"
            tithi_num -= 15
            
        return f"{tithi_names[tithi_num - 1]} ({paksha})"

    def calculate_nakshatra_simple(self, jdn):
        """Calculate Nakshatra using date-based method"""
        nakshatra_num = ((jdn - 2451545) % 27) + 1
        nakshatra_num = int(nakshatra_num)
        
        nakshatra_names = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
            "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
            "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
            "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
            "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
            "Uttara Bhadrapada", "Revati"
        ]
        
        return nakshatra_names[nakshatra_num - 1]

    def calculate_yoga_simple(self, jdn):
        """Calculate Yoga using simplified method"""
        yoga_num = ((jdn - 2451545) % 27) + 1
        yoga_num = int(yoga_num)
        
        yoga_names = [
            "Vishkambha", "Preeti", "Ayushman", "Saubhagya", "Shobhana",
            "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
            "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
            "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva",
            "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
            "Indra", "Vaidhriti"
        ]
        
        return yoga_names[yoga_num - 1]

    def calculate_karana_simple(self, moon_phase):
        """Calculate Karana using simplified method"""
        karana_num = int(moon_phase / 6) + 1
        if karana_num > 60:
            karana_num = karana_num % 60
            
        karana_names = [
            "Bava", "Balava", "Kaulava", "Taitila", "Gara",
            "Vanija", "Vishti (Bhadra)", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
        ]
        
        # Simplify to common karanas
        simple_karana_num = karana_num % 7
        return karana_names[simple_karana_num]

    def get_vara(self, weekday):
        """Get Vara (weekday)"""
        vara_names = [
            "Somavara (Monday)", "Mangalavara (Tuesday)", "Budhavara (Wednesday)",
            "Guruvara (Thursday)", "Shukravara (Friday)", "Shanivara (Saturday)",
            "Ravivar (Sunday)"
        ]
        return vara_names[weekday]

    def calculate_sunrise_sunset(self, date):
        """Calculate approximate sunrise and sunset times"""
        # Approximate times for Delhi (you can adjust for other locations)
        sunrise_base = 6.0  # 6:00 AM base
        sunset_base = 18.0  # 6:00 PM base
        
        # Seasonal adjustment (very simplified)
        day_of_year = date.timetuple().tm_yday
        seasonal_offset = math.sin(2 * math.pi * (day_of_year - 81) / 365) * 1.5
        
        sunrise_time = sunrise_base - seasonal_offset
        sunset_time = sunset_base + seasonal_offset
        
        def time_to_string(time_float):
            hours = int(time_float)
            minutes = int((time_float - hours) * 60)
            return f"{hours:02d}:{minutes:02d}"
        
        return {
            'sunrise': time_to_string(sunrise_time),
            'sunset': time_to_string(sunset_time)
        }

    def display_panchangam_details(self, data):
        """Display calculated Panchangam details"""
        
        # Create sections for better organization
        sections = [
            ("🌅 Time Details", [
                ("Sunrise (Approx)", data['sunrise']),
                ("Sunset (Approx)", data['sunset'])
            ]),
            ("🌙 Panchangam Elements", [
                ("Tithi", data['tithi']),
                ("Nakshatra", data['nakshatra']),
                ("Yoga", data['yoga']),
                ("Karana", data['karana']),
                ("Vara (Weekday)", data['vara'])
            ]),
            ("🌟 Additional Information", [
                ("Moon Phase", data['moon_phase']),
                ("Calculation Method", "Simplified Traditional")
            ])
        ]
        
        for section_title, items in sections:
            # Section header
            section_frame = Frame(self.scrollable_frame, bg="#f1f5f9", relief="solid", bd=1)
            section_frame.pack(fill="x", padx=10, pady=10)
            
            section_label = Label(section_frame, text=section_title, 
                                 font=("Arial", 14, "bold"), bg="#f1f5f9", fg="#1e293b")
            section_label.pack(pady=10)
            
            # Items in section
            for item_name, item_value in items:
                item_frame = Frame(self.scrollable_frame, bg="white")
                item_frame.pack(fill="x", padx=20, pady=2)
                
                Label(item_frame, text=f"{item_name}:", font=("Arial", 12, "bold"), 
                     bg="white", fg="#374151").pack(side="left")
                
                Label(item_frame, text=str(item_value), font=("Arial", 12), 
                     bg="white", fg="#059669").pack(side="right")

        # Add disclaimer
        disclaimer_frame = Frame(self.scrollable_frame, bg="#fef3c7", relief="solid", bd=1)
        disclaimer_frame.pack(fill="x", padx=10, pady=20)
        
        disclaimer_label = Label(disclaimer_frame, 
                                text="⚠️ Note: These calculations use simplified traditional methods.\nFor precise astronomical calculations, Swiss Ephemeris is recommended.", 
                                font=("Arial", 10), bg="#fef3c7", fg="#92400e", 
                                wraplength=400, justify="center")
        disclaimer_label.pack(pady=10)

    def back_to_dashboard(self):
        """Return to the main dashboard"""
        try:
            self.window.destroy()
            import homepage
            dashboard_root = Tk()
            homepage.PanchangamDashboard(dashboard_root, self.user_email)
            dashboard_root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return to dashboard: {str(e)}")

# Test the Panchangam page independently
if __name__ == "__main__":
    root = Tk()
    app = PanchangamPage(root, "test@example.com")
    root.mainloop()
