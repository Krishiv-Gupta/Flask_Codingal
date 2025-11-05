from flask import Flask, render_template, request
import json
import urllib.request

app = Flask(__name__)


@app.route("/", methods=['POST', "GET"])
def details():
    if request.method == 'POST':
        location = request.form.get("location")
        API_KEY = "r7F0vLzcpkE6h8ZCDKoR9_-BLSjKGxUfIKDkp4dV2GY"

        try:
            source = urllib.request.urlopen('https://geocode.search.hereapi.com/v1/geocode?apikey='+API_KEY+'&q='+location).read()
            responseData = json.loads(source)
            data = {
                "latitude":str(responseData['items'][0]['position']['lat']),
                "longitude":str(responseData['items'][0]['position']['lng']),
            }
            return render_template("index.html", data=data, apikey = API_KEY)
        except:
            return render_template("index.html", error="Give the correct location")
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

