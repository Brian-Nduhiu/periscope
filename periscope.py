import re
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def employeeHome():
    return render_template("employee.html")


if __name__ == "__main__":
    app.run()