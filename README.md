YouTube Script Assistant 🎬

An AI-powered video content generation tool that helps YouTube creators turn a video idea into a structured content plan, full script, visual suggestions, and YouTube description.

✨ Features

- AI-Generated Video Titles: Generate multiple title ideas for your topic.
- Opening Hooks: Create engaging opening hooks to capture viewers' attention.
- Video Outline: Generate a structured outline for your video.
- Full Script Generation: Turn your selected title, hook, and outline into a complete video script.
- Script Editing: Edit and save your generated script.
- Section Regeneration: Regenerate individual script sections.
- Visual Suggestions: Generate visual ideas, B-roll suggestions, and on-screen text for different script sections.
- YouTube Description: Generate an introduction, summary, topics, keywords, hashtags, and call to action.
- Copy and Download: Copy the full script or download it as a text file.
- Saved Scripts: Save, search, reopen, update, and delete previously generated scripts.

🛠️ Tech Stack

Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Gemini API

Database

- MySQL

Frontend

- HTML
- CSS
- JavaScript

Testing

- Pytest

📁 Project Structure

youtube_script_assistant/
│
├── app/
│   ├── routers/
│   ├── models/
│   ├── schemas/
│   └── ...
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── css/
│       └── style.css
│
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

⚙️ Installation and Setup

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd youtube_script_assistant

2. Create a virtual environment

python -m venv venv

Activate it:

Windows PowerShell

.\venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a ".env" file in the project root using ".env.example" as a reference.

Configure the following variables:

- "GEMINI_API_KEY": Your Gemini API key.
- "GEMINI_MODEL": The Gemini model used for content generation.
- "DATABASE_URL": Your MySQL database connection URL.

Never commit your actual ".env" file, API key, or database credentials to GitHub.

5. Start the backend

uvicorn app.main:app --reload

Backend URL:

"http://127.0.0.1:8000"

API documentation:

"http://127.0.0.1:8000/docs"

6. Run the frontend

Open "frontend/index.html" using the VS Code Live Server extension.

🧪 Run Tests

Run the automated test suite from the project root:

python -m pytest -v

📸 Screenshots

Project screenshots will be added here.

🔮 Future Improvements

- Deploy the application online.
- Add support for additional AI models.
- Improve generation reliability with retry and fallback handling.
- Add more export formats.

👨‍💻 Author

Subrat Dubey

Aspiring AI Engineer | Python Developer | Generative AI & Automation

---

Built as a portfolio project to explore Generative AI, backend development, APIs, and AI-powered content automation.