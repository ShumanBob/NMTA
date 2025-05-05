from flask import Flask, render_template, request, jsonify
import os
import subprocess
import requests
from pyngrok import ngrok

# set up file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLASSES_FILE = os.path.join(BASE_DIR, "data/classes.txt")
SCRAPER_PATH = os.path.join(BASE_DIR, "courseScraper.py")
FORMATTER_PATH = os.path.join(BASE_DIR, "courseFormatter.py")

# run the course scraper and formatter
subprocess.run(["python", SCRAPER_PATH], capture_output=True, text=True)
subprocess.run(["python", FORMATTER_PATH], capture_output=True, text=True)

# flask app
app = Flask(__name__)
# course field definitions
class Course:
    def __init__(self, class_name, crn, department, days, time, credit_hours, seats, title,
                 instructor, location, course_type, term, subject, campus,
                 date_range, limit, enrolled, waitlist, fees, bookstore_link):
        self.class_name = class_name
        self.crn = crn
        self.department = department
        self.days = days
        self.time = time
        self.credit_hours = credit_hours
        self.seats = seats
        self.title = title
        self.instructor = instructor
        self.location = location
        self.course_type = course_type
        self.term = term
        self.subject = subject
        self.campus = campus
        self.date_range = date_range
        self.limit = limit
        self.enrolled = enrolled
        self.waitlist = waitlist
        self.fees = fees
        self.bookstore_link = bookstore_link

    def __repr__(self):
        return f"{self.class_name} - {self.title} ({self.days} {self.time})"
# route to schedule builder page
@app.route("/schedule_builder", methods=["GET", "POST"])
def schedule_builder():
    selected_classes = []
    try:
        # read the parsed data from the file
        with open(CLASSES_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    # split data
                    main_part, _, meta_part = line.partition(" | ")
                    parts = [p.strip() for p in main_part.split(",")]
                    if len(parts) < 7:
                        continue

                    # extract key value pairs; N/A if empty
                    meta_parts = {}
                    for kv in meta_part.split(", "):
                        if ": " in kv:
                            key, value = kv.split(": ", 1)
                            val = value.strip() or "N/A"
                            meta_parts[key.strip()] = val
                    # assign main fields
                    class_name = parts[0]
                    crn = parts[1]
                    days = parts[2]
                    time = parts[3]
                    credit_hours = parts[4]
                    seats = parts[5]
                    title = parts[6]
                    department = meta_parts.get("Subject", "N/A")
                    # create course object and add to list
                    course = Course(
                        class_name=class_name,
                        crn=crn,
                        department=department,
                        days=days,
                        time=time,
                        credit_hours=credit_hours,
                        seats=seats,
                        title=title,
                        instructor=meta_parts.get("Instructor", "N/A"),
                        location=meta_parts.get("Location", "N/A"),
                        course_type=meta_parts.get("Type", "N/A"),
                        term=meta_parts.get("Term", "N/A"),
                        subject=meta_parts.get("Subject", "N/A"),
                        campus=meta_parts.get("Campus", "N/A"),
                        date_range=meta_parts.get("Date Range", "N/A"),
                        limit=meta_parts.get("Limit", "N/A"),
                        enrolled=meta_parts.get("Enrolled", "N/A"),
                        waitlist=meta_parts.get("Waitlist", "N/A"),
                        fees=meta_parts.get("Fees", "N/A"),
                        bookstore_link=meta_parts.get("Bookstore", "N/A")
                    )

                    selected_classes.append(course)
                except Exception as parse_error:
                    print(f"Error parsing line: {line}\n{parse_error}")
    # error execeptions and render template
    except FileNotFoundError:
        selected_classes = [{"Error": "classes.txt file not found."}]
    except Exception as e:
        selected_classes = [{"Error": f"An unexpected error occurred: {str(e)}"}]

    return render_template("schedule_builder.html", selected_classes=selected_classes)
# routing for front page
@app.route("/")
def home():
    return render_template("index.html")
# routing for flowchart pages
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

@app.route('/acceleratedphysics')
def acceleratedphysics():
    return render_template('acceleratedphysics.html')

@app.route('/astrophysics')
def astrophysics():
    return render_template('astrophysics.html')

@app.route('/atmosphereicphysics')
def atmosphereicphysics():
    return render_template('atmosphereicphysics.html')

@app.route('/chemEngineering')
def chemEngineering():
    return render_template('chemEngineering.html')

@app.route('/chemistry')
def chemistry():
    return render_template('chemistry.html')

@app.route('/mathematics')
def mathematics():
    return render_template('mathematics.html')

@app.route('/petroleum')
def petroleum():
    return render_template('petroleum.html')

@app.route('/physics')
def physics():
    return render_template('physics.html')

@app.route('/noflowchart')
def noflowchart():
    return render_template('noflowchart.html')

# chatbot route
@app.route("/chat", methods=["POST"])
def chatbot():
    try:
        CHATBOT_URL = os.environ.get("CHATBOT_URL", "http://localhost:5001")
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        # forward to chatbot server
        response = requests.post(f"{CHATBOT_URL}/chat", json={"message": user_message})
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to reach chatbot server: {str(e)}"}), 500
# run flask app with ngrok tunnel
if __name__ == "__main__":
    # make sure ngrok onlt runs once
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        public_url = ngrok.connect(5000)
        print(" * ngrok tunnel running at:", public_url)
    app.run(port=5000, debug=False)
