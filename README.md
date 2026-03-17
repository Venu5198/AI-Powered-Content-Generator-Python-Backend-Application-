# AI-Powered Content Generator (Python Backend)

A powerful, full-stack application that leverages advanced AI models to automatically generate high-quality text content such as blog posts, marketing copy, and social media updates. The backend is powered by **Flask** and the **OpenRouter API**, managing AI interactions, data storage via **Pandas**, and serving a modern Vanilla HTML/JS frontend.

## Features ✨

- **Generate Content**: Input a topic, choose your tone (Professional, Casual, Enthusiastic, Informative), specify word count, and provide keywords to receive structured text generation.
- **Summarize Content**: Paste long texts to get concise, AI-powered summaries.
- **Keyword Focus**: Specifically generate SEO-focused content based around target keywords.
- **History Tracking**: All generated prompts and results are automatically stored in a `CSV` database using Pandas and easily readable via the UI's History Dashboard.
- **OpenRouter API**: Agnostically integrates with *OpenRouter's* API model routing to access cutting-edge Language Models dynamically without relying heavily on a single provider endpoint.

## Tech Stack 🛠

- **Backend Framework**: Python (Flask)
- **AI Integration**: OpenAI Python SDK (Configured for OpenRouter endpoints)
- **Data Management**: Pandas
- **Frontend**: HTML5, Vanilla CSS3 (Custom Properties), Vanilla JS (Fetch API)

## Installation & Setup 🚀

To run this application locally on your machine, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/Venu5198/AI-Powered-Content-Generator-Python-Backend-Application-.git
cd AI-Powered-Content-Generator-Python-Backend-Application-
```

### 2. Create a Virtual Environment and Install Dependencies
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix/MacOS
# source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory (alongside `requirements.txt`). Add the following keys, putting in your OpenRouter API key:

```env
FLASK_ENV=development
FLASK_APP=run.py
OPENROUTER_API_KEY=your_openrouter_api_key_here
SITE_URL=http://localhost:5000
SITE_NAME=AI-Content-Generator
```

### 4. Run the Application
Start the Flask development server:
```bash
python run.py
```

Navigate to `http://localhost:5000` in your web browser to use the application interface.

## Project Structure 📁

```text
ai-content-generator/
│
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── routes.py            # API endpoint definitions
│   ├── services/
│   │   ├── ai_service.py    # OpenRouter API interaction logic
│   │   └── data_service.py  # Pandas data processing & CSV storage
│
├── templates/               
│   └── index.html           # Frontend interface
├── static/                  
│   ├── css/style.css
│   └── js/main.js
├── data/                    # Stores generation_history.csv
├── config/                  
│   └── settings.py          # App configuration pulling from .env
│
├── requirements.txt         # Project dependencies
└── run.py                   # Application entry point
```

## API Design 📡

The Flask API endpoints can be directly interfaced with using JSON payloads.

- `POST /generate-content`: Generates text based on `topic`, `tone`, `word_count`, and `keywords`.
- `POST /summarize-content`: Requires `text` and `max_length`. Returns a summary.
- `POST /keyword-content`: Requires `topic` and `keywords`. Generates an SEO article.
- `GET /history`: Returns generation history formatted as JSON arrays object.

## Future Enhancements 🔮
- Migrate the Pandas CSV storage to a robust relational database (PostgreSQL) for production caching scaling.
- Create automated scheduled content workflows (via Celery/Redis).
- Extend the API for Multilingual Generation logic routines. 
