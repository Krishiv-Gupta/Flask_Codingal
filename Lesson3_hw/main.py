from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    bmi = None
    category = None

    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"]) / 100  # convert cm to meters
            bmi = weight / (height * height)

            if bmi < 18.5:
                category = "Underweight"
            elif bmi < 24.9:
                category = "Normal weight"
            elif bmi < 29.9:
                category = "Overweight"
            else:
                category = "Obese"
        except:
            bmi = "Invalid input"
            category = ""

    return render_template("index.html", bmi=bmi, category=category)

if __name__ == "__main__":
    app.run(debug=True)
