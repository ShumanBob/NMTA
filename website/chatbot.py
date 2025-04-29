from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL_NAME = "NMTA"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    prompt = f"""### Instruction:
{user_message}. Only use the provided course catalog information. Do not invent, assume, or expand beyond what is officially stated.

### Response:
"""

    payload = {
        "model": OLLAMA_MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "context": [],
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        result = response.json()
        model_output = result.get("response", "")

        if "### End" in model_output:
            model_output = model_output.split("### End")[0]

        return jsonify({"response": model_output.strip()})

    except Exception as e:
        print("Error talking to Ollama:", e)
        return jsonify({"response": "Sorry, an error occurred."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
