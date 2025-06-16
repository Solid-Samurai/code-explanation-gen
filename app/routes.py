from flask import Blueprint, request, jsonify
import requests
import os

print("Loading routes.py...")

main = Blueprint('main', __name__)

# Hugging Face API setup
API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/Salesforce/codet5-base"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
print(f"API_TOKEN: {API_TOKEN if API_TOKEN else 'Not found'}")

def query_hugging_face(payload):
    """Send request to Hugging Face Inference API."""
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@main.route('/explain', methods=['POST'])
def explain_code():
    """API endpoint to explain code and suggest optimizations."""
    data = request.get_json()
    code_snippet = data.get('code', '')
    
    if not code_snippet.strip():
        return jsonify({"error": "No code provided"}), 400
    
    # Generate explanation using Hugging Face
    prompt = f"Explain the following Python code in plain English:\n\n{code_snippet}"
    payload = {"inputs": prompt, "parameters": {"max_length": 512}}
    result = query_hugging_face(payload)
    
    if isinstance(result, dict) and "error" in result:
        return jsonify({"error": result["error"]}), 500
    
    explanation = result[0]["generated_text"] if result else "No explanation generated."
    
    # Suggest optimizations (rule-based)
    suggestions = []
    if "class Heap" in code_snippet or "heapify" in code_snippet.lower():
        suggestions.append("Consider using Python's heapq module for a more efficient and tested heap implementation.")
    if "def sort" in code_snippet or "bubble" in code_snippet.lower():
        suggestions.append("Replace custom sorting with Python's sorted() or list.sort() for better performance.")
    if "class " in code_snippet and "def _init_" in code_snippet:
        suggestions.append("Ensure proper encapsulation using private attributes (e.g., _variable) and consider design patterns like Singleton if applicable.")
    if not suggestions:
        suggestions = ["No specific optimizations detected. Ensure code follows best practices."]
    
    return jsonify({
        "explanation": explanation,
        "optimizations": suggestions
    })