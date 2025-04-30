from flask import Flask, render_template, request, jsonify
import os
import subprocess
import requests
from pyngrok import ngrok

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLASSES_FILE = os.path.join(BASE_DIR, "classes.txt")
SCRAPER_PATH = os.path.join(BASE_DIR, "courseScraper.py")
FORMATTER_PATH = os.path.join(BASE_DIR, "courseFormatter.py")

# run course scraper
subprocess.run(["python", SCRAPER_PATH], capture_output=True, text=True)
subprocess.run(["python", FORMATTER_PATH], capture_output=True, text=True)

app = Flask(__name__)

class Course:
    def __init__(self, class_name, department, days, time, credit_hours, seats, title):
        self.class_name = class_name
        self.department = department
        self.days = days
        self.time = time
        self.credit_hours = credit_hours
        self.seats = seats
        self.title = title

    def __repr__(self):
        return f"{self.class_name} - {self.title} ({self.days} {self.time}, {self.credit_hours} credit hours)"

@app.route("/selected_classes", methods=["GET", "POST"])
def selected_classes():
    selected_classes = []
    try:
        with open(CLASSES_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(", ")
                    if len(parts) == 7:
                        class_name = parts[0].strip()
                        department = parts[1].strip()
                        days = parts[2].strip()
                        time = parts[3].strip()
                        credit_hours = parts[4].strip()
                        seats = parts[5].strip()
                        title = parts[6].strip()
                        selected_classes.append(Course(class_name, department, days, time, credit_hours, seats, title))
    except FileNotFoundError:
        selected_classes = [{"Error": "classes.txt file not found."}]
    except Exception as e:
        selected_classes = [{"Error": f"An unexpected error occurred: {str(e)}"}]

    return render_template("selected_classes.html", selected_classes=selected_classes)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/computer_science")
def computer_science():
    return render_template("computer_science.html")

@app.route("/mechanical_engineering")
def mechanical_engineering():
    return render_template("mechanical_engineering.html")

@app.route("/civil_engineering")
def civil_engineering():
    return render_template("civil_engineering.html")

@app.route("/electrical_engineering")
def electrical_engineering():
    return render_template("electrical_engineering.html")

@app.route("/biology")
def biology():
    return render_template("biology.html")

@app.route("/basic_sciences")
def basic_sciences():
    return render_template("basic_sciences.html")

# forward chatbot requests
CHATBOT_URL = "http://localhost:5001"

@app.route("/chatbot_api", methods=["POST"])
def chatbot_api():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Forward the request to chatbot.py
        response = requests.post(f"{CHATBOT_URL}/chat", json={"message": user_message})
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to reach chatbot server: {str(e)}"}), 500

if __name__ == "__main__":
    # prevents duplicate ngrok tunnel when flask is reloaded
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        public_url = ngrok.connect(5000)
        print(" * ngrok tunnel running at:", public_url)

    app.run(host="0.0.0.0", port=5000, debug=True)

