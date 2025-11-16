from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from weather_api import get_weather

app = Flask(__name__, static_folder="../frontend")
CORS(app)

# Serve index.html at the root


@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

# Serve other static files (CSS, JS)


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

# Forecast API


@app.route("/forecast", methods=["GET"])
def forecast():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    forecast = get_weather(city)
    return jsonify(forecast)


if __name__ == "__main__":
    app.run(debug=True)
