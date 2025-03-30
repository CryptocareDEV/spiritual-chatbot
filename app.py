from flask import Flask, request, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from datetime import datetime
import random

app = Flask(__name__)

# Create the chatbot
spiritual_bot = ChatBot("SpiritualGuide")

# Train the chatbot with spiritual phrases
trainer = ListTrainer(spiritual_bot)
training_data = [
    "Hello", "Greetings, seeker of peace!",
    "How can I help you?", "I’m here to guide your soul. What do you seek?",
    "Tell me your zodiac sign", "Please share your zodiac sign for a reading.",
    "What should I do today?", "Let me suggest a spiritual act for you."
]
trainer.train(training_data)

# Devotional songs with YouTube links (you can replace with Spotify links)
songs = {
    "morning": [
        {"name": "Om Jai Jagdish Hare", "url": "https://www.youtube.com/watch?v=0gXvAV88DRo"},
        {"name": "Morning Raga", "url": "https://www.youtube.com/watch?v=HrjKPSL_QtM"},
        {"name": "Aarti Shri Ram", "url": "https://www.youtube.com/watch?v=Hr5Nudn23uY"}
    ],
    "afternoon": [
        {"name": "Bhajo Radhe Krishna", "url": "https://www.youtube.com/watch?v=5gFky9rLbsQ"},
        {"name": "Hanuman Chalisa", "url": "https://www.youtube.com/watch?v=AETFvQonfV8"},
        {"name": "Jai Ambe Gauri", "url": "https://www.youtube.com/watch?v=8nJ2LPhfDEw"}
    ],
    "evening": [
        {"name": "Gayatri Mantra", "url": "https://www.youtube.com/watch?v=nDnamSM3Z3s"},
        {"name": "Shiv Tandav Stotram", "url": "https://www.youtube.com/watch?v=1nTnlQdm7Q0"},
        {"name": "Krishna Bhajan", "url": "https://www.youtube.com/watch?v=5mXhW6iCuTM"}
    ]
}

# Spiritual acts
acts = ["Meditate for 10 minutes", "Offer a prayer", "Light a candle and reflect", "Chant a mantra"]

# Horoscope messages
horoscopes = {
    "aries": "A day of energy and courage awaits you.",
    "taurus": "Stability and patience will bring rewards.",
    "gemini": "Communication opens new doors today.",
    # Add more zodiac signs as needed
}

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Chat endpoint
@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["message"].lower()
    response = str(spiritual_bot.get_response(user_input))

    # Custom responses
    now = datetime.now()
    hour = now.hour

    # Song recommendation based on time with clickable link
    if "song" in user_input:
        if 5 <= hour < 12:
            song = random.choice(songs["morning"])
            return f'For the morning, enjoy: <a href="{song["url"]}" target="_blank">{song["name"]}</a>'
        elif 12 <= hour < 17:
            song = random.choice(songs["afternoon"])
            return f'For the afternoon, try: <a href="{song["url"]}" target="_blank">{song["name"]}</a>'
        else:
            song = random.choice(songs["evening"])
            return f'An evening song for your soul: <a href="{song["url"]}" target="_blank">{song["name"]}</a>'

    # Spiritual act suggestion
    elif "what should i do" in user_input:
        act = random.choice(acts)
        return f"Consider this spiritual act: {act}"

    # Horoscope and luck
    elif "zodiac" in user_input or "horoscope" in user_input:
        for sign in horoscopes:
            if sign in user_input:
                luck = random.randint(1, 100)
                return f"{horoscopes[sign]} Your chance of a good day: {luck}%"
        return "Please tell me your zodiac sign (e.g., Aries, Taurus)."

    return response

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)