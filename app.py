from flask import Flask, render_template, request

from exportToCalendar import exportToIcal


app = Flask(__name__)

def validCourses(courses):
    if courses == "ballsack":
        return True
    return False

@app.route("/", methods=["GET", "POST"])
def index():
    courses = request.form.get("courses", "")
    result = ""
    if request.method == "POST":
        if validCourses(courses):
            result = "successful"
        else:
            result = "try again"
    return render_template("index.html", result=result)


