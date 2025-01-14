from flask import Flask, render_template
from selenium_script import scrape_twitter_trends

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run_script", methods=["GET"])
def run_script():
    data = scrape_twitter_trends()
    return render_template(
        "index.html",
        trends=data["trends"],
        ip=data["ip_address"],
        timestamp=data["timestamp"],
    )

if __name__ == "__main__":
    app.run(debug=True)
