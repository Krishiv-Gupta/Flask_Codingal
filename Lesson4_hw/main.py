from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    vowel_count = None
    text = ""
    a=0
    if request.method == "POST":
        text = request.form["text"].lower()
        vowels = ['a','e','i','o','u']
        for i in text:
            if i in vowels:
                a+=1

    return render_template("index.html", text=text, count=a)

if __name__ == "__main__":
    app.run(debug=True)
