from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd
import os
import re
import string


app = Flask(__name__)
CORS(app)  # Enable CORS

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///thirukkural.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Database Model
class Thirukkural(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kural_no = db.Column(db.Integer, unique=True, nullable=False)
    kural_tamil = db.Column(db.Text, nullable=False)
    kural_english = db.Column(db.Text, nullable=False)
    explanation_tamil = db.Column(db.Text)
    explanation_english = db.Column(db.Text)
    category = db.Column(db.String(50))

# Create Database and Load Data (if empty)
with app.app_context():
    db.create_all()
    if not Thirukkural.query.first() and os.path.exists("thirukkural_data.csv"):
        df = pd.read_csv("thirukkural_data.csv")
        for _, row in df.iterrows():
            if not Thirukkural.query.filter_by(kural_no=row["kural_no"]).first():
                new_kural = Thirukkural(
                    kural_no=row["kural_no"],
                    kural_tamil=row["kural_tamil"],
                    kural_english=row["kural_english"],
                    explanation_tamil=row.get("explanation_tamil", ""),
                    explanation_english=row.get("explanation_english", ""),
                    category=row.get("category", "")
                )
                db.session.add(new_kural)
        db.session.commit()

# ----------------- API ROUTES ---------------- #

# API: Chat-style query to get Kural by number or keyword
@app.route("/api/chat", methods=["GET", "POST"])
def chat_bot():
    if request.method == "POST":
        data = request.get_json()
        user_query = data.get("query", "").strip().lower() if data else ""
    else:  # GET method
        user_query = request.args.get("query", "").strip().lower()

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    # Extract number if present
    numbers = re.findall(r'\d+', user_query)
    if numbers:
        kural_number = int(numbers[0])  # Take first number found

        if not (1 <= kural_number <= 1330):
            return jsonify({
                "error": "Invalid Kural number! Please enter a number between 1 and 1330.",
                "query": user_query
            }), 400
        kural = Thirukkural.query.filter_by(kural_no=kural_number).first()
        if kural:
            return jsonify({
                "type": "kural",
                "query": user_query,
                "kural_no": kural.kural_no,
                "kural_tamil": kural.kural_tamil,
                "kural_english": kural.kural_english,
                "explanation_tamil": kural.explanation_tamil,
                "explanation_english": kural.explanation_english
            })

    # Search by keyword (both exact phrase and split words)
    kurals = Thirukkural.query.all()

    # First, try exact phrase matching
    exact_matched_kurals = [
        k for k in kurals
        if user_query in k.kural_english.lower() or user_query in k.kural_tamil.lower()
    ]

    if exact_matched_kurals:
        results = [dict(
            kural_no=k.kural_no,
            kural_tamil=k.kural_tamil,
            kural_english=k.kural_english,
            explanation_tamil=k.explanation_tamil,
            explanation_english=k.explanation_english
        ) for k in exact_matched_kurals[:3]]  # Limit to 3 results
        return jsonify({
            "type": "search",
            "query": user_query,
            "results": results
        })

    # Clean and If no exact match, try split word matching
    query_words = [word.strip(string.punctuation).lower() for word in user_query.split() if word.strip(string.punctuation)]

    word_matched_kurals = [
        k for k in kurals
        if any(word in k.kural_english.lower() or word in k.kural_tamil.lower() for word in query_words)
    ]

    if word_matched_kurals:
        results = [dict(
            kural_no=k.kural_no,
            kural_tamil=k.kural_tamil,
            kural_english=k.kural_english,
            explanation_tamil=k.explanation_tamil,
            explanation_english=k.explanation_english
        ) for k in word_matched_kurals[:3]]  # Limit to 3 results
        return jsonify({
            "type": "search",
            "query": user_query,
            "results": results
        })

    # Not found
    return jsonify({
        "message": "Sorry, I couldn't find any Kural matching your query.",
        "query": user_query
    }), 404



# API: Random Kural
@app.route("/api/random", methods=["GET"])
def random_kural():
    kural = Thirukkural.query.order_by(db.func.random()).first()
    if kural:
        return jsonify({
            "kural_no": kural.kural_no,
            "kural_tamil": kural.kural_tamil,
            "kural_english": kural.kural_english,
            "explanation_tamil": kural.explanation_tamil,
            "explanation_english": kural.explanation_english
        })
    return jsonify({"error": "No Kurals found"}), 404

# Home Route
@app.route("/")
def home():
    return render_template("index.html")

# ----------------- Run Server ---------------- #
if __name__ == "__main__":
    app.run(debug=True)
