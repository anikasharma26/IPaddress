import os
import urllib.request
import json
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/track", methods=["GET"])
def track_ip():
    ip = request.args.get('ip')
    if ip:
        url = f"http://ip-api.com/json/{ip}"
        
        try:
            response = urllib.request.urlopen(url)
            data = response.read()
            values = json.loads(data)

            if values['status'] == 'fail':
                return jsonify({"error": values['message']})
            else:
                return jsonify({
                    "IP": values['query'],
                    "location": f"{values['city']}, {values['regionName']}",
                    "country": values['country'],
                    "ISP": values['isp'],
                    "TimeZone": values['timezone'],
                    "Latitude": values['lat'],
                    "Longitude": values['lon'],

                })
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"})
    return jsonify({"error": "IP not provided"})

if __name__ == "__main__":
    app.run(debug=True)