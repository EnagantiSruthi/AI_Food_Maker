from flask import Flask, render_template, request, jsonify
import json
from youtube_search import YoutubeSearch
import multiprocessing
import os

app = Flask(__name__)

def load_food_data():
    try:
        with open("food_data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def get_youtube_video(query):
    try:
        results = YoutubeSearch(f"{query} recipe", max_results=1).to_dict()
        if results:
            return f"https://www.youtube.com/watch?v={results[0]['id']}"
    except Exception:
        return "No video found. Please try a different recipe."
    return "No video found. Please try a different recipe."

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_food_details', methods=['POST'])
def get_food_details():
    food_name = request.form.get("food_name", "").strip().lower()
    
    if not food_name:
        return jsonify({
            "error": "Food name is required"
        }), 400
    
    food_data = load_food_data()

    if food_name in food_data:
        ingredients = ", ".join(food_data[food_name].get("ingredients", []))
        instructions = food_data[food_name].get("instructions", "No instructions available.")
    else:
        ingredients = "Unknown ingredients"
        instructions = "Sorry, I don't have this recipe yet! But we have a video for you."

    youtube_link = get_youtube_video(food_name)

    return jsonify({
        "ingredients": ingredients,
        "instructions": instructions,
        "youtube_link": youtube_link
    })

if __name__ == '__main__':
    if os.name != "nt":
        multiprocessing.set_start_method("fork", force=True)
    app.run(debug=True, port=7860, host='0.0.0.0')
