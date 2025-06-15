import os
import requests
from flask import Blueprint, request, jsonify

main = Blueprint("main", __name__)

HF_API_KEY = os.getenv("HF_API_KEY")  # Do NOT hardcode the key
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/codebert-base"

@main.route("/analyze", methods=["POST"])
def analyze_code():
    data = request.get_json()
    code = data.get("code", "").strip()
    if not code:
        return jsonify({"error": "Empty input"}), 400

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(HF_API_URL, headers=headers, json={"inputs": code})

    explanation = response.json()[0].get("generated_text", "No explanation found")
    suggestions = []
    if "heap" in code.lower():
        suggestions.append("Consider using Python's built-in `heapq` module.")

    return jsonify({"explanation": explanation, "suggestions": suggestions})

@main.route("/", methods=["GET"])
def home():
    return "Backend is running!"
