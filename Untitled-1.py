"""
Visual Circuit Designer and Calculator
A comprehensive circuit simulation program with GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

class Component:
    """Base class for all circuit components"""
    def __init__(self, x, y, comp_type, value=0):
        self.x = x
        self.y = y
        self.type = comp_type
        self.value = value
        self.connections = []
        self.selected = False
        
    def draw(self, canvas):
        """Draw the component on canvas"""
        color = "yellow" if self.selected else "lightblue"
        
        if self.type == "resistor":
            # Draw resistor as zigzag
            canvas.create_rectangle(self.x-30, self.y-10, self.x+30, self.y+10, 
                                  fill=color, outline="black", width=2, tags="component")
            canvas.create_text(self.x, self.y-25, text=f"R: {self.value}Ω", 
                             font=("Arial", 9), tags="component")
            
        elif self.type == "battery":
            # Draw battery
            canvas.create_line(self.x-20, self.y-15, self.x-20, self.y+15, 
                             width=4, fill="red", tags="component")
            canvas.create_line(self.x+20, self.y-10, self.x+20, self.y+10, 
                             width=2, fill="black", tags="component")
            canvas.create_text(self.x, self.y-25, text=f"V: {self.value}V", 
                             font=("Arial", 9), tags="component")
            
        elif self.type == "led":
            # Draw LED as triangle
            points = [self.x-15, self.y+10, self.x+15, self.y+10, self.x, self.y-15]
            canvas.create_polygon(points, fill=color, outline="black", 
                                width=2, tags="component")
            canvas.create_text(self.x, self.y-25, text="LED", 
                             font=("Arial", 9), tags="component")
            
        elif self.type == "capacitor":
            # Draw capacitor
            canvas.create_line(self.x-5, self.y-15, self.x-5, self.y+15, 
                             width=3, fill="black", tags="component")
            canvas.create_line(self.x+5, self.y-15, self.x+5, self.y+15, 
                             width=3, fill="black", tags="component")
            canvas.create_text(self.x, self.y-25, text=f"C: {self.value}µF", 
                             font=("Arial", 9), tags="component")
            
        elif self.type in ["AND", "OR", "NOT", "NAND", "NOR", "XOR"]:
            # Draw logic gate
            canvas.create_rectangle(self.x-30, self.y-20, self.x+30, self.y+20, 
                                  fill=color, outline="black", width=2, tags="component")
            canvas.create_text(self.x, self.y, text=self.type, 
                             font=("Arial", 10, "bold"), tags="component")
        
        # Draw connection points
        canvas.create_oval(self.x-3, self.y-3, self.x+3, self.y+3, 
                         fill="red", outline="black", tags="component")

class Wire:
    """Represents a wire connection between components"""
    def __init__(self, comp1, comp2):
        self.comp1 = comp1
        self.comp2 = comp2
        
    def draw(self, canvas):
        """Draw the wire"""
        canvas.create_line(self.comp1.x, self.comp1.y, 
                         self.comp2.x, self.comp2.y,
                         width=2, fill="blue", tags="wire")

class CircuitSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual Circuit Designer & Calculator")
        self.root.geometry("1200x800")
        
        self.components = []
        self.wires = []
        self.selected_component = None
        self.dragging = False
        self.connecting = False
        self.connect_start = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Component toolbar
        left_panel = ttk.Frame(main_frame, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Title
        ttk.Label(left_panel, text="Circuit Components", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Component buttons
        ttk.Label(left_panel, text="Basic Components:", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        ttk.Button(left_panel, text="Add Resistor", 
                  command=lambda: self.add_component("resistor")).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Add Battery", 
                  command=lambda: self.add_component("battery")).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Add LED", 
                  command=lambda: self.add_component("led")).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Add Capacitor", 
                  command=lambda: self.add_component("capacitor")).pack(fill=tk.X, pady=2)
        
        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Label(left_panel, text="Logic Gates:", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        for gate in ["AND", "OR", "NOT", "NAND", "NOR", "XOR"]:
            ttk.Button(left_panel, text=f"Add {gate} Gate", 
                      command=lambda g=gate: self.add_component(g)).pack(fill=tk.X, pady=2)
        
        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Label(left_panel, text="Actions:", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        ttk.Button(left_panel, text="Connect Components", 
                  command=self.start_connecting).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Calculate Circuit", 
                  command=self.calculate_circuit).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Delete Selected", 
                  command=self.delete_selected).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Clear All", 
                  command=self.clear_canvas).pack(fill=tk.X, pady=2)
        
        # Canvas for circuit drawing
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(canvas_frame, text="Circuit Design Area", 
                 font=("Arial", 12, "bold")).pack(pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", 
                               relief=tk.SUNKEN, borderwidth=2)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
        # Right panel - Results
        right_panel = ttk.Frame(main_frame, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        ttk.Label(right_panel, text="Circuit Analysis", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Results text area
        self.results_text = tk.Text(right_panel, height=30, width=35, 
                                   font=("Courier", 9))
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(right_panel, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        # Instructions
        instructions = """
        === INSTRUCTIONS ===
        
        1. Click component buttons to add
        2. Click and drag to move
        3. Click 'Connect Components'
        4. Click two components to wire
        5. Click 'Calculate Circuit'
        
        Results will appear here!
        """
        self.results_text.insert("1.0", instructions)
        
    def add_component(self, comp_type):
        """Add a new component to the circuit"""
        # Prompt for value
        value = 0
        if comp_type == "resistor":
            value = self.prompt_value("Enter resistance (Ω):", 100)
        elif comp_type == "battery":
            value = self.prompt_value("Enter voltage (V):", 9)
        elif comp_type == "capacitor":
            value = self.prompt_value("Enter capacitance (µF):", 10)
        
        # Add component at center of canvas
        x = self.canvas.winfo_width() // 2
        y = self.canvas.winfo_height() // 2
        
        component = Component(x, y, comp_type, value)
        self.components.append(component)
        self.redraw()
        
    def prompt_value(self, message, default):
        """Prompt user for component value"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Component Value")
        dialog.geometry("300x100")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=message).pack(pady=10)
        
        entry = ttk.Entry(dialog)
        entry.insert(0, str(default))
        entry.pack(pady=5)
        entry.focus()
        
        result = [default]
        
        def on_ok():
            try:
                result[0] = float(entry.get())
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
        
        def on_enter(event):
            on_ok()
        
        entry.bind("<Return>", on_enter)
        
        ttk.Button(dialog, text="OK", command=on_ok).pack(pady=5)
        
        dialog.wait_window()
        return result[0]
    
    def on_canvas_click(self, event):
        """Handle canvas click"""
        if self.connecting:
            # Connecting mode
            component = self.find_component_at(event.x, event.y)
            if component:
                if self.connect_start is None:
                    self.connect_start = component
                    component.selected = True
                    self.redraw()
                else:
                    # Create wire
                    if self.connect_start != component:
                        wire = Wire(self.connect_start, component)
                        self.wires.append(wire)
                        self.connect_start.connections.append(component)
                        component.connections.append(self.connect_start)
                    
                    self.connect_start.selected = False
                    self.connect_start = None
                    self.connecting = False
                    self.redraw()
        else:
            # Selection mode
            component = self.find_component_at(event.x, event.y)
            if component:
                # Deselect all
                for comp in self.components:
                    comp.selected = False
                component.selected = True
                self.selected_component = component
                self.dragging = True
                self.redraw()
    
    def on_canvas_drag(self, event):
        """Handle canvas drag"""
        if self.dragging and self.selected_component:
            self.selected_component.x = event.x
            self.selected_component.y = event.y
            self.redraw()
    
    def on_canvas_release(self, event):
        """Handle canvas release"""
        self.dragging = False
    
    def find_component_at(self, x, y):
        """Find component at given coordinates"""
        for component in self.components:
            if abs(component.x - x) < 40 and abs(component.y - y) < 30:
                return component
        return None
    
    def start_connecting(self):
        """Start connection mode"""
        self.connecting = True
        self.connect_start = None
        messagebox.showinfo("Connect Mode", 
                          "Click on two components to connect them with a wire")
    
    def delete_selected(self):
        """Delete selected component"""
        if self.selected_component:
            # Remove wires connected to this component
            self.wires = [w for w in self.wires 
                         if w.comp1 != self.selected_component 
                         and w.comp2 != self.selected_component]
            
            # Remove from components list
            self.components.remove(self.selected_component)
            self.selected_component = None
            self.redraw()
    
    def clear_canvas(self):
        """Clear all components"""
        if messagebox.askyesno("Clear All", "Are you sure you want to clear the circuit?"):
            self.components = []
            self.wires = []
            self.selected_component = None
            self.redraw()
            self.results_text.delete("1.0", tk.END)
    
    def redraw(self):
        """Redraw the entire canvas"""
        self.canvas.delete("all")
        
        # Draw grid
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        for i in range(0, width, 50):
            self.canvas.create_line(i, 0, i, height, fill="lightgray")
        for i in range(0, height, 50):
            self.canvas.create_line(0, i, width, i, fill="lightgray")
        
        # Draw wires first
        for wire in self.wires:
            wire.draw(self.canvas)
        
        # Draw components
        for component in self.components:
            component.draw(self.canvas)
    
    def calculate_circuit(self):
        """Calculate circuit parameters"""
        self.results_text.delete("1.0", tk.END)
        
        output = "=== CIRCUIT ANALYSIS ===\n\n"
        
        # Count components
        resistors = [c for c in self.components if c.type == "resistor"]
        batteries = [c for c in self.components if c.type == "battery"]
        leds = [c for c in self.components if c.type == "led"]
        capacitors = [c for c in self.components if c.type == "capacitor"]
        gates = [c for c in self.components if c.type in ["AND", "OR", "NOT", "NAND", "NOR", "XOR"]]
        
        output += f"Components:\n"
        output += f"  Resistors: {len(resistors)}\n"
        output += f"  Batteries: {len(batteries)}\n"
        output += f"  LEDs: {len(leds)}\n"
        output += f"  Capacitors: {len(capacitors)}\n"
        output += f"  Logic Gates: {len(gates)}\n"
        output += f"  Wires: {len(self.wires)}\n\n"
        
        # Basic circuit analysis
        if batteries and resistors:
            output += "=== SERIES CIRCUIT ANALYSIS ===\n\n"
            
            # Calculate total resistance (assuming series)
            total_r = sum(r.value for r in resistors)
            output += f"Total Resistance: {total_r:.2f} Ω\n"
            
            # Calculate voltage (sum of batteries)
            total_v = sum(b.value for b in batteries)
            output += f"Total Voltage: {total_v:.2f} V\n"
            
            # Calculate current (Ohm's Law: I = V/R)
            if total_r > 0:
                current = total_v / total_r
                output += f"Current: {current:.4f} A ({current*1000:.2f} mA)\n"
                
                # Calculate power (P = V * I)
                power = total_v * current
                output += f"Total Power: {power:.4f} W\n\n"
                
                # Voltage drop across each resistor
                output += "Voltage drops:\n"
                for i, r in enumerate(resistors, 1):
                    v_drop = current * r.value
                    output += f"  R{i} ({r.value}Ω): {v_drop:.2f} V\n"
                
                output += "\n"
                
                # LED analysis
                if leds:
                    output += "LED Analysis:\n"
                    led_voltage = 2.0  # Typical LED forward voltage
                    for i, led in enumerate(leds, 1):
                        output += f"  LED{i}: ~{led_voltage}V forward voltage\n"
                        output += f"         Current: {current*1000:.2f} mA\n"
                        if current > 0.03:  # 30mA
                            output += "         ⚠️ WARNING: High current!\n"
                        elif current < 0.005:  # 5mA
                            output += "         ⚠️ May be dim\n"
                        else:
                            output += "         ✓ Safe operating range\n"
                    output += "\n"
        
        # Parallel circuit hint
        if len(resistors) > 1:
            output += "=== PARALLEL ANALYSIS ===\n\n"
            output += "If resistors are in parallel:\n"
            parallel_r = 1 / sum(1/r.value for r in resistors if r.value > 0)
            output += f"Equivalent Resistance: {parallel_r:.2f} Ω\n\n"
        
        # Capacitor analysis
        if capacitors:
            output += "=== CAPACITOR ANALYSIS ===\n\n"
            total_c_series = 1 / sum(1/c.value for c in capacitors if c.value > 0)
            total_c_parallel = sum(c.value for c in capacitors)
            output += f"If in series: {total_c_series:.2f} µF\n"
            output += f"If in parallel: {total_c_parallel:.2f} µF\n\n"
        
        # Logic gates
        if gates:
            output += "=== LOGIC GATES ===\n\n"
            for i, gate in enumerate(gates, 1):
                output += f"{gate.type} Gate #{i}\n"
                output += f"  Truth table for {gate.type}:\n"
                
                if gate.type == "NOT":
                    output += "    A | Y\n"
                    output += "    0 | 1\n"
                    output += "    1 | 0\n"
                elif gate.type == "AND":
                    output += "    A B | Y\n"
                    output += "    0 0 | 0\n"
                    output += "    0 1 | 0\n"
                    output += "    1 0 | 0\n"
                    output += "    1 1 | 1\n"
                elif gate.type == "OR":
                    output += "    A B | Y\n"
                    output += "    0 0 | 0\n"
                    output += "    0 1 | 1\n"
                    output += "    1 0 | 1\n"
                    output += "    1 1 | 1\n"
                elif gate.type == "NAND":
                    output += "    A B | Y\n"
                    output += "    0 0 | 1\n"
                    output += "    0 1 | 1\n"
                    output += "    1 0 | 1\n"
                    output += "    1 1 | 0\n"
                elif gate.type == "NOR":
                    output += "    A B | Y\n"
                    output += "    0 0 | 1\n"
                    output += "    0 1 | 0\n"
                    output += "    1 0 | 0\n"
                    output += "    1 1 | 0\n"
                elif gate.type == "XOR":
                    output += "    A B | Y\n"
                    output += "    0 0 | 0\n"
                    output += "    0 1 | 1\n"
                    output += "    1 0 | 1\n"
                    output += "    1 1 | 0\n"
                output += "\n"
        
        # General formulas
        output += "=== USEFUL FORMULAS ===\n\n"
        output += "Ohm's Law: V = I × R\n"
        output += "Power: P = V × I = I²R = V²/R\n"
        output += "Series R: R_total = R1 + R2 + ...\n"
        output += "Parallel R: 1/R_total = 1/R1 + 1/R2 + ...\n"
        output += "Series C: 1/C_total = 1/C1 + 1/C2 + ...\n"
        output += "Parallel C: C_total = C1 + C2 + ...\n"
        
        self.results_text.insert("1.0", output)

def main():
    root = tk.Tk()
    app = CircuitSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()