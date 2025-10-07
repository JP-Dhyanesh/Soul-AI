import json
import google.generativeai as genai

# Configure Gemini
API_KEY = "AIzaSyDh2QRoZKoOIcVG4bYCxhAwtt9q_58ignI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")  # or a supported model from list_models()

# Load your emotion dataset
with open("traindata.json", "r", encoding="utf-8") as f:
    emotion_data = json.load(f)

# Organize dataset by emotion for fast lookup
emotion_examples = {
    "happy": [],
    "sad": [],
    "angry": [],
    "fearful": [],
    "disgusted": [],
    "surprised": [],
    "neutral": []
}

# Map keywords to emotion
emotion_keywords = {
    "happy": ["happy", "excited", "amazing", "good vibes", "joy", "glad"],
    "sad": ["sad", "cry", "alone", "give up", "drained", "nothing goes right"],
    "angry": ["angry", "mad", "frustrated", "upset", "irritated"],
    "fearful": ["scared", "afraid", "anxious", "worried", "terrified"],
    "disgusted": ["gross", "disgusted", "sick", "unpleasant"],
    "surprised": ["shocked", "wow", "unexpected", "surprised"],
    "neutral": ["okay", "fine", "meh", "nothing special", "average"]
}

# Populate emotion_examples
for entry in emotion_data:
    for emotion in emotion_examples.keys():
        if emotion in entry["prompt"].lower():
            emotion_examples[emotion].append(entry)

# Detect user emotion
def detect_emotion(user_text: str) -> str:
    user_text_lower = user_text.lower()
    for emotion, keywords in emotion_keywords.items():
        if any(word in user_text_lower for word in keywords):
            return emotion
    return "neutral"

# Pick best example for LLM context
def pick_example(user_text: str) -> dict:
    emotion = detect_emotion(user_text)
    examples = emotion_examples.get(emotion)
    if examples:
        # Pick the one with prompt most similar to user_text (optional: can improve with NLP similarity)
        return examples[0]  # simple: pick first match
    return {"prompt": user_text, "response": ""}

# Get response from Gemini
def get_response(user_text: str) -> str:
    try:
        example = pick_example(user_text)
        context = (
            f"User emotion detected: {detect_emotion(user_text)}.\n"
            f"Example conversation:\n{example['prompt']} {example['response']}\n\n"
            f"Now respond empathetically to the user message below:\nUser: {user_text}\nBot:"
        )

        response = model.generate_content(context)
        return response.text.strip()

    except Exception as e:
        return f"Error: {str(e)}"
