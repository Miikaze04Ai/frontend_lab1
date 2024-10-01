from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/send_data", methods=["POST"])
def send_data():
    data = request.form["data"]
    # Send data to server using HTTP request
    response = requests.post("http://localhost:5001/receive_data", data={"data": data})
    if response.status_code == 200:
        return "Data sent successfully", 200
    else:
        return "Failed to send data to server", 500

@app.route("/get_data", methods=["POST"])
def get_data():
    # Send request to backend to get data
    response = requests.post("http://localhost:5001/get_data")
    if response.status_code == 200:
        return response.text, 200
    else:
        return "Failed to get data from server", 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)