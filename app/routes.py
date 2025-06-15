import os
import requests
from flask import Blueprint, request, jsonify

main = Blueprint("main", __name__)

HF_API_KEY = os.getenv("HF_API_KEY")
HF_API_URL = "https://api-inference.huggingface.co/models/Salesforce/codegen-350M-mono"

@main.route("/analyze", methods=["POST"])
def analyze_code():
    data = request.get_json()
    print("Incoming request data:", data)  # Debug log

    code = data.get("code", "").strip()
    if not code:
        return jsonify({"error": "Empty input"}), 400

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": code}

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        print("Hugging Face raw response:", response.text)
        response.raise_for_status()
    except Exception as e:
        print("Error calling Hugging Face API:", str(e))
        return jsonify({"error": "Hugging Face API call failed"}), 500

    try:
        response_data = response.json()
        if isinstance(response_data, list) and len(response_data) > 0:
            explanation = response_data[0].get("generated_text", "No explanation found")
        elif isinstance(response_data, dict) and "error" in response_data:
            explanation = f"Model Error: {response_data['error']}"
        else:
            explanation = f"Unexpected response format: {response_data}"
    except Exception as e:
        explanation= f"Failed to parse response. Raw:{response.text}"
        return jsonify({"error": explanation}), 500

    suggestions = []
    if "heap" in code.lower():
        suggestions.append("Consider using Python's built-in `heapq` module.")

    return jsonify({
        "explanation": explanation,
        "suggestions": suggestions
    })

@main.route("/", methods=["GET"])
def home():
    return "Backend is running!"
