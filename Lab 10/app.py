import os
from flask import Flask, render_template, request, jsonify

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

styles = {
    "minimalist": "Think neutral colors like beige, white, and black. Clean lines and simple accessories are key.",
    "vintage": "Go for 90s style denim, oversized sweaters, or classic retro patterns. Very Pinterest-coded!",
    "formal": "A sharp blazer, tailored trousers, or a sophisticated midi dress would work perfectly.",
    "streetwear": "Oversized hoodies, cargo pants, and chunky sneakers. Comfort meets style.",
    "aesthetic": "Focus on pastels, soft lighting vibes, and Y2K inspired accessories.",
    "party": "Sequins, bold colors, or a sleek black outfit with statement jewelry.",
    "default": "Tell me a vibe like Minimalist, Vintage, Streetwear, or Formal and I'll style you!"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def get_style():
    user_input = request.json.get("text").lower()
    response = styles["default"]
    for key in styles:
        if key in user_input:
            response = styles[key]
            break
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)