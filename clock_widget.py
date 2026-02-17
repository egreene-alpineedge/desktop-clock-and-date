import tkinter as tk
from tkinter import font as tkfont
from datetime import datetime

class ClockWidget:
    def __init__(self):
        self.root = tk.Tk()

        # Load custom fonts
        self.load_fonts()

        # Remove window decorations (title bar, borders)
        self.root.overrideredirect(True)

        # Set window size and position
        window_width = 700
        window_height = 900
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = screen_width - window_width
        y_position = 160
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Mars theme colors (matching design.html)
        self.mars = "#c1440e"
        self.mars_bright = "#e85d1a"
        self.dust = "#d4835a"
        self.sky = "#0b0d14"
        self.panel = "#080a12"
        self.text = "#f0ddd0"
        self.text_dim = "#b8a89a"
        self.bg_color = "#0f0a08"

        # Configure root background
        self.root.configure(bg=self.panel)

        # Make background transparent
        self.root.attributes("-transparentcolor", self.panel)

        # Create main container frame without border
        self.main_frame = tk.Frame(
            self.root,
            bg=self.panel,
            highlightthickness=0
        )
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Container for side-by-side Earth and Mars displays
        self.dual_time_container = tk.Frame(self.main_frame, bg=self.panel)
        self.dual_time_container.pack(fill=tk.X, padx=16, pady=(40, 12))

        # Configure two equal-width columns
        self.dual_time_container.grid_columnconfigure(0, weight=1)
        self.dual_time_container.grid_columnconfigure(1, weight=1)

        # Left column: Earth time and date
        self.earth_frame = tk.Frame(self.dual_time_container, bg=self.panel)
        self.earth_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        # Right column: Mars time and date
        self.mars_frame = tk.Frame(self.dual_time_container, bg=self.panel)
        self.mars_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        # Earth time and date display
        self.create_time_display()

        # Mars time and date display
        self.create_mars_time_display()

        # Start the clock update loop
        self.update_clock()

    def load_fonts(self):
        """Load or find appropriate fonts for the widget"""
        available_fonts = list(tkfont.families())

        # Check if our custom fonts are available
        if "Orbitron" in available_fonts:
            self.time_font = "Orbitron"
            print("Using Orbitron font")
        else:
            # Fallback to system fonts
            orbitron_alternatives = ["Cascadia Mono", "Consolas", "Ubuntu Mono", "Courier New"]
            self.time_font = "Consolas"
            for font_name in orbitron_alternatives:
                if font_name in available_fonts:
                    self.time_font = font_name
                    break
            print(f"Using fallback font: {self.time_font}")

        if "Share Tech Mono" in available_fonts:
            self.mono_font = "Share Tech Mono"
            print("Using Share Tech Mono font")
        else:
            self.mono_font = self.time_font

    def create_time_display(self):
        """Create the Earth time and date display section"""
        # Divider with label
        divider_container = tk.Frame(self.earth_frame, bg=self.panel)
        divider_container.pack(fill=tk.X, padx=8, pady=(0, 8))

        # Canvas for the divider line with centered text
        divider_canvas = tk.Canvas(
            divider_container,
            height=20,
            bg=self.panel,
            highlightthickness=0
        )
        divider_canvas.pack(fill=tk.X)

        # Draw the divider line
        divider_canvas.create_line(0, 10, 304, 10, fill=self.mars, width=1)

        # Add centered label
        divider_label = tk.Label(
            divider_container,
            text="EARTH STANDARD TIME",
            font=(self.mono_font, 6),
            fg=self.mars,
            bg=self.panel
        )
        divider_label.place(in_=divider_canvas, relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Main time container (hours:minutes, seconds, AM/PM)
        time_container = tk.Frame(self.earth_frame, bg=self.panel)
        time_container.pack(fill=tk.X, padx=8, pady=(0, 4))

        # Main time frame (hours:minutes)
        time_frame = tk.Frame(time_container, bg=self.panel)
        time_frame.pack(side=tk.LEFT)

        self.time_label = tk.Label(
            time_frame,
            text="00:00",
            font=(self.time_font, 60, "normal"),
            fg=self.text,
            bg=self.panel
        )
        self.time_label.pack()

        # Right side (seconds and AM/PM)
        right_frame = tk.Frame(time_container, bg=self.panel)
        right_frame.pack(side=tk.LEFT, padx=(7, 0), anchor=tk.S, pady=(0, 7))

        self.seconds_label = tk.Label(
            right_frame,
            text="00",
            font=(self.time_font, 18, "normal"),
            fg=self.mars_bright,
            bg=self.panel
        )
        self.seconds_label.pack(anchor=tk.W)

        self.ampm_label = tk.Label(
            right_frame,
            text="AM",
            font=("Segoe UI", 7),
            fg=self.dust,
            bg=self.panel
        )
        self.ampm_label.pack(anchor=tk.W, pady=(6, 0))

        # Date row (Earth)
        date_row = tk.Frame(self.earth_frame, bg=self.panel)
        date_row.pack(fill=tk.X, padx=8, pady=(4, 0))

        # Weekday (left)
        self.weekday_label = tk.Label(
            date_row,
            text="TUESDAY",
            font=(self.time_font, 9),
            fg=self.dust,
            bg=self.panel
        )
        self.weekday_label.pack(side=tk.LEFT)

        # Date (center)
        self.date_label = tk.Label(
            date_row,
            text="February 17",
            font=("Segoe UI", 14, "italic"),
            fg=self.text,
            bg=self.panel
        )
        self.date_label.pack(side=tk.LEFT, padx=(20, 0))

        # Year (right)
        self.year_label = tk.Label(
            date_row,
            text="2026",
            font=(self.mono_font, 10),
            fg=self.text_dim,
            bg=self.panel
        )
        self.year_label.pack(side=tk.RIGHT)

    def create_mars_time_display(self):
        """Create Mars time and date display section"""
        # Divider with label
        mars_divider_container = tk.Frame(self.mars_frame, bg=self.panel)
        mars_divider_container.pack(fill=tk.X, padx=8, pady=(0, 8))

        # Canvas for the divider line with centered text
        mars_divider_canvas = tk.Canvas(
            mars_divider_container,
            height=20,
            bg=self.panel,
            highlightthickness=0
        )
        mars_divider_canvas.pack(fill=tk.X)

        # Draw the divider line
        mars_divider_canvas.create_line(0, 10, 304, 10, fill=self.mars, width=1)

        # Add centered label
        mars_divider_label = tk.Label(
            mars_divider_container,
            text="MARS LOCAL TIME - GALE CRATER",
            font=(self.mono_font, 6),
            fg=self.mars,
            bg=self.panel
        )
        mars_divider_label.place(in_=mars_divider_canvas, relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Mars time display (matching Earth time size)
        mars_time_container = tk.Frame(self.mars_frame, bg=self.panel)
        mars_time_container.pack(fill=tk.X, padx=8, pady=(0, 4))

        # Main Mars time frame (hours:minutes)
        mars_time_frame = tk.Frame(mars_time_container, bg=self.panel)
        mars_time_frame.pack(side=tk.LEFT)

        self.mars_time_label = tk.Label(
            mars_time_frame,
            text="00:00",
            font=(self.time_font, 60, "normal"),
            fg=self.mars_bright,
            bg=self.panel
        )
        self.mars_time_label.pack()

        # Right side (seconds)
        mars_right_frame = tk.Frame(mars_time_container, bg=self.panel)
        mars_right_frame.pack(side=tk.LEFT, padx=(7, 0), anchor=tk.S, pady=(0, 7))

        self.mars_seconds_label = tk.Label(
            mars_right_frame,
            text="00",
            font=(self.time_font, 18, "normal"),
            fg=self.mars_bright,
            bg=self.panel
        )
        self.mars_seconds_label.pack(anchor=tk.W)

        # Mars date row (matching Earth date sizes)
        mars_date_row = tk.Frame(self.mars_frame, bg=self.panel)
        mars_date_row.pack(fill=tk.X, padx=8, pady=(4, 0))

        # Mars weekday (left) - matching Earth weekday size
        self.mars_weekday_label = tk.Label(
            mars_date_row,
            text="SOL SOLIS",
            font=(self.time_font, 9),
            fg=self.dust,
            bg=self.panel
        )
        self.mars_weekday_label.pack(side=tk.LEFT)

        # Mars date (center) - matching Earth date size
        self.mars_date_label = tk.Label(
            mars_date_row,
            text="1 Sagittarius",
            font=("Segoe UI", 14, "italic"),
            fg=self.text,
            bg=self.panel
        )
        self.mars_date_label.pack(side=tk.LEFT, padx=(20, 0))

        # Mars year (right) - same size as Earth year
        self.mars_year_label = tk.Label(
            mars_date_row,
            text="MY 37",
            font=(self.mono_font, 10),
            fg=self.text_dim,
            bg=self.panel
        )
        self.mars_year_label.pack(side=tk.RIGHT)

    def get_martian_sol(self, date):
        """Calculate Martian sol (approximate) for weekday cycle"""
        # J2000 epoch: January 1, 2000, 12:00 TT
        from datetime import datetime as dt
        j2000 = dt(2000, 1, 1, 12, 0, 0)
        days_since_j2000 = (date - j2000).total_seconds() / 86400
        sol = int(days_since_j2000 / 1.02749125) + 44796
        return sol

    def get_mars_local_time(self, earth_datetime):
        """Calculate Mars local solar time for Gale Crater (Curiosity landing site)"""
        # Mars Sol Date calculation
        from datetime import datetime as dt
        j2000 = dt(2000, 1, 1, 12, 0, 0)
        days_since_j2000 = (earth_datetime - j2000).total_seconds() / 86400.0

        # Mars Sol Date (number of Martian days since J2000 epoch)
        msd = (days_since_j2000 - 4.5) / 1.027491252 + 44796.0

        # Gale Crater longitude: 137.4°E
        # Calculate local mean solar time
        gale_longitude = 137.4
        mtc = (24 * msd) % 24  # Coordinated Mars Time (at 0° longitude)
        lmst = (mtc + gale_longitude * 24 / 360) % 24  # Local Mean Solar Time

        # Convert to hours, minutes, seconds
        hours = int(lmst)
        minutes = int((lmst - hours) * 60)
        seconds = int(((lmst - hours) * 60 - minutes) * 60)

        return hours, minutes, seconds

    def get_darian_date(self, earth_datetime):
        """Calculate Darian calendar date from Earth datetime"""
        from datetime import datetime as dt

        # Darian calendar epoch: April 11, 1955 (telescopic observation)
        darian_epoch = dt(1955, 4, 11, 0, 0, 0)

        # Calculate Mars Sol Date
        j2000 = dt(2000, 1, 1, 12, 0, 0)
        days_since_j2000 = (earth_datetime - j2000).total_seconds() / 86400.0
        msd = (days_since_j2000 - 4.5) / 1.027491252 + 44796.0

        # Calculate days since Darian epoch
        days_since_epoch_j2000 = (darian_epoch - j2000).total_seconds() / 86400.0
        msd_epoch = (days_since_epoch_j2000 - 4.5) / 1.027491252 + 44796.0
        sols_since_epoch = msd - msd_epoch

        # Mars year is 668.5907 sols (average)
        mars_year_length = 668.5907
        mars_year = int(sols_since_epoch / mars_year_length) + 1

        # Sol within the year
        sol_in_year = int(sols_since_epoch % mars_year_length)

        # Darian calendar months (24 months)
        month_names = [
            "Sagittarius", "Dhanus", "Capricornus", "Makara",
            "Aquarius", "Kumbha", "Pisces", "Mina",
            "Aries", "Mesha", "Taurus", "Rishabha",
            "Gemini", "Mithuna", "Cancer", "Karka",
            "Leo", "Simha", "Virgo", "Kanya",
            "Libra", "Tula", "Scorpius", "Vrishika"
        ]

        # Month lengths (alternating 28 and 27 sols, with adjustments)
        # Standard year: 668 sols
        month_lengths = [28, 27] * 12  # Alternating pattern

        # Find current month and day
        day_count = sol_in_year
        month_index = 0
        for i, length in enumerate(month_lengths):
            if day_count < length:
                month_index = i
                break
            day_count -= length

        day = day_count + 1
        month_name = month_names[month_index]

        return day, month_name, mars_year

    def update_clock(self):
        """Update the clock display"""
        now = datetime.now()

        # Format time
        hours = now.hour
        minutes = now.minute
        seconds = now.second

        # Determine AM/PM
        ampm = "PM" if hours >= 12 else "AM"

        # Convert to 12-hour format
        hours_12 = hours % 12
        if hours_12 == 0:
            hours_12 = 12

        # Update time labels
        self.time_label.config(text=f"{hours_12:02d}:{minutes:02d}")
        self.seconds_label.config(text=f"{seconds:02d}")
        self.ampm_label.config(text=ampm)

        # Update date labels
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']

        self.weekday_label.config(text=days[now.weekday()].upper())
        self.date_label.config(text=f"{months[now.month - 1]} {now.day}")
        self.year_label.config(text=str(now.year))

        # Update Mars time (split into hours:minutes and seconds)
        mars_h, mars_m, mars_s = self.get_mars_local_time(now)
        self.mars_time_label.config(text=f"{mars_h:02d}:{mars_m:02d}")
        self.mars_seconds_label.config(text=f"{mars_s:02d}")

        # Update Mars date (only update once per second to avoid recalculating)
        if seconds == 0 or not hasattr(self, '_last_mars_date_update'):
            mars_day, mars_month, mars_year = self.get_darian_date(now)

            # Martian weekday names (7-day week)
            mars_weekdays = [
                "Solis",    # Sunday (Sol's day - Sun)
                "Lunae",    # Monday (Luna's day - Moon)
                "Martis",   # Tuesday (Mars' day)
                "Mercurii", # Wednesday (Mercury's day)
                "Jovis",    # Thursday (Jupiter's day)
                "Veneris",  # Friday (Venus' day)
                "Saturni"   # Saturday (Saturn's day)
            ]

            sol = self.get_martian_sol(now)
            mars_weekday = mars_weekdays[sol % 7]
            self.mars_weekday_label.config(text=mars_weekday.upper())
            self.mars_date_label.config(text=f"{mars_day} {mars_month}")
            self.mars_year_label.config(text=f"MY {mars_year}")
            self._last_mars_date_update = seconds

        # Schedule next update (every 100ms for smooth seconds)
        self.root.after(100, self.update_clock)

    def run(self):
        """Start the main event loop"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ClockWidget()
    app.run()
