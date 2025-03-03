from flask import Flask, render_template, request
import coursereader

app = Flask(__name__)
course_list = coursereader.main()
#print(course_list[0].course_code)

@app.route("/")
def home():
    return render_template("index.html", course_list=course_list)

@app.route("/computer_science", methods=["GET", "POST"])
def computer_science():
    if request.method == "POST":
        selected_classes = request.form.getlist("checkbox[]")
        return render_template("selected_classes.html", course_list=course_list)
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
