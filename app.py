from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from weather_api import get_weather
from whitenoise import WhiteNoise

app = Flask(__name__, static_folder="../frontend")
CORS(app)

# Use WhiteNoise to serve static files in production
app.wsgi_app = WhiteNoise(
    app.wsgi_app, root=app.static_folder, index_file=True)

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
