# Thirukkural API & Web App

This project is a Flask-based web application and API that allows users to search for Thirukkural verses, retrieve explanations, and generate short stories based on the Kurals.

## Features
- Search for Thirukkural by number or keyword (Tamil/English)
- API endpoints to fetch Kural details and generate stories
- A simple web UI for users to search and view Kurals
- SQLite database integration

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/thirukkural-api.git
cd thirukkural-api
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Database
- Ensure you have `thirukkural_data.csv` in the project directory.
- Run the Flask app once to initialize the database:
```bash
python app.py
```

---

## API Endpoints

### 1. Get a Kural by Number
**Endpoint:** `GET /kural/<number>`  
**Example:** `GET /kural/2`
```json
{
  "kural_no": 2,
  "kural_tamil": "கற்றதனால் ஆய பயனென்கொல்...",
  "kural_english": "What profit hath learning...
}
```

### 2. Search for Kurals
**Endpoint:** `GET /search?keyword=<query>`  
**Example:** `GET /search?keyword=wisdom`
```json
[
  {
    "kural_no": 2,
    "kural_tamil": "...",
    "kural_english": "..."
  }
]
```

### 3. Generate a Story for a Kural
**Endpoint:** `GET /story/<number>`  
**Example:** `GET /story/2`
```json
{
  "story": "A wise man followed this Kural..."
}
```

---

## Running the Web App
To start the Flask server, run:
```bash
python app.py
```
Then, open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Improving UI
If you want to enhance the UI, modify `templates/index.html` and `static/style.css`.

---

## Author
**Praveen Manoharan**  
[Zerrowtech](https://zerrowtech.com/praveen-manoharan/)

---

## Contributions
Feel free to fork this project and submit pull requests!

---

## License
This project is licensed under the MIT License.
