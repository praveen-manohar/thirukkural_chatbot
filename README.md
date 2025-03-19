# Thirukkural API & Web App

This project is a **Flask-based REST API and Web Application** that allows users to search for Thirukkural verses, retrieve detailed explanations, and explore random Kurals. It supports both **GET URL-based searches** and **POST JSON requests** for flexibility in web and app integrations.

---

## ⭐️ Features

- 🔍 **Search Thirukkural** by number or keyword (Tamil & English support).
- 🎲 **Fetch random Kurals** with full explanations.
- 🌐 **API endpoints** for seamless integration with apps and websites.
- 💻 **Web-based UI** for direct searching and viewing Kurals.
- 🗄️ **SQLite database** backend for storing Kural data.

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/thirukkural-api.git
cd thirukkural-api
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Database

- Make sure you have `thirukkural_data.csv` in your project directory.
- Run the Flask app once to initialize the SQLite database:

```bash
python app.py
```

---

## 📡 API Endpoints

### 1. **Search for Kurals or Get by Number**

**Endpoint:** `GET or POST /api/chat`

#### a. Search using GET (query param):

```
GET /api/chat?query=love
```

#### b. Search using POST (JSON):

```bash
POST /api/chat
Content-Type: application/json
{
  "query": "love"
}
```

#### ✅ **Response Example:**

```json
{
  "type": "search",
  "query": "love",
  "results": [
    {
      "kural_no": 80,
      "kural_tamil": "அன்பும் அறனும் உடைத்தென்பர் ஆற்றின்...",
      "kural_english": "They say love and virtue dwell together...",
      "explanation_tamil": "...",
      "explanation_english": "..."
    }
  ]
}
```

---

### 2. **Get a Random Kural**

**Endpoint:** `GET /api/random`

#### ✅ **Example:**

```
GET /api/random
```

#### ✅ **Response Example:**

```json
{
  "kural_no": 45,
  "kural_tamil": "அறவாழி அந்தணன் தாள்சேர்ந்தார்...",
  "kural_english": "Those who have reached the feet of the virtuous...",
  "explanation_tamil": "...",
  "explanation_english": "..."
}
```

---

## 🌍 Web Interface (Optional)

You can also search and read Kurals through a simple web interface.

### Run the app:

```bash
python app.py
```

### Open in browser:

```
http://127.0.0.1:5000
```

---

## 🎨 Improving the UI

- **HTML Templates**: `templates/index.html`
- **CSS Styling**: `static/style.css`

You can customize these files to improve user experience.

---

## 🧑‍💻 Author

**Praveen Manoharan**  
[Zerrowtech](https://zerrowtech.com/praveen-manoharan/)


---

## 🤝 Contributions

- Fork this repository and create a pull request for improvements.
- Feel free to suggest additional features and report issues!

---

## 📜 License

This project is licensed under the **MIT License** — free for personal and commercial use.

---

### 🔗 Example API Call Using Fetch (Frontend JavaScript)

```javascript
fetch('http://127.0.0.1:5000/api/chat?query=love')
  .then(response => response.json())
  .then(data => console.log(data));



