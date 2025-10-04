from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# --- a tiny keyword-based "NLP" layer (no cloud, very simple) ---

POSITIVE_WORDS = {"great", "good", "awesome", "love", "like", "amazing", "helpful"}
NEGATIVE_WORDS = {"bad", "terrible", "hate", "dislike", "awful", "confusing", "broken"}

INTENTS = {
    "greeting": [
        r"\bhello\b", r"\bhi\b", r"\bhey\b"
    ],
    "hours": [
        r"\bhours\b", r"\bopen\b", r"\bclosing\b"
    ],
    "returns": [
        r"\breturn\b", r"\brefund\b", r"\bexchange\b"
    ]
}

def match_intent(text):
    text_l = text.lower()
    for intent, patterns in INTENTS.items():
        for p in patterns:
            if re.search(p, text_l):
                return intent
    return None

def tiny_sentiment(text):
    """
    Very small heuristic:
    +1 for each positive keyword, -1 for each negative keyword.
    """
    tokens = re.findall(r"\w+", text.lower())
    score = 0
    for t in tokens:
        if t in POSITIVE_WORDS:
            score += 1
        if t in NEGATIVE_WORDS:
            score -= 1
    # Map to label
    if score > 0:
        label = "positive"
    elif score < 0:
        label = "negative"
    else:
        label = "neutral"
    return {"score": score, "label": label}

def respond(intent, sentiment_label):
    # simple routing by intent + add a little variation by sentiment label
    if intent == "greeting":
        return "Hi there! How can I help you today?"
    if intent == "hours":
        return "Our typical store hours are 10am–8pm, Mon–Sat, and 11am–6pm on Sun."
    if intent == "returns":
        return "You can return most items within 30 days with receipt. Would you like a quick link to the policy?"

    # default / unknown intent
    if sentiment_label == "negative":
        return "I’m sorry this is frustrating. Can you tell me a bit more so I can help?"
    return "Got it! Could you share a little more detail so I can assist?"

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    user_text = (data.get("text") or "").strip()
    if not user_text:
        return jsonify({"error": "Empty message. Please type something."}), 400

    sent = tiny_sentiment(user_text)
    intent = match_intent(user_text)
    bot_text = respond(intent, sent["label"])

    return jsonify({
        "intent": intent or "unknown",
        "sentiment": sent,
        "bot": bot_text
    })

if __name__ == "__main__":
    # Run locally
    app.run(host="127.0.0.1", port=5000, debug=True)
