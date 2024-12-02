from flask import Flask, render_template, request, render_template_string
import requests
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    html = '''
<!DOCTYPE html>
<html>
  <head>
    <title>Enter data to be sent to the server</title>
  </head>
  <body>
    <h1>Enter data to be sent to the server</h1>
    <form action="/send_data" method="post">
      <input type="text" name="data" placeholder="Enter some data">
      <button type="submit">Send to Server</button>
    </form>
    <h1>Get data from server</h1>
    <form action="/get_data" method="post">
      <button type="submit">Get Data</button>
      <input type="text" id="result" readonly>
    </form>
    <script>
      document.addEventListener("DOMContentLoaded", function() {
        const form = document.querySelector("form[action='/get_data']");
        form.addEventListener("submit", function(event) {
          event.preventDefault();
          fetch("/get_data", {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded"
            }
          })
          .then(response => response.text())
          .then(data => {
            document.querySelector("#result").value = data;
          })
          .catch(error => console.error(error));
        });
      });
    </script>
  </body>
</html>
    '''
    return render_template_string(html, response_data='')

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