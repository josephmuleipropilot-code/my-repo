import tkinter as tk
from tkinter import font
import math
import cmath

class FX991EXCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Casio fx-991 EX Calculator")
        self.root.geometry("680x900")
        self.root.configure(bg="#2a2a2a")
        self.root.resizable(False, False)
        
        # Variables
        self.display_main = tk.StringVar(value="0")
        self.display_sub = tk.StringVar(value="")
        self.last_result = 0
        self.angle_mode = "DEG"
        self.shift_mode = False
        self.alpha_mode = False
        self.hyp_mode = False
        self.current_op = None
        self.first_operand = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the complete UI"""
        # Top mode indicator
        mode_frame = tk.Frame(self.root, bg="#1a1a1a", height=30)
        mode_frame.pack(fill=tk.X, padx=5, pady=3)
        mode_frame.pack_propagate(False)
        
        self.mode_label = tk.Label(
            mode_frame,
            text=f"[{self.angle_mode}] [NORM]",
            font=("Arial", 9),
            fg="#00ff00",
            bg="#1a1a1a"
        )
        self.mode_label.pack(anchor="w", padx=10, pady=5)
        
        # Main display area
        self.create_display()
        
        # Button area
        self.create_buttons()
    
    def create_display(self):
        """Create dual-line display like fx-991 EX"""
        display_frame = tk.Frame(self.root, bg="#1a1a1a", height=120)
        display_frame.pack(fill=tk.BOTH, padx=8, pady=5)
        display_frame.pack_propagate(False)
        
        # Sub display (formula/previous calculation)
        self.sub_display = tk.Label(
            display_frame,
            textvariable=self.display_sub,
            font=("Courier", 11),
            fg="#666666",
            bg="#1a1a1a",
            justify=tk.RIGHT,
            anchor="e"
        )
        self.sub_display.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        # Main display (result)
        self.main_display = tk.Label(
            display_frame,
            textvariable=self.display_main,
            font=("Courier", 32, "bold"),
            fg="#00ff00",
            bg="#1a1a1a",
            justify=tk.RIGHT,
            anchor="e"
        )
        self.main_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))
    
    def create_buttons(self):
        """Create button layout matching fx-991 EX"""
        button_frame = tk.Frame(self.root, bg="#2a2a2a")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Button layout - actual fx-991 EX layout
        layouts = [
            # Row 1: Mode buttons
            [
                ("SHIFT", self.toggle_shift, "#333333"),
                ("ALPHA", self.toggle_alpha, "#333333"),
                ("MODE", self.open_mode_menu, "#333333"),
                ("SETUP", self.open_setup_menu, "#333333"),
            ],
            # Row 2
            [
                ("CMPLX", self.toggle_complex, "#1a3a7a"),
                ("CALC", self.show_calc_menu, "#1a3a7a"),
                ("∫dx", self.integral_placeholder, "#1a3a7a"),
                ("d/dx", self.derivative_placeholder, "#1a3a7a"),
            ],
            # Row 3: Trig and logs
            [
                ("sin", self.sin_func, "#1a3a7a"),
                ("cos", self.cos_func, "#1a3a7a"),
                ("tan", self.tan_func, "#1a3a7a"),
                ("π", self.insert_pi, "#8B4513"),
            ],
            # Row 4
            [
                ("sin⁻¹", self.asin_func, "#1a3a7a"),
                ("cos⁻¹", self.acos_func, "#1a3a7a"),
                ("tan⁻¹", self.atan_func, "#1a3a7a"),
                ("e", self.insert_e, "#8B4513"),
            ],
            # Row 5
            [
                ("sinh", self.sinh_func, "#1a3a7a"),
                ("cosh", self.cosh_func, "#1a3a7a"),
                ("tanh", self.tanh_func, "#1a3a7a"),
                ("^", self.power_op, "#ff6600"),
            ],
            # Row 6
            [
                ("log", self.log_func, "#1a3a7a"),
                ("ln", self.ln_func, "#1a3a7a"),
                ("log₍", self.logbase_func, "#1a3a7a"),
                ("!", self.factorial_func, "#ff6600"),
            ],
            # Row 7
            [
                ("√", self.sqrt_func, "#1a3a7a"),
                ("∛", self.cbrt_func, "#1a3a7a"),
                ("ˣ√", self.nroot_func, "#1a3a7a"),
                ("÷", self.divide_op, "#ff6600"),
            ],
            # Row 8
            [
                ("Pol(", self.polar_func, "#1a3a7a"),
                ("Rec(", self.rect_func, "#1a3a7a"),
                ("GCD", self.gcd_func, "#1a3a7a"),
                ("×", self.multiply_op, "#ff6600"),
            ],
            # Row 9
            [
                ("7", self.digit_click, "#505050"),
                ("8", self.digit_click, "#505050"),
                ("9", self.digit_click, "#505050"),
                ("−", self.subtract_op, "#ff6600"),
            ],
            # Row 10
            [
                ("4", self.digit_click, "#505050"),
                ("5", self.digit_click, "#505050"),
                ("6", self.digit_click, "#505050"),
                ("+", self.add_op, "#ff6600"),
            ],
            # Row 11
            [
                ("1", self.digit_click, "#505050"),
                ("2", self.digit_click, "#505050"),
                ("3", self.digit_click, "#505050"),
                ("=", self.equals_press, "#ff3300"),
            ],
            # Row 12
            [
                ("0", self.digit_click, "#505050"),
                (".", self.decimal_click, "#505050"),
                ("×10ˣ", self.exp10_func, "#8B4513"),
                ("DEL", self.delete_last, "#ff3300"),
            ],
            # Row 13
            [
                ("(", self.open_paren, "#505050"),
                (")", self.close_paren, "#505050"),
                ("Ans", self.insert_ans, "#8B4513"),
                ("AC", self.all_clear, "#ff3300"),
            ],
        ]
        
        for row_layout in layouts:
            row_frame = tk.Frame(button_frame, bg="#2a2a2a")
            row_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
            
            for btn_text, cmd, color in row_layout:
                self.create_button(row_frame, btn_text, cmd, color)
    
    def create_button(self, parent, text, command, color):
        """Create styled button"""
        btn_font = font.Font(family="Arial", size=9, weight="bold")
        
        btn = tk.Button(
            parent,
            text=text,
            font=btn_font,
            bg=color,
            fg="white" if color != "#505050" else "#00ff00",
            activebackground="#555555",
            relief=tk.RAISED,
            bd=1,
            command=command,
            padx=2,
            pady=2
        )
        btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)
    
    def update_display(self, value):
        """Update main display"""
        self.display_main.set(str(value))
        self.last_result = float(value) if isinstance(value, (int, float)) else 0
    
    def update_sub_display(self, value):
        """Update sub display"""
        self.display_sub.set(str(value))
    
    def digit_click(self):
        """Handle digit button clicks"""
        btn = self.root.focus_get()
        digit = btn.cget("text")
        
        current = self.display_main.get()
        if current == "0" and digit != ".":
            self.display_main.set(digit)
        else:
            self.display_main.set(current + digit)
    
    def decimal_click(self):
        """Handle decimal point"""
        current = self.display_main.get()
        if "." not in current:
            self.display_main.set(current + ".")
    
    def open_paren(self):
        """Open parenthesis"""
        current = self.display_main.get()
        if current == "0":
            self.display_main.set("(")
        else:
            self.display_main.set(current + "(")
    
    def close_paren(self):
        """Close parenthesis"""
        self.display_main.set(self.display_main.get() + ")")
    
    def delete_last(self):
        """Delete last character"""
        current = self.display_main.get()
        if len(current) > 1:
            self.display_main.set(current[:-1])
        else:
            self.display_main.set("0")
    
    def all_clear(self):
        """Clear all"""
        self.display_main.set("0")
        self.display_sub.set("")
        self.current_op = None
        self.first_operand = None
        self.shift_mode = False
        self.alpha_mode = False
    
    # Operator functions
    def add_op(self):
        self.set_operator("+")
    
    def subtract_op(self):
        self.set_operator("−")
    
    def multiply_op(self):
        self.set_operator("×")
    
    def divide_op(self):
        self.set_operator("÷")
    
    def power_op(self):
        self.set_operator("^")
    
    def set_operator(self, op):
        """Set operator for calculation"""
        try:
            current = self.display_main.get()
            if self.first_operand is None:
                self.first_operand = float(self.eval_expression(current))
            else:
                # Calculate intermediate result
                second = float(self.eval_expression(current))
                result = self.perform_operation(self.first_operand, second, self.current_op)
                self.first_operand = result
                self.update_display(self.format_result(result))
            
            self.current_op = op
            self.update_sub_display(f"{self.first_operand} {op}")
            self.display_main.set("0")
        except:
            self.display_main.set("Error")
    
    def equals_press(self):
        """Calculate result"""
        try:
            if self.current_op and self.first_operand is not None:
                second = float(self.eval_expression(self.display_main.get()))
                result = self.perform_operation(self.first_operand, second, self.current_op)
                
                self.update_sub_display(f"{self.first_operand} {self.current_op} {second}")
                self.update_display(self.format_result(result))
                
                self.first_operand = result
                self.current_op = None
            else:
                # Just evaluate expression
                result = float(self.eval_expression(self.display_main.get()))
                self.update_display(self.format_result(result))
                self.last_result = result
        except:
            self.display_main.set("Error")
    
    def perform_operation(self, a, b, op):
        """Perform mathematical operation"""
        if op == "+":
            return a + b
        elif op == "−":
            return a - b
        elif op == "×":
            return a * b
        elif op == "÷":
            return a / b if b != 0 else float('inf')
        elif op == "^":
            return a ** b
        return 0
    
    def eval_expression(self, expr):
        """Safely evaluate mathematical expression"""
        try:
            # Replace custom operators with Python equivalents
            expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
            return eval(expr)
        except:
            return 0
    
    def format_result(self, result):
        """Format result for display"""
        if isinstance(result, complex):
            return f"{result.real:.10g} + {result.imag:.10g}i"
        elif isinstance(result, float):
            if result == int(result):
                return str(int(result))
            else:
                return f"{result:.10g}"
        return str(result)
    
    # Trigonometric functions
    def sin_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            if self.angle_mode == "DEG":
                val = math.radians(val)
            result = math.sin(val)
            self.update_display(self.format_result(result))
            self.update_sub_display(f"sin({self.display_main.get()})")
        except:
            self.display_main.set("Error")
    
    def cos_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            if self.angle_mode == "DEG":
                val = math.radians(val)
            result = math.cos(val)
            self.update_display(self.format_result(result))
            self.update_sub_display(f"cos({self.display_main.get()})")
        except:
            self.display_main.set("Error")
    
    def tan_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            if self.angle_mode == "DEG":
                val = math.radians(val)
            result = math.tan(val)
            self.update_display(self.format_result(result))
            self.update_sub_display(f"tan({self.display_main.get()})")
        except:
            self.display_main.set("Error")
    
    def asin_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            result = math.asin(val)
            if self.angle_mode == "DEG":
                result = math.degrees(result)
            self.update_display(self.format_result(result))
        except:
            self.display_main.set("Error")
    
    def acos_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            result = math.acos(val)
            if self.angle_mode == "DEG":
                result = math.degrees(result)
            self.update_display(self.format_result(result))
        except:
            self.display_main.set("Error")
    
    def atan_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            result = math.atan(val)
            if self.angle_mode == "DEG":
                result = math.degrees(result)
            self.update_display(self.format_result(result))
        except:
            self.display_main.set("Error")
    
    def sinh_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            result = math.sinh(val)
            self.update_display(self.format_result(result))
        except:
            self.display_main.set("Error")
    
    def cosh_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            result = math.cosh(val)
            self.update_display(self.format_result(result))
        except:
            self.display_main.set("Error")
    
    def tanh_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            result = math.tanh(val)
            self.update_display(self.format_result(result))
        except:
            self.display_main.set("Error")
    
    # Logarithmic functions
    def log_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            result = math.log10(val)
            self.update_display(self.format_result(result))
            self.update_sub_display(f"log({val})")
        except:
            self.display_main.set("Error")
    
    def ln_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            result = math.log(val)
            self.update_display(self.format_result(result))
            self.update_sub_display(f"ln({val})")
        except:
            self.display_main.set("Error")
    
    def logbase_func(self):
        """Logarithm with custom base"""
        self.display_main.set(self.display_main.get() + "log(")
    
    # Power and root functions
    def sqrt_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            result = math.sqrt(val)
            self.update_display(self.format_result(result))
            self.update_sub_display(f"√({val})")
        except:
            self.display_main.set("Error")
    
    def cbrt_func(self):
        try:
            val = float(self.eval_expression(self.display_main.get()))
            result = val ** (1/3) if val >= 0 else -((-val) ** (1/3))
            self.update_display(self.format_result(result))
            self.update_sub_display(f"∛({val})")
        except:
            self.display_main.set("Error")
    
    def nroot_func(self):
        """Nth root"""
        self.display_main.set(self.display_main.get() + "^(1/")
    
    # Constants
    def insert_pi(self):
        current = self.display_main.get()
        if current == "0":
            self.display_main.set(str(math.pi))
        else:
            self.display_main.set(current + str(math.pi))
    
    def insert_e(self):
        current = self.display_main.get()
        if current == "0":
            self.display_main.set(str(math.e))
        else:
            self.display_main.set(current + str(math.e))
    
    def insert_ans(self):
        current = self.display_main.get()
        if current == "0":
            self.display_main.set(str(self.last_result))
        else:
            self.display_main.set(current + str(self.last_result))
    
    # Other functions
    def factorial_func(self):
        try:
            val = int(float(self.eval_expression(self.display_main.get())))
            result = math.factorial(val)
            self.update_display(result)
            self.update_sub_display(f"{val}!")
        except:
            self.display_main.set("Error")
    
    def exp10_func(self):
        """10 to the power of x"""
        self.display_main.set(self.display_main.get() + "×10^")
    
    def gcd_func(self):
        """GCD placeholder"""
        self.display_main.set("gcd(")
    
    def polar_func(self):
        """Polar coordinate conversion"""
        self.display_main.set("Pol(")
    
    def rect_func(self):
        """Rectangular coordinate conversion"""
        self.display_main.set("Rec(")
    
    # Mode toggles
    def toggle_shift(self):
        self.shift_mode = not self.shift_mode
    
    def toggle_alpha(self):
        self.alpha_mode = not self.alpha_mode
    
    def toggle_complex(self):
        """Toggle complex number mode"""
        pass
    
    def open_mode_menu(self):
        """Open MODE menu"""
        pass
    
    def open_setup_menu(self):
        """Open SETUP menu"""
        pass
    
    def show_calc_menu(self):
        """Show CALC menu"""
        pass
    
    # Placeholders for advanced features
    def integral_placeholder(self):
        self.display_main.set("∫(")
    
    def derivative_placeholder(self):
        self.display_main.set("d/dx(")


if __name__ == "__main__":
    root = tk.Tk()
    calc = FX991EXCalculator(root)
    root.mainloop()
