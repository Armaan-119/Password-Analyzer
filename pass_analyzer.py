import tkinter as tk
from tkinter import ttk
import re
import math

class PasswordAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Analyzer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variables
        self.password_var = tk.StringVar()
        self.show_password = tk.BooleanVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Password Strength Analyzer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Password input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(input_frame, text="Enter Password:").grid(row=0, column=0, sticky=tk.W)
        
        self.password_entry = ttk.Entry(input_frame, textvariable=self.password_var, 
                                       show="*", width=40, font=("Arial", 10))
        self.password_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        self.password_entry.bind('<KeyRelease>', self.on_password_change)
        
        # Show/Hide password checkbox
        show_check = ttk.Checkbutton(input_frame, text="Show Password", 
                                    variable=self.show_password, 
                                    command=self.toggle_password_visibility)
        show_check.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          pady=(20, 0))
        
        # Strength indicator
        ttk.Label(results_frame, text="Strength:").grid(row=0, column=0, sticky=tk.W)
        self.strength_label = ttk.Label(results_frame, text="", font=("Arial", 10, "bold"))
        self.strength_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Progress bar for strength
        self.strength_progress = ttk.Progressbar(results_frame, length=300, mode='determinate')
        self.strength_progress.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                                   pady=(5, 10))
        
        # Crack time
        ttk.Label(results_frame, text="Estimated crack time:").grid(row=2, column=0, sticky=tk.W)
        self.crack_time_label = ttk.Label(results_frame, text="", font=("Arial", 10))
        self.crack_time_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # Suggestions frame
        suggestions_frame = ttk.LabelFrame(results_frame, text="Suggestions", padding="10")
        suggestions_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                              pady=(10, 0))
        
        # Suggestions text widget
        self.suggestions_text = tk.Text(suggestions_frame, height=8, width=60, 
                                       wrap=tk.WORD, font=("Arial", 9))
        suggestions_scrollbar = ttk.Scrollbar(suggestions_frame, orient="vertical", 
                                            command=self.suggestions_text.yview)
        self.suggestions_text.configure(yscrollcommand=suggestions_scrollbar.set)
        
        self.suggestions_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        suggestions_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(0, weight=1)
        results_frame.columnconfigure(1, weight=1)
        suggestions_frame.columnconfigure(0, weight=1)
        suggestions_frame.rowconfigure(0, weight=1)
        
    def toggle_password_visibility(self):
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def on_password_change(self, event=None):
        password = self.password_var.get()
        if password:
            self.analyze_password(password)
        else:
            self.clear_results()
    
    def analyze_password(self, password):
        # Calculate strength score
        score, checks = self.calculate_strength(password)
        
        # Update strength display
        self.update_strength_display(score)
        
        # Calculate crack time
        crack_time = self.calculate_crack_time(password)
        self.crack_time_label.config(text=crack_time)
        
        # Generate suggestions
        suggestions = self.generate_suggestions(checks, password)
        self.update_suggestions(suggestions)
    
    def calculate_strength(self, password):
        score = 0
        checks = {
            'length': len(password) >= 8,
            'length_good': len(password) >= 12,
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'lowercase': bool(re.search(r'[a-z]', password)),
            'numbers': bool(re.search(r'\d', password)),
            'special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
            'no_common': not self.is_common_password(password),
            'no_sequential': not self.has_sequential_chars(password),
            'no_repeated': not self.has_repeated_chars(password)
        }
        
        # Scoring system
        if checks['length']: score += 10
        if checks['length_good']: score += 10
        if checks['uppercase']: score += 15
        if checks['lowercase']: score += 15
        if checks['numbers']: score += 15
        if checks['special']: score += 20
        if checks['no_common']: score += 10
        if checks['no_sequential']: score += 5
        if checks['no_repeated']: score += 5
        
        # Length bonus
        if len(password) > 12:
            score += min((len(password) - 12) * 2, 20)
        
        return min(score, 100), checks
    
    def is_common_password(self, password):
        common_passwords = [
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey',
            '1234567890', 'password1', '123123', 'qwerty123'
        ]
        return password.lower() in common_passwords
    
    def has_sequential_chars(self, password):
        sequences = ['123', '234', '345', '456', '567', '678', '789',
                    'abc', 'bcd', 'cde', 'def', 'efg', 'fgh', 'ghi']
        password_lower = password.lower()
        return any(seq in password_lower for seq in sequences)
    
    def has_repeated_chars(self, password):
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False
    
    def update_strength_display(self, score):
        self.strength_progress['value'] = score
        
        if score < 30:
            strength_text = "Very Weak"
            color = "red"
        elif score < 50:
            strength_text = "Weak"
            color = "orange"
        elif score < 70:
            strength_text = "Fair"
            color = "yellow"
        elif score < 85:
            strength_text = "Good"
            color = "lightgreen"
        else:
            strength_text = "Strong"
            color = "green"
        
        self.strength_label.config(text=f"{strength_text} ({score}/100)", foreground=color)
    
    def calculate_crack_time(self, password):
        # Character set sizes
        charset_size = 0
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'\d', password):
            charset_size += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            charset_size += 32
        
        if charset_size == 0:
            return "Unable to calculate"
        
        # Total possible combinations
        total_combinations = charset_size ** len(password)
        
        # Average attempts needed (half of total combinations)
        avg_attempts = total_combinations / 2
        
        # Assuming 1 billion attempts per second (modern hardware)
        attempts_per_second = 1_000_000_000
        seconds = avg_attempts / attempts_per_second
        
        return self.format_time(seconds)
    
    def format_time(self, seconds):
        if seconds < 1:
            return "Less than 1 second"
        elif seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.1f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.1f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.1f} days"
        elif seconds < 31536000000:
            return f"{seconds/31536000:.1f} years"
        else:
            return "Millions of years"
    
    def generate_suggestions(self, checks, password):
        suggestions = []
        
        if not checks['length']:
            suggestions.append("• Make your password at least 8 characters long")
        elif not checks['length_good']:
            suggestions.append("• Consider making your password at least 12 characters for better security")
        
        if not checks['uppercase']:
            suggestions.append("• Add at least one uppercase letter (A-Z)")
        
        if not checks['lowercase']:
            suggestions.append("• Add at least one lowercase letter (a-z)")
        
        if not checks['numbers']:
            suggestions.append("• Include at least one number (0-9)")
        
        if not checks['special']:
            suggestions.append("• Add special characters (!@#$%^&* etc.)")
        
        if not checks['no_common']:
            suggestions.append("• Avoid common passwords like 'password' or '123456'")
        
        if not checks['no_sequential']:
            suggestions.append("• Avoid sequential characters like '123' or 'abc'")
        
        if not checks['no_repeated']:
            suggestions.append("• Avoid repeating the same character multiple times")
        
        if len(suggestions) == 0:
            suggestions.append("• Your password looks strong! Consider using a unique password for each account.")
            suggestions.append("• Consider using a password manager to generate and store complex passwords.")
        
        return suggestions
    
    def update_suggestions(self, suggestions):
        self.suggestions_text.delete(1.0, tk.END)
        self.suggestions_text.insert(1.0, "\n".join(suggestions))
    
    def clear_results(self):
        self.strength_label.config(text="")
        self.strength_progress['value'] = 0
        self.crack_time_label.config(text="")
        self.suggestions_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = PasswordAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
