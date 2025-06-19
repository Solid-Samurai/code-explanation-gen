
from flask import Blueprint, request, jsonify
from transformers import pipeline

main = Blueprint("main", __name__)

# Load the model only once
pipe = pipeline("text2text-generation", model="t5-small")

@main.route("/analyze", methods=["POST"])
def analyze_code():
    try:
        data = request.get_json()
        code = data.get("code", "")
        if not code:
            return jsonify({"error": "No code provided"}), 400

        prompt = f"Explain this Python code in simple terms:\n{code}"
        response = pipe(prompt, max_length=150, do_sample=False)[0]["generated_text"]

        suggestions = [
            "Use meaningful variable names",
            "Add comments for clarity",
            "Follow PEP8 coding standards"
        ]

        return jsonify({
            "explanation": response.strip(),
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
=======
import os
import requests
from flask import Blueprint, request, jsonify

main = Blueprint("main", __name__)

# ✅ Verified model that supports Hugging Face Inference API
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HF_API_KEY = os.getenv("HF_API_KEY")

@main.route("/analyze", methods=["POST"])
def analyze_code():
    data = request.get_json()
    print("Incoming request data:", data)

    code = data.get("code", "").strip()
    if not code:
        return jsonify({"error": "Empty input"}), 400

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    # ✅ Prompt format for instruction-tuned model
    payload = {
        "inputs": f"Explain what this Python code does:\n{code}",
        "parameters": {
            "max_new_tokens": 100
        }
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        print("Hugging Face raw response:", response.text)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("HTTPError:", e)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        return jsonify({
            "error": f"HTTPError {response.status_code}: {response.text}"
        }), 500
    except Exception as e:
        print("Other error calling Hugging Face API:", str(e))
        return jsonify({
            "error": "Hugging Face API call failed"
        }), 500

    try:
        response_data = response.json()
        if isinstance(response_data, list) and len(response_data) > 0:
            explanation = response_data[0].get("generated_text", "No explanation found")
        elif isinstance(response_data, dict) and "error" in response_data:
            explanation = f"Model Error: {response_data['error']}"
        else:
            explanation = f"Unexpected response format: {response_data}"
    except Exception as e:
        print("Error parsing HF response:", str(e))
        explanation = f"Failed to parse response. Raw: {response.text}"
        return jsonify({"error": explanation}), 500

    # ✅ Rule-based suggestions
    suggestions = []
    if "heap" in code.lower():
        suggestions.append("Consider using Python's built-in `heapq` module.")
    if "for" in code.lower() and "range" in code.lower():
        suggestions.append("Consider using list comprehensions for cleaner loops if applicable.")

    return jsonify({
        "explanation": explanation,
        "suggestions": suggestions
    })

@main.route("/", methods=["GET"])
def home():
    return "Backend is running!"
