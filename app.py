from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
from datetime import date
from ChatMemory import ChatMemory
import os

load_dotenv()

app = Flask(__name__)
CORS(app)  

client = Groq(api_key=os.getenv("Groq_API"))

@app.route("/")
def home():
    return jsonify({"message": "AstroBot API is running 🚀"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("message", "")
    print('Received Query:', query)

    if not query:
        return jsonify({"response": "it looks your query is empty\nHow can i help with"})

    memory=ChatMemory(SystemPrompt=f'You are AstroBot, a helpful astrology assistant. todays date is {date.today()}. dont introduce yourself again and again')
    memory.UserInp(query)
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=memory.get_context(),
            temperature=0.7,
            max_tokens=1000,
            stream=False
        )

        response_text = completion.choices[0].message.content
        memory.BotResp(response_text)
        return jsonify({"response": response_text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)