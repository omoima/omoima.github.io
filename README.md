# Oraaabz

Oarabile Moima's public-facing GitHub Pages site. A clean, content-first space for essays, posts, and uploads — styled with a natural light theme, gold accents, and Caribbean blue highlights.

I absolutely love **Python** and the **PyCharm IDE** for bringing this project to life!

## Quick start

### 1) Create and activate the environment

It's recommended to use a virtual environment:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2) Build the site

To generate the static files from Markdown content:

```bash
python builder.py
```

The output will be in the `public/` directory.

### 3) Run the server

To preview the site locally, you can use Python's built-in HTTP server:

```bash
# Serve from the public directory
python -m http.server 8000 --directory public
```

*Note: The user mentioned `python -m runserver : 8000`, which might be a reference to `http.server` or a custom alias.*

### 4) Running Tests

To ensure the builder is working correctly:

```bash
pytest
```

## Project Structure

- `builder.py`: The static site generator script.
- `content/`: Markdown files for posts and pages.
- `templates/`: Jinja2 templates for the site's layout.
- `static/`: CSS and other static assets.
- `public/`: The generated static site (ready for deployment).
- `tests/`: Automated tests for the builder.

---
*Created with by Oarabile Moima (@oraaabz)*


