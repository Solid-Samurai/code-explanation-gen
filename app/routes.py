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
    try:
        response_data = response.json()
        if isinstance(response_data, list) and len(response_data) > 0:
            explanation = response_data[0].get("generated_text", "No explanation found")
    	elif isinstance(response_data, dict) and "error" in response_data:
            explanation = f"Model Error: {response_data['error']}"
    	else:
            explanation = "Unexpected response format from Hugging Face"
    except Exception as e:
    	print("Error parsing HF response:", str(e))
    	return jsonify({"error": "Failed to parse Hugging Face response"}), 500

@main.route("/", methods=["GET"])
def home():
    return "Backend is running!"
