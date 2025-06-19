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
