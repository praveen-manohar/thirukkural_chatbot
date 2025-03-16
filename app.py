<<<<<<< HEAD
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///thirukkural.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Create Database Model
class Thirukkural(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kural_no = db.Column(db.Integer, unique=True, nullable=False)
    kural_tamil = db.Column(db.Text, nullable=False)
    kural_english = db.Column(db.Text, nullable=False)
    explanation_tamil = db.Column(db.Text)
    explanation_english = db.Column(db.Text)
    category = db.Column(db.String(50))

# Create Database and Load Data (Only if Not Exists)
with app.app_context():
    db.create_all()
    if not Thirukkural.query.first() and os.path.exists("thirukkural_data.csv"):
        df = pd.read_csv("thirukkural_data.csv")
        for index, row in df.iterrows():
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

# API to get a specific Kural by number
@app.route("/api/kural/<int:number>", methods=["GET"])
def get_kural(number):
    kural = Thirukkural.query.filter_by(kural_no=number).first()
    if kural:
        return jsonify({
            "kural_no": kural.kural_no,
            "kural_tamil": kural.kural_tamil,
            "kural_english": kural.kural_english,
            "explanation_tamil": kural.explanation_tamil,
            "explanation_english": kural.explanation_english
        })
    return jsonify({"error": "Kural not found"}), 404

# API to search Kurals by a keyword
@app.route("/api/search", methods=["GET"])
def search_kural():
    keyword = request.args.get("keyword", "").strip().lower()
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    if keyword.isdigit():  # Check if the keyword is a number
        kural = Thirukkural.query.filter_by(kural_no=int(keyword)).first()
        if kural:
            return jsonify([{
                "kural_no": kural.kural_no,
                "kural_tamil": kural.kural_tamil,
                "kural_english": kural.kural_english,
                "explanation_tamil": kural.explanation_tamil,
                "explanation_english": kural.explanation_english
            }])
        return jsonify({"message": "No matching Kural found"}), 404

    # If keyword is not a number, search in Tamil and English text
    kurals = Thirukkural.query.all()
    matched_kurals = [
        k for k in kurals
        if keyword in k.kural_english.lower() or keyword in k.kural_tamil.lower()
    ]

    if matched_kurals:
        results = [{
            "kural_no": k.kural_no,
            "kural_tamil": k.kural_tamil,
            "kural_english": k.kural_english,
            "explanation_tamil": k.explanation_tamil,
            "explanation_english": k.explanation_english
        } for k in matched_kurals]
        return jsonify(results[:3])  # Return top 3 matches

    return jsonify({"message": "No matching Kural found"}), 404

# API to generate a short story for a given Kural number
@app.route("/api/story/<int:number>", methods=["GET"])
def generate_story(number):
    kural = Thirukkural.query.filter_by(kural_no=number).first()
    if kural:
        story = f"A wise man once followed this Kural: '{kural.kural_english}'. One day, he faced a great challenge..."
        return jsonify({"story": story})
    return jsonify({"error": "Kural not found"}), 404

# UI Route
@app.route("/")
def home():
    return render_template("index.html")

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
=======
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///thirukkural.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Create Database Model
class Thirukkural(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kural_no = db.Column(db.Integer, unique=True, nullable=False)
    kural_tamil = db.Column(db.Text, nullable=False)
    kural_english = db.Column(db.Text, nullable=False)
    explanation_tamil = db.Column(db.Text)
    explanation_english = db.Column(db.Text)
    category = db.Column(db.String(50))

# Create Database and Load Data (Only if Not Exists)
with app.app_context():
    db.create_all()
    if not Thirukkural.query.first() and os.path.exists("thirukkural_data.csv"):
        df = pd.read_csv("thirukkural_data.csv")
        for index, row in df.iterrows():
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

# API to get a specific Kural by number
@app.route("/api/kural/<int:number>", methods=["GET"])
def get_kural(number):
    kural = Thirukkural.query.filter_by(kural_no=number).first()
    if kural:
        return jsonify({
            "kural_no": kural.kural_no,
            "kural_tamil": kural.kural_tamil,
            "kural_english": kural.kural_english,
            "explanation_tamil": kural.explanation_tamil,
            "explanation_english": kural.explanation_english
        })
    return jsonify({"error": "Kural not found"}), 404

# API to search Kurals by a keyword
@app.route("/api/search", methods=["GET"])
def search_kural():
    keyword = request.args.get("keyword", "").strip().lower()
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    if keyword.isdigit():  # Check if the keyword is a number
        kural = Thirukkural.query.filter_by(kural_no=int(keyword)).first()
        if kural:
            return jsonify([{
                "kural_no": kural.kural_no,
                "kural_tamil": kural.kural_tamil,
                "kural_english": kural.kural_english,
                "explanation_tamil": kural.explanation_tamil,
                "explanation_english": kural.explanation_english
            }])
        return jsonify({"message": "No matching Kural found"}), 404

    # If keyword is not a number, search in Tamil and English text
    kurals = Thirukkural.query.all()
    matched_kurals = [
        k for k in kurals
        if keyword in k.kural_english.lower() or keyword in k.kural_tamil.lower()
    ]

    if matched_kurals:
        results = [{
            "kural_no": k.kural_no,
            "kural_tamil": k.kural_tamil,
            "kural_english": k.kural_english,
            "explanation_tamil": k.explanation_tamil,
            "explanation_english": k.explanation_english
        } for k in matched_kurals]
        return jsonify(results[:3])  # Return top 3 matches

    return jsonify({"message": "No matching Kural found"}), 404

# API to generate a short story for a given Kural number
@app.route("/api/story/<int:number>", methods=["GET"])
def generate_story(number):
    kural = Thirukkural.query.filter_by(kural_no=number).first()
    if kural:
        story = f"A wise man once followed this Kural: '{kural.kural_english}'. One day, he faced a great challenge..."
        return jsonify({"story": story})
    return jsonify({"error": "Kural not found"}), 404

# UI Route
@app.route("/")
def home():
    return render_template("index.html")

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 657bc41 (Initial commit - Thirukkural Chatbot)
