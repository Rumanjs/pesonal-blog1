"""
app.py — Flask Application Entry Point
-----------------------------------------
This is the main file that creates the Flask app, registers all routes,
and starts the development server.

Routes:
    /               — Homepage (list all posts, newest first)
    /post/<id>      — View a single blog post
    /create         — Create a new blog post
    /edit/<id>      — Edit an existing blog post
    /delete/<id>    — Delete a blog post
    /search         — Search posts by title or content
    /about          — About page with AI/ML explanation
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, BlogPost
from ai_utils import analyze_sentiment, extract_keywords


# ── App Factory ─────────────────────────────────────────────────────────────


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration from our Config class
    app.config.from_object(Config)

    # Initialize the database with this app
    db.init_app(app)

    # Create all database tables if they don't exist yet
    with app.app_context():
        db.create_all()

    return app


# Create the app instance
app = create_app()


# ── ROUTES ──────────────────────────────────────────────────────────────────


# ──────────────────────────── Homepage ──────────────────────────────────────

@app.route("/")
def home():
    """
    Display all blog posts on the homepage.
    Posts are ordered by date in descending order (newest first).
    """
    # Query all posts, newest first
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template("home.html", posts=posts)


# ──────────────────────── Individual Post ───────────────────────────────────

@app.route("/post/<int:post_id>")
def post(post_id):
    """
    Display a single blog post by its ID.
    Returns 404 if the post doesn't exist.
    """
    # get_or_404 will automatically return a 404 error page if not found
    blog_post = BlogPost.query.get_or_404(post_id)
    return render_template("post.html", post=blog_post)


# ──────────────────────── Create Post ───────────────────────────────────────

@app.route("/create", methods=["GET", "POST"])
def create():
    """
    Handle the 'Create Post' form.
    GET  → show the empty form.
    POST → validate input, run AI analysis, save to database.
    """
    # Pre-defined categories for the dropdown
    categories = [
        "AI/ML",
        "Web Development",
        "Data Science",
        "Python",
        "Deep Learning",
        "General",
    ]

    if request.method == "POST":
        # ── Retrieve form data ──────────────────────────────────────────
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        author = request.form.get("author", "").strip() or "Anonymous"
        category = request.form.get("category", "General")

        # ── Validate required fields ───────────────────────────────────
        if not title or not content:
            flash("Title and Content are required!", "danger")
            return render_template(
                "create.html",
                categories=categories,
                title=title,
                content=content,
                author=author,
                category=category,
            )

        # ── Run AI/ML analysis ──────────────────────────────────────────
        sentiment_label, sentiment_score = analyze_sentiment(content)
        keywords = extract_keywords(content)
        keywords_str = ", ".join(keywords)  # Store as comma-separated string

        # ── Create and save the new post ────────────────────────────────
        new_post = BlogPost(
            title=title,
            content=content,
            author=author,
            category=category,
            sentiment=sentiment_label,
            sentiment_score=sentiment_score,
            keywords=keywords_str,
        )
        db.session.add(new_post)
        db.session.commit()

        flash("Blog post created successfully!", "success")
        return redirect(url_for("home"))

    # GET request — show the empty form
    return render_template("create.html", categories=categories)


# ──────────────────────── Edit Post ─────────────────────────────────────────

@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id):
    """
    Handle the 'Edit Post' form.
    GET  → pre-fill the form with the existing post data.
    POST → validate, re-run AI analysis, update the database.
    """
    blog_post = BlogPost.query.get_or_404(post_id)
    categories = [
        "AI/ML",
        "Web Development",
        "Data Science",
        "Python",
        "Deep Learning",
        "General",
    ]

    if request.method == "POST":
        # ── Retrieve updated form data ──────────────────────────────────
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        author = request.form.get("author", "").strip() or "Anonymous"
        category = request.form.get("category", "General")

        # ── Validate required fields ───────────────────────────────────
        if not title or not content:
            flash("Title and Content are required!", "danger")
            return render_template(
                "edit.html", post=blog_post, categories=categories
            )

        # ── Re-run AI/ML analysis on updated content ───────────────────
        sentiment_label, sentiment_score = analyze_sentiment(content)
        keywords = extract_keywords(content)
        keywords_str = ", ".join(keywords)

        # ── Update the post fields ──────────────────────────────────────
        blog_post.title = title
        blog_post.content = content
        blog_post.author = author
        blog_post.category = category
        blog_post.sentiment = sentiment_label
        blog_post.sentiment_score = sentiment_score
        blog_post.keywords = keywords_str

        db.session.commit()

        flash("Blog post updated successfully!", "success")
        return redirect(url_for("post", post_id=blog_post.id))

    # GET request — show form with current post data
    return render_template("edit.html", post=blog_post, categories=categories)


# ──────────────────────── Delete Post ───────────────────────────────────────

@app.route("/delete/<int:post_id>", methods=["POST"])
def delete(post_id):
    """
    Delete a blog post by its ID.
    Only accepts POST requests to prevent accidental deletion via URL.
    """
    blog_post = BlogPost.query.get_or_404(post_id)
    db.session.delete(blog_post)
    db.session.commit()

    flash("Blog post deleted successfully!", "info")
    return redirect(url_for("home"))


# ──────────────────────── Search ────────────────────────────────────────────

@app.route("/search")
def search():
    """
    Search blog posts by title or content.
    The search query is passed as a URL parameter: /search?q=keyword
    Uses SQL LIKE for simple substring matching.
    """
    query = request.args.get("q", "").strip()
    results = []

    if query:
        # Search in both title and content columns (case-insensitive via LIKE)
        search_pattern = f"%{query}%"
        results = BlogPost.query.filter(
            db.or_(
                BlogPost.title.ilike(search_pattern),
                BlogPost.content.ilike(search_pattern),
            )
        ).order_by(BlogPost.date_posted.desc()).all()

    return render_template("search.html", results=results, query=query)


# ──────────────────────── About Page ────────────────────────────────────────

@app.route("/about")
def about():
    """Display the About page with information about the AI/ML features."""
    return render_template("about.html")


# ── Run the Development Server ──────────────────────────────────────────────

if __name__ == "__main__":
    # debug=True enables auto-reload and detailed error pages during development
    app.run(debug=True)
