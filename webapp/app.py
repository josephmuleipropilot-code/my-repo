from flask import Flask, render_template, request
from solver import TOPIC_LIBRARY, solve_equation

app = Flask(__name__)


def serializable_topics():
    out = {}
    for topic, equations in TOPIC_LIBRARY.items():
        out[topic] = []
        for eq in equations:
            out[topic].append({"name": eq.name, "variables": eq.variables})
    return out


@app.route("/", methods=["GET"]) 
def index():
    topics = serializable_topics()
    return render_template("index.html", topics=topics)


@app.route("/solve", methods=["POST"]) 
def solve():
    topic = request.form.get("topic")
    equation_index = int(request.form.get("equation_index"))

    # collect known values (non-empty inputs)
    known_values = {}
    for key, value in request.form.items():
        if key.startswith("var_"):
            varname = key[4:]
            if value.strip() != "":
                try:
                    known_values[varname] = float(value)
                except ValueError:
                    return render_template("result.html", error=f"Invalid numeric input for {varname}.")

    try:
        solved_var, solved_value = solve_equation(topic, equation_index, known_values)
        return render_template("result.html", solved_var=solved_var, solved_value=solved_value)
    except Exception as e:
        return render_template("result.html", error=str(e))


if __name__ == "__main__":
    app.run(debug=True)
