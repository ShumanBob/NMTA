from  flask import Flask, render_template, request

app = Flask(__name__)

class Course:
    def __init__(self, class_name, department, days, time, credit_hours, title):
        self.class_name = class_name
        self.department = department
        self.days = days
        self.time = time
        self.credit_hours = credit_hours
        self.title = title

    def __repr__(self):
        return f"{self.class_name} - {self.title} ({self.days} {self.time}, {self.credit_hours} credit hours)"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/computer_science", methods=["GET", "POST"])
def computer_science():
    selected_classes = []
    if request.method == "POST":
        try:
            with open("classes.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(", ")
                        if len(parts) == 6:
                            class_name = parts[0].strip()
                            department = parts[1].strip()
                            days = parts[2].strip()
                            time = parts[3].strip()
                            credit_hours = parts[4].strip()
                            title = parts[5].strip()
                            selected_classes.append(Course(class_name, department, days, time, credit_hours, title))
                        else:
                            error_message = f"Invalid format: {line}. Expected 6 fields separated by commas."
                            selected_classes.append({"Error": error_message})
        except FileNotFoundError:
            selected_classes = [{"Error": "classes.txt file not found."}]
        except Exception as e:
            selected_classes = [{"Error": f"An unexpected error occurred: {str(e)}"}]
        return render_template("selected_classes.html", selected_classes=selected_classes)
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

if __name__ == "__main__":
    app.run(debug=True)