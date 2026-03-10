# 🤖 Personal AI Blog — Flask + NLP

A personal blog website built with **Python Flask**, featuring AI-powered **Sentiment Analysis** and **Keyword Extraction**. Designed as a mini-project for AI/ML Engineering students.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 CRUD Operations | Create, Read, Update, Delete blog posts |
| 🔍 Search | Search posts by title or content keywords |
| 🧠 Sentiment Analysis | Auto-classifies posts as Positive / Negative / Neutral (TextBlob) |
| 🏷️ Keyword Extraction | Extracts top-5 keywords using RAKE algorithm |
| 📱 Responsive UI | Modern dark-themed design with Bootstrap 5 |
| 🗄️ SQLite Database | Lightweight database via SQLAlchemy ORM |

---

## 🛠️ Technology Stack

- **Backend:** Python 3, Flask
- **Database:** SQLite + Flask-SQLAlchemy
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **AI/NLP:** TextBlob, rake-nltk, NLTK
- **Icons:** Bootstrap Icons

---

## 📂 Project Structure

```
personal blog site/
├── app.py                  # Flask app with all routes
├── config.py               # Configuration (DB URI, secret key)
├── models.py               # SQLAlchemy database models
├── ai_utils.py             # AI/ML: sentiment analysis + keyword extraction
├── wsgi.py                 # WSGI entry point for production
├── requirements.txt        # Python dependencies
├── Procfile                # Render / Railway start command
├── vercel.json             # Vercel deployment config
├── runtime.txt             # Python version for cloud platforms
├── .gitignore              # Git ignore rules
├── blog.db                 # SQLite database (auto-created on first run)
├── static/
│   └── css/
│       └── style.css       # Custom dark-theme styles
└── templates/
    ├── base.html           # Base layout with navbar & footer
    ├── home.html           # Homepage with post cards
    ├── post.html           # Individual post page
    ├── create.html         # Create new post form
    ├── edit.html           # Edit existing post form
    ├── about.html          # About page (AI/ML explanation)
    └── search.html         # Search results page
```

---

## 🚀 How to Run Locally

### Prerequisites
- **Python 3.8+** installed on your system.

### Step 1 — Clone / Open the Project
Open a terminal and navigate to the project folder:
```bash
cd "personal blog site"
```

### Step 2 — Create a Virtual Environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Download NLTK Data (one-time setup)
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"
```

### Step 5 — Run the Application
```bash
python app.py
```

### Step 6 — Open in Browser
Visit: **http://127.0.0.1:5000**

---

## ☁️ Deploy to Cloud

The project is pre-configured for **Render**, **Railway**, and **Vercel**. Push your code to a GitHub repo first.

### Option 1 — Deploy to Render (Recommended)

1. Push your code to **GitHub**.
2. Go to [render.com](https://render.com) → **New** → **Web Service**.
3. Connect your GitHub repo.
4. Render will auto-detect the settings. Verify:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
5. Add **Environment Variables** in the Render dashboard:
   - `SECRET_KEY` = (any random string)
   - `DATABASE_URL` = (optional — Render provides this if you add a Postgres database)
6. Click **Deploy**. Your app will be live at `https://your-app.onrender.com`.

> **Note:** SQLite works on Render but data resets on each deploy. For persistent data, add a **Render Postgres** database and use the `DATABASE_URL` it provides. To use Postgres, also run: `pip install psycopg2-binary` and add it to `requirements.txt`.

### Option 2 — Deploy to Railway

1. Push your code to **GitHub**.
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**.
3. Select your repo. Railway auto-detects the `Procfile`.
4. Add **Environment Variables**:
   - `SECRET_KEY` = (any random string)
5. Optionally add a **Postgres plugin** — Railway auto-sets `DATABASE_URL`.
6. Click **Deploy**. Your app goes live automatically.

### Option 3 — Deploy to Vercel

1. Install the Vercel CLI: `npm i -g vercel`
2. In the project folder, run:
   ```bash
   vercel
   ```
3. Follow the prompts to link your project.
4. Add environment variables in the Vercel dashboard:
   - `SECRET_KEY` = (any random string)
5. Deploy: `vercel --prod`

> **Note:** Vercel's serverless functions have a read-only filesystem, so SQLite writes won't persist. For production on Vercel, use an external database (e.g., Supabase, PlanetScale) and set `DATABASE_URL`.

---

## 🧠 How the AI/ML Features Work

### 1. Sentiment Analysis (TextBlob)

TextBlob uses a **pre-trained sentiment lexicon** — a dictionary of English words with polarity scores ranging from **-1.0** (very negative) to **+1.0** (very positive).

**Process:**
1. The blog content is passed to `TextBlob(text)`.
2. TextBlob tokenises the text into words.
3. Each word's polarity is looked up in the lexicon.
4. The individual polarities are averaged into a single **polarity score**.
5. The score is mapped to a label:
   - **Positive** → score > 0.1
   - **Negative** → score < -0.1
   - **Neutral** → between -0.1 and 0.1

### 2. Keyword Extraction (RAKE)

RAKE (Rapid Automatic Keyword Extraction) is an **unsupervised, domain-independent** algorithm.

**Process:**
1. The text is split at stopwords and punctuation to create candidate phrases.
2. A word co-occurrence matrix is built from these phrases.
3. Each word is scored: `score = degree(word) / frequency(word)`.
4. Phrase scores are computed by summing their word scores.
5. The top-5 phrases (by score) are returned as keywords.

---

## 📸 Pages Overview

| Page | URL | Description |
|---|---|---|
| Home | `/` | All posts in reverse chronological order |
| Create | `/create` | Form to write a new post |
| Post | `/post/<id>` | Full post with AI analysis panels |
| Edit | `/edit/<id>` | Edit an existing post |
| Search | `/search?q=keyword` | Search results page |
| About | `/about` | AI/ML features explanation |

---

## 📄 Database Schema

**Table: `blog_post`**

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-incremented primary key |
| `title` | VARCHAR(200) | Post title |
| `content` | TEXT | Full post body |
| `author` | VARCHAR(100) | Author name |
| `category` | VARCHAR(50) | User-selected category |
| `sentiment` | VARCHAR(20) | AI-generated: Positive / Negative / Neutral |
| `sentiment_score` | FLOAT | Polarity score (-1.0 to 1.0) |
| `keywords` | VARCHAR(500) | Comma-separated extracted keywords |
| `date_posted` | DATETIME | Creation timestamp |

---

## 📝 License

This project is intended for educational purposes. Feel free to use and modify it.
