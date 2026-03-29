from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)
GROQ_API_KEY = "your_groq_api_key_here"

client = Groq(api_key=GROQ_API_KEY)
with open("knowledge.txt", "r", encoding="utf-8") as f:
    knowledge = f.read()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if user_message.lower() in ["hi", "hello", "hey"]:
        return jsonify({"reply": "Hello! How can I assist you today with Cloud Infrastructure and Cloud Services?"})
    elif user_message.lower() in ["bye", "goodbye"]:
        return jsonify({"reply": "Goodbye! If you have any more questions, feel free to ask."})

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": f"Answer from this data ONLY: \n {knowledge} \n\nQuestion: {user_message}\n\nIf user asks for information not in the knowledge, respond with 'Sorry, I don't have that information.'"},
        ],
    ) 
    
    bot_reply = completion.choices[0].message.content.strip()
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":    
    app.run(debug=True)