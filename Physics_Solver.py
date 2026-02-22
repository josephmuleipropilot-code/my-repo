import math


class EquationDefinition:
    def __init__(self, name, variables, solve_rules):
        self.name = name
        self.variables = variables
        self.solve_rules = solve_rules


def make_rule(requires, formula):
    return {"requires": requires, "formula": formula}


def sin_deg(angle):
    return math.sin(math.radians(angle))

# this is just sin inverse
def asin_deg(value):
    if value < -1 or value > 1:
        raise ValueError("No real-angle solution exists for this Snell's law input.")
    return math.degrees(math.asin(value))


def sqrt_checked(value, label):
    if value < 0:
        raise ValueError(f"Cannot solve {label}: square-root input became negative.")
    return math.sqrt(value)


def solve_motion_2_time(values):
    u = values["u"]
    a = values["a"]
    s = values["s"]

    if abs(a) < 1e-12:
        if abs(u) < 1e-12:
            raise ValueError("Cannot solve t: both a and u are zero.")
        return s / u

    discriminant = (u ** 2) + (2 * a * s)
    if discriminant < 0:
        raise ValueError("Cannot solve t: discriminant is negative.")

    root = math.sqrt(discriminant)
    t1 = (-u + root) / a
    t2 = (-u - root) / a

    non_negative = [candidate for candidate in [t1, t2] if candidate >= 0]
    if non_negative:
        return min(non_negative)
    return t1

# looottts of topics
TOPIC_LIBRARY = {
    "Kinematics": [
        EquationDefinition(
            name="1st Equation of Motion (v = u + a*t)",
            variables={
                "v": "Final velocity (m/s)",
                "u": "Initial velocity (m/s)",
                "a": "Acceleration (m/s^2)",
                "t": "Time (s)",
            },
            solve_rules={
                "v": make_rule(["u", "a", "t"], lambda x: x["u"] + x["a"] * x["t"]),
                "u": make_rule(["v", "a", "t"], lambda x: x["v"] - x["a"] * x["t"]),
                "a": make_rule(["v", "u", "t"], lambda x: (x["v"] - x["u"]) / x["t"]),
                "t": make_rule(["v", "u", "a"], lambda x: (x["v"] - x["u"]) / x["a"]),
            },
        ),
        EquationDefinition(
            name="2nd Equation of Motion (s = u*t + 0.5*a*t^2)",
            variables={
                "s": "Displacement (m)",
                "u": "Initial velocity (m/s)",
                "a": "Acceleration (m/s^2)",
                "t": "Time (s)",
            },
            solve_rules={
                "s": make_rule(["u", "a", "t"], lambda x: x["u"] * x["t"] + 0.5 * x["a"] * (x["t"] ** 2)),
                "u": make_rule(["s", "a", "t"], lambda x: (x["s"] - 0.5 * x["a"] * (x["t"] ** 2)) / x["t"]),
                "a": make_rule(["s", "u", "t"], lambda x: 2 * (x["s"] - x["u"] * x["t"]) / (x["t"] ** 2)),
                "t": make_rule(["s", "u", "a"], solve_motion_2_time),
            },
        ),
        EquationDefinition(
            name="3rd Equation of Motion (v^2 = u^2 + 2*a*s)",
            variables={
                "v": "Final velocity (m/s)",
                "u": "Initial velocity (m/s)",
                "a": "Acceleration (m/s^2)",
                "s": "Displacement (m)",
            },
            solve_rules={
                "v": make_rule(["u", "a", "s"], lambda x: sqrt_checked((x["u"] ** 2) + (2 * x["a"] * x["s"]), "v")),
                "u": make_rule(["v", "a", "s"], lambda x: sqrt_checked((x["v"] ** 2) - (2 * x["a"] * x["s"]), "u")),
                "a": make_rule(["v", "u", "s"], lambda x: ((x["v"] ** 2) - (x["u"] ** 2)) / (2 * x["s"])),
                "s": make_rule(["v", "u", "a"], lambda x: ((x["v"] ** 2) - (x["u"] ** 2)) / (2 * x["a"])),
            },
        ),
        EquationDefinition(
            name="4th Equation of Motion (s = ((u + v)/2)*t)",
            variables={
                "s": "Displacement (m)",
                "u": "Initial velocity (m/s)",
                "v": "Final velocity (m/s)",
                "t": "Time (s)",
            },
            solve_rules={
                "s": make_rule(["u", "v", "t"], lambda x: ((x["u"] + x["v"]) / 2) * x["t"]),
                "u": make_rule(["s", "v", "t"], lambda x: (2 * x["s"] / x["t"]) - x["v"]),
                "v": make_rule(["s", "u", "t"], lambda x: (2 * x["s"] / x["t"]) - x["u"]),
                "t": make_rule(["s", "u", "v"], lambda x: (2 * x["s"]) / (x["u"] + x["v"])),
            },
        ),
    ],
    "Forces and Materials": [
        EquationDefinition(
            name="Density (rho = m / V)",
            variables={
                "rho": "Density (kg/m^3)",
                "m": "Mass (kg)",
                "V": "Volume (m^3)",
            },
            solve_rules={
                "rho": make_rule(["m", "V"], lambda x: x["m"] / x["V"]),
                "m": make_rule(["rho", "V"], lambda x: x["rho"] * x["V"]),
                "V": make_rule(["rho", "m"], lambda x: x["m"] / x["rho"]),
            },
        ),
        EquationDefinition(
            name="Hooke's Law (F = k*x)",
            variables={
                "F": "Force (N)",
                "k": "Spring constant (N/m)",
                "x": "Extension (m)",
            },
            solve_rules={
                "F": make_rule(["k", "x"], lambda x: x["k"] * x["x"]),
                "k": make_rule(["F", "x"], lambda x: x["F"] / x["x"]),
                "x": make_rule(["F", "k"], lambda x: x["F"] / x["k"]),
            },
        ),
        EquationDefinition(
            name="Springs in Series (1/k_total = 1/k1 + 1/k2)",
            variables={
                "k_total": "Equivalent spring constant (N/m)",
                "k1": "Spring constant 1 (N/m)",
                "k2": "Spring constant 2 (N/m)",
            },
            solve_rules={
                "k_total": make_rule(["k1", "k2"], lambda x: 1 / ((1 / x["k1"]) + (1 / x["k2"]))),
                "k1": make_rule(["k_total", "k2"], lambda x: 1 / ((1 / x["k_total"]) - (1 / x["k2"]))),
                "k2": make_rule(["k_total", "k1"], lambda x: 1 / ((1 / x["k_total"]) - (1 / x["k1"]))),
            },
        ),
        EquationDefinition(
            name="Springs in Parallel (k_total = k1 + k2)",
            variables={
                "k_total": "Equivalent spring constant (N/m)",
                "k1": "Spring constant 1 (N/m)",
                "k2": "Spring constant 2 (N/m)",
            },
            solve_rules={
                "k_total": make_rule(["k1", "k2"], lambda x: x["k1"] + x["k2"]),
                "k1": make_rule(["k_total", "k2"], lambda x: x["k_total"] - x["k2"]),
                "k2": make_rule(["k_total", "k1"], lambda x: x["k_total"] - x["k1"]),
            },
        ),
        EquationDefinition(
            name="Moment (M = F*d)",
            variables={
                "M": "Moment (N m)",
                "F": "Force (N)",
                "d": "Perpendicular distance from pivot (m)",
            },
            solve_rules={
                "M": make_rule(["F", "d"], lambda x: x["F"] * x["d"]),
                "F": make_rule(["M", "d"], lambda x: x["M"] / x["d"]),
                "d": make_rule(["M", "F"], lambda x: x["M"] / x["F"]),
            },
        ),
        EquationDefinition(
            name="Principle of Moments (clockwise = anticlockwise)",
            variables={
                "clockwise": "Total clockwise moment (N m)",
                "anticlockwise": "Total anticlockwise moment (N m)",
            },
            solve_rules={
                "clockwise": make_rule(["anticlockwise"], lambda x: x["anticlockwise"]),
                "anticlockwise": make_rule(["clockwise"], lambda x: x["clockwise"]),
            },
        ),
    ],
    "Energy and Work": [
        EquationDefinition(
            name="Gravitational Potential Energy (E_p = m*g*h)",
            variables={
                "E_p": "Gravitational potential energy (J)",
                "m": "Mass (kg)",
                "g": "Gravitational field strength (N/kg or m/s^2)",
                "h": "Height (m)",
            },
            solve_rules={
                "E_p": make_rule(["m", "g", "h"], lambda x: x["m"] * x["g"] * x["h"]),
                "m": make_rule(["E_p", "g", "h"], lambda x: x["E_p"] / (x["g"] * x["h"])),
                "g": make_rule(["E_p", "m", "h"], lambda x: x["E_p"] / (x["m"] * x["h"])),
                "h": make_rule(["E_p", "m", "g"], lambda x: x["E_p"] / (x["m"] * x["g"])),
            },
        ),
        EquationDefinition(
            name="Kinetic Energy (E_k = 0.5*m*v^2)",
            variables={
                "E_k": "Kinetic energy (J)",
                "m": "Mass (kg)",
                "v": "Speed (m/s)",
            },
            solve_rules={
                "E_k": make_rule(["m", "v"], lambda x: 0.5 * x["m"] * (x["v"] ** 2)),
                "m": make_rule(["E_k", "v"], lambda x: (2 * x["E_k"]) / (x["v"] ** 2)),
                "v": make_rule(["E_k", "m"], lambda x: sqrt_checked((2 * x["E_k"]) / x["m"], "v")),
            },
        ),
        EquationDefinition(
            name="Work Done (W = F*d)",
            variables={
                "W": "Work done (J)",
                "F": "Force (N)",
                "d": "Distance moved in direction of force (m)",
            },
            solve_rules={
                "W": make_rule(["F", "d"], lambda x: x["F"] * x["d"]),
                "F": make_rule(["W", "d"], lambda x: x["W"] / x["d"]),
                "d": make_rule(["W", "F"], lambda x: x["W"] / x["F"]),
            },
        ),
        EquationDefinition(
            name="Work Against Gravity (W = m*g*h)",
            variables={
                "W": "Work done against gravity (J)",
                "m": "Mass (kg)",
                "g": "Gravitational field strength (N/kg or m/s^2)",
                "h": "Vertical height gained (m)",
            },
            solve_rules={
                "W": make_rule(["m", "g", "h"], lambda x: x["m"] * x["g"] * x["h"]),
                "m": make_rule(["W", "g", "h"], lambda x: x["W"] / (x["g"] * x["h"])),
                "g": make_rule(["W", "m", "h"], lambda x: x["W"] / (x["m"] * x["h"])),
                "h": make_rule(["W", "m", "g"], lambda x: x["W"] / (x["m"] * x["g"])),
            },
        ),
    ],
    "Gas Laws and Pressure": [
        EquationDefinition(
            name="Pressure in a Liquid (P = rho*g*h)",
            variables={
                "P": "Pressure (Pa)",
                "rho": "Liquid density (kg/m^3)",
                "g": "Gravitational field strength (N/kg or m/s^2)",
                "h": "Depth below surface (m)",
            },
            solve_rules={
                "P": make_rule(["rho", "g", "h"], lambda x: x["rho"] * x["g"] * x["h"]),
                "rho": make_rule(["P", "g", "h"], lambda x: x["P"] / (x["g"] * x["h"])),
                "g": make_rule(["P", "rho", "h"], lambda x: x["P"] / (x["rho"] * x["h"])),
                "h": make_rule(["P", "rho", "g"], lambda x: x["P"] / (x["rho"] * x["g"])),
            },
        ),
        EquationDefinition(
            name="Boyle's Law (P1*V1 = P2*V2)",
            variables={
                "P1": "Initial pressure (Pa)",
                "V1": "Initial volume (m^3)",
                "P2": "Final pressure (Pa)",
                "V2": "Final volume (m^3)",
            },
            solve_rules={
                "P1": make_rule(["V1", "P2", "V2"], lambda x: (x["P2"] * x["V2"]) / x["V1"]),
                "V1": make_rule(["P1", "P2", "V2"], lambda x: (x["P2"] * x["V2"]) / x["P1"]),
                "P2": make_rule(["P1", "V1", "V2"], lambda x: (x["P1"] * x["V1"]) / x["V2"]),
                "V2": make_rule(["P1", "V1", "P2"], lambda x: (x["P1"] * x["V1"]) / x["P2"]),
            },
        ),
        EquationDefinition(
            name="Charles' Law (V1/T1 = V2/T2)",
            variables={
                "V1": "Initial volume (m^3)",
                "T1": "Initial absolute temperature (K)",
                "V2": "Final volume (m^3)",
                "T2": "Final absolute temperature (K)",
            },
            solve_rules={
                "V1": make_rule(["T1", "V2", "T2"], lambda x: (x["V2"] * x["T1"]) / x["T2"]),
                "T1": make_rule(["V1", "V2", "T2"], lambda x: (x["V1"] * x["T2"]) / x["V2"]),
                "V2": make_rule(["V1", "T1", "T2"], lambda x: (x["V1"] * x["T2"]) / x["T1"]),
                "T2": make_rule(["V1", "T1", "V2"], lambda x: (x["V2"] * x["T1"]) / x["V1"]),
            },
        ),
        EquationDefinition(
            name="Pressure Law (P1/T1 = P2/T2)",
            variables={
                "P1": "Initial pressure (Pa)",
                "T1": "Initial absolute temperature (K)",
                "P2": "Final pressure (Pa)",
                "T2": "Final absolute temperature (K)",
            },
            solve_rules={
                "P1": make_rule(["T1", "P2", "T2"], lambda x: (x["P2"] * x["T1"]) / x["T2"]),
                "T1": make_rule(["P1", "P2", "T2"], lambda x: (x["P1"] * x["T2"]) / x["P2"]),
                "P2": make_rule(["P1", "T1", "T2"], lambda x: (x["P1"] * x["T2"]) / x["T1"]),
                "T2": make_rule(["P1", "T1", "P2"], lambda x: (x["P2"] * x["T1"]) / x["P1"]),
            },
        ),
    ],
    "Refarction": [
        EquationDefinition(
            name="Snell's Law (n1*sin(theta1) = n2*sin(theta2))",
            variables={
                "n1": "Refractive index of medium 1",
                "theta1": "Angle of incidence (degrees)",
                "n2": "Refractive index of medium 2",
                "theta2": "Angle of refraction (degrees)",
            },
            solve_rules={
                "n1": make_rule(["theta1", "n2", "theta2"], lambda x: (x["n2"] * sin_deg(x["theta2"])) / sin_deg(x["theta1"])),
                "theta1": make_rule(["n1", "n2", "theta2"], lambda x: asin_deg((x["n2"] * sin_deg(x["theta2"])) / x["n1"])),
                "n2": make_rule(["n1", "theta1", "theta2"], lambda x: (x["n1"] * sin_deg(x["theta1"])) / sin_deg(x["theta2"])),
                "theta2": make_rule(["n1", "theta1", "n2"], lambda x: asin_deg((x["n1"] * sin_deg(x["theta1"])) / x["n2"])),
            },
        ),
    ],
    "Thermal Physics": [
        EquationDefinition(
            name="Heat Capacity (C = Q/delta_T)",
            variables={
                "C": "Heat capacity (J/K)",
                "Q": "Thermal energy transferred (J)",
                "delta_T": "Temperature change (K or deg C)",
            },
            solve_rules={
                "C": make_rule(["Q", "delta_T"], lambda x: x["Q"] / x["delta_T"]),
                "Q": make_rule(["C", "delta_T"], lambda x: x["C"] * x["delta_T"]),
                "delta_T": make_rule(["Q", "C"], lambda x: x["Q"] / x["C"]),
            },
        ),
        EquationDefinition(
            name="Specific Heat Capacity (c = Q/(m*delta_T))",
            variables={
                "c": "Specific heat capacity (J/kg/K)",
                "Q": "Thermal energy transferred (J)",
                "m": "Mass (kg)",
                "delta_T": "Temperature change (K or deg C)",
            },
            solve_rules={
                "c": make_rule(["Q", "m", "delta_T"], lambda x: x["Q"] / (x["m"] * x["delta_T"])),
                "Q": make_rule(["c", "m", "delta_T"], lambda x: x["c"] * x["m"] * x["delta_T"]),
                "m": make_rule(["c", "Q", "delta_T"], lambda x: x["Q"] / (x["c"] * x["delta_T"])),
                "delta_T": make_rule(["c", "Q", "m"], lambda x: x["Q"] / (x["c"] * x["m"])),
            },
        ),
        EquationDefinition(
            name="Latent Heat of Fusion (Q = m*L_f)",
            variables={
                "Q": "Energy for melting/freezing (J)",
                "m": "Mass (kg)",
                "L_f": "Specific latent heat of fusion (J/kg)",
            },
            solve_rules={
                "Q": make_rule(["m", "L_f"], lambda x: x["m"] * x["L_f"]),
                "m": make_rule(["Q", "L_f"], lambda x: x["Q"] / x["L_f"]),
                "L_f": make_rule(["Q", "m"], lambda x: x["Q"] / x["m"]),
            },
        ),
        EquationDefinition(
            name="Latent Heat of Vaporization (Q = m*L_v)",
            variables={
                "Q": "Energy for boiling/condensing (J)",
                "m": "Mass (kg)",
                "L_v": "Specific latent heat of vaporization (J/kg)",
            },
            solve_rules={
                "Q": make_rule(["m", "L_v"], lambda x: x["m"] * x["L_v"]),
                "m": make_rule(["Q", "L_v"], lambda x: x["Q"] / x["L_v"]),
                "L_v": make_rule(["Q", "m"], lambda x: x["Q"] / x["m"]),
            },
        ),
    ],
    "Electricity": [
        EquationDefinition(
            name="Current (I = Q/t)",
            variables={
                "I": "Current (A)",
                "Q": "Charge (C)",
                "t": "Time (s)",
            },
            solve_rules={
                "I": make_rule(["Q", "t"], lambda x: x["Q"] / x["t"]),
                "Q": make_rule(["I", "t"], lambda x: x["I"] * x["t"]),
                "t": make_rule(["I", "Q"], lambda x: x["Q"] / x["I"]),
            },
        ),
        EquationDefinition(
            name="Voltage (V = E/Q)",
            variables={
                "V": "Potential difference / voltage (V)",
                "E": "Energy transferred (J)",
                "Q": "Charge (C)",
            },
            solve_rules={
                "V": make_rule(["E", "Q"], lambda x: x["E"] / x["Q"]),
                "E": make_rule(["V", "Q"], lambda x: x["V"] * x["Q"]),
                "Q": make_rule(["V", "E"], lambda x: x["E"] / x["V"]),
            },
        ),
        EquationDefinition(
            name="Ohm's Law (V = I*R)",
            variables={
                "V": "Voltage (V)",
                "I": "Current (A)",
                "R": "Resistance (ohms)",
            },
            solve_rules={
                "V": make_rule(["I", "R"], lambda x: x["I"] * x["R"]),
                "I": make_rule(["V", "R"], lambda x: x["V"] / x["R"]),
                "R": make_rule(["V", "I"], lambda x: x["V"] / x["I"]),
            },
        ),
        EquationDefinition(
            name="Resistivity of a Wire (R = rho*L/A)",
            variables={
                "R": "Resistance (ohms)",
                "rho": "Resistivity (ohm m)",
                "L": "Length of wire (m)",
                "A": "Cross-sectional area (m^2)",
            },
            solve_rules={
                "R": make_rule(["rho", "L", "A"], lambda x: (x["rho"] * x["L"]) / x["A"]),
                "rho": make_rule(["R", "L", "A"], lambda x: (x["R"] * x["A"]) / x["L"]),
                "L": make_rule(["R", "rho", "A"], lambda x: (x["R"] * x["A"]) / x["rho"]),
                "A": make_rule(["R", "rho", "L"], lambda x: (x["rho"] * x["L"]) / x["R"]),
            },
        ),
    ],
    "Transformers": [
        EquationDefinition(
            name="Transformer Ratio (Vp/Vs = Np/Ns)",
            variables={
                "Vp": "Primary voltage (V)",
                "Vs": "Secondary voltage (V)",
                "Np": "Primary turns",
                "Ns": "Secondary turns",
            },
            solve_rules={
                "Vp": make_rule(["Vs", "Np", "Ns"], lambda x: (x["Vs"] * x["Np"]) / x["Ns"]),
                "Vs": make_rule(["Vp", "Np", "Ns"], lambda x: (x["Vp"] * x["Ns"]) / x["Np"]),
                "Np": make_rule(["Vp", "Vs", "Ns"], lambda x: (x["Vp"] * x["Ns"]) / x["Vs"]),
                "Ns": make_rule(["Vp", "Vs", "Np"], lambda x: (x["Vs"] * x["Np"]) / x["Vp"]),
            },
        ),
        EquationDefinition(
            name="Transformer Power Transfer (Vp*Ip = Vs*Is)",
            variables={
                "Vp": "Primary voltage (V)",
                "Ip": "Primary current (A)",
                "Vs": "Secondary voltage (V)",
                "Is": "Secondary current (A)",
            },
            solve_rules={
                "Vp": make_rule(["Ip", "Vs", "Is"], lambda x: (x["Vs"] * x["Is"]) / x["Ip"]),
                "Ip": make_rule(["Vp", "Vs", "Is"], lambda x: (x["Vs"] * x["Is"]) / x["Vp"]),
                "Vs": make_rule(["Vp", "Ip", "Is"], lambda x: (x["Vp"] * x["Ip"]) / x["Is"]),
                "Is": make_rule(["Vp", "Ip", "Vs"], lambda x: (x["Vp"] * x["Ip"]) / x["Vs"]),
            },
        ),
    ],
}


def choose_single_option(prompt, options):
    while True:
        print()
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")

        raw_choice = input(f"{prompt} (number): ").strip().lower()
        if raw_choice in {"q", "quit", "exit"}:
            raise SystemExit("Exiting physics solver.")

        try:
            selected_index = int(raw_choice) - 1
            if 0 <= selected_index < len(options):
                return selected_index
        except ValueError:
            pass

        print("Invalid selection. Please enter a listed number.")


def ask_yes_no(prompt):
    while True:
        raw_choice = input(f"{prompt} (y/n): ").strip().lower()
        if raw_choice in {"y", "yes"}:
            return True
        if raw_choice in {"n", "no"}:
            return False
        print("Please answer with y or n.")


def show_equation_summary(equation):
    print()
    print(f"Equation: {equation.name}")
    print("Variables:")
    for key, description in equation.variables.items():
        print(f"  {key}: {description}")


def read_known_values(equation):
    known_values = {}
    print()
    print("Enter known values.")
    print("Leave one variable blank so the solver can find it.")

    for variable, description in equation.variables.items():
        while True:
            raw_value = input(f"{variable} ({description}): ").strip()
            if raw_value == "":
                break
            try:
                known_values[variable] = float(raw_value)
                break
            except ValueError:
                print("Invalid number. Enter a numeric value or leave blank.")

    return known_values

# checks if the user has inputted a correct value
def solve_missing_variable(equation, known_values):
    missing_variables = [variable for variable in equation.variables if variable not in known_values]

    if len(missing_variables) != 1:
        raise ValueError(
            "You must leave exactly one variable blank. "
            f"Current missing count: {len(missing_variables)}"
        )

    target = missing_variables[0]
    solve_rule = equation.solve_rules.get(target)
    if solve_rule is None:
        raise ValueError(f"No solve rule available for {target} in this equation.")

    required_variables = solve_rule["requires"]
    missing_required = [var for var in required_variables if var not in known_values]
    if missing_required:
        missing_list = ", ".join(missing_required)
        raise ValueError(f"Missing required known values: {missing_list}")

    result = solve_rule["formula"](known_values)
    return target, result

# this simply runs da code
def run_solver():
    print("=" * 64)
    print("Welcome to My very own physics equation solver, desgined to make your life easier")
    print("Pick a topic, pick an equation, fill known values, and solve.")
    print("Type q / quit / exit at menu prompts to close the app.")
    print("=" * 64)

    while True:
        topic_names = list(TOPIC_LIBRARY.keys())
        topic_index = choose_single_option("Choose a topic", topic_names)
        topic_name = topic_names[topic_index]

        equations = TOPIC_LIBRARY[topic_name]
        equation_names = [equation.name for equation in equations]
        equation_index = choose_single_option("Choose an equation", equation_names)
        equation = equations[equation_index]

        show_equation_summary(equation)
        known_values = read_known_values(equation)

        try:
            solved_variable, solved_value = solve_missing_variable(equation, known_values)
            print()
            print("Solved successfully:")
            print(f"  {solved_variable} = {solved_value}")
        except ZeroDivisionError:
            print()
            print("Could not solve: division by zero occurred.")
        except ValueError as error:
            print()
            print(f"Could not solve: {error}")

        if not ask_yes_no("Do another calculation"):
            print("Bye and thank you very much for using this.")
            break


if __name__ == "__main__":
    run_solver()
