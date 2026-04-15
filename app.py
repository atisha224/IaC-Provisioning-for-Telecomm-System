from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chatbot_response(user_input):
    try:
     
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a telecom support assistant. Help users with telecom issues like internet problems, plans, network issues, call drops, and balance queries. Give clear and helpful answers."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("LLM Error:", e)

        user_input = user_input.lower()

        if "internet not working" in user_input or "no internet" in user_input:
            return "Please check your data plan and restart your device. If the issue continues, contact customer support."

        elif "slow internet" in user_input or "slow wifi" in user_input:
            return "Slow internet may be due to network congestion. Try moving to a better signal area or restarting your router."

        elif "wifi not working" in user_input:
            return "Restart your router and ensure all cables are connected properly."

        elif "prepaid" in user_input:
            return "Prepaid plans require recharge before usage. Services stop when balance ends."

        elif "postpaid" in user_input:
            return "Postpaid plans allow you to use services first and pay later at the end of the billing cycle."

        elif "balance" in user_input:
            return "You can check your balance using USSD codes or your telecom app."

        elif "hello" in user_input or "hi" in user_input:
            return "Hello! 👋 I'm your Telecom Assistant. How can I help you?"

        else:
            return "I'm facing some issues right now. Please try asking about telecom services like internet, plans, or balance."


# Routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    response = chatbot_response(user_message)
    return jsonify({"response": response})


# Run app
if __name__ == "__main__":
    app.run(debug=True, port=5000)