import requests
from flask import Blueprint, request, jsonify

main = Blueprint("main", __name__)

HF_API_URL = "https://api-inference.huggingface.co/models/t5-small"
HF_API_KEY = "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" 

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

@main.route("/analyze", methods=["POST"])
def analyze_code():
    data = request.get_json()
    code = data.get("code", "")
    if not code:
        return jsonify({"error": "No code provided"}), 400

    prompt = f"Explain this Python code in simple terms:\n{code}"

    try:
        response = requests.post(HF_API_URL, headers=HEADERS, json={"inputs": prompt})
        result = response.json()

        if isinstance(result, dict) and "error" in result:
            return jsonify({"error": result["error"]}), 500

        generated = result[0]["generated_text"]

        suggestions = [
            "Use meaningful variable names",
            "Add comments for clarity",
            "Follow PEP8 coding standards"
        ]

        return jsonify({
            "explanation": generated.strip(),
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
