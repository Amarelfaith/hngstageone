from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins


def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number."""
    return n == sum(i for i in range(1, n) if n % i == 0)


def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n


def get_fun_fact(n: int) -> str:
    """Retrieve a fun fact about a number from NumbersAPI."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}")
        return response.text if response.status_code == 200 else "No fact available."
    except requests.RequestException:
        return "No fact available."


@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    number = request.args.get("number")

    # Validate input
    if number is None:
        return jsonify({"error": "Number parameter is required"}), 400
    if not number.isdigit():
        return jsonify({"error": "Input must be a number"}), 400
    try:
        number = int(number)
    except ValueError:
        return jsonify({"error": "Number must be a positive integer"}), 400

    if number <= 0:
        return jsonify({"error": "Number must be greater than zero"}), 400

    # Determine properties
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")

    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    return jsonify({
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(number)),
        "fun_fact": get_fun_fact(number)
    })


if __name__ == "__main__":
    app.run(debug=True)
