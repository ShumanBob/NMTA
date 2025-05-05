from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# ollama APT configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate" # local ollama server port
OLLAMA_MODEL_NAME = "NMTA-1.0" # model name

# define /chat endpoint to handle POST requests
@app.route("/chat", methods=["POST"])
def chat():
    # extract user message from json payload
    user_message = request.json.get("message", "")
    # make the structured prompt for llm
    prompt = f"""### Instruction:
{user_message}. Only use the provided course catalog information. Do not invent, assume, or expand beyond what is officially stated.

### Response:
"""
    # format request payload that is sent to ollama API
    payload = {
        "model": OLLAMA_MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "context": [],
    }

    try:
        # send a POST request to ollama with prompt payload
        response = requests.post(OLLAMA_API_URL, json=payload)
        result = response.json() # parse JSON response
        # extract model response
        model_output = result.get("response", "")

        # split if encountering the following
        if "### End" in model_output:
            model_output = model_output.split("### End")[0]

        # replace 202620 with Fall 2025; replace was with is
        model_output = model_output.replace("202620", "Fall 2025")
        model_output = model_output.replace("was", "is")
        # return the resulting response after post processing
        return jsonify({"response": model_output.strip()})

    except Exception as e:
        # print("Error talking to Ollama:", e)
        # return following if error is encountered
        return jsonify({"response": "Sorry, an error occurred."}), 500

if __name__ == "__main__":
    # run app on port 5001
    app.run(port=5001, debug=False)