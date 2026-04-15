import os
import pytest
from bs4 import BeautifulSoup
from builder import parse_markdown, render_template, build_site

def test_parse_markdown():
    markdown_content = """---
title: Test Post
date: 2026-04-12
theme: africa
---
# Hello Africa
This is a test post about the *savannah*.
"""
    frontmatter, html_content = parse_markdown(markdown_content)
    
    assert frontmatter['title'] == 'Test Post'
    assert str(frontmatter['date']) == '2026-04-12'
    assert frontmatter['theme'] == 'africa'
    
    soup = BeautifulSoup(html_content, 'html.parser')
    assert soup.find('h1').text == 'Hello Africa'
    assert soup.find('em').text == 'savannah'

def test_parse_markdown_syntax_highlight():
    markdown_content = """---
title: Code Test
---
```python
print("Jambo")
```
"""
    _, html_content = parse_markdown(markdown_content)
    # The markdown extensions (fenced_code, codehilite) should add a 'code' element.
    assert 'class="codehilite"' in html_content or 'class="highlight"' in html_content or '<code' in html_content

def test_render_template(tmp_path):
    # Setup dummy template directory
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    
    base_template = template_dir / "base.html"
    base_template.write_text("<html><title>{{ title }}</title><body>{% block content %}{% endblock %}</body></html>")
    
    post_template = template_dir / "post.html"
    post_template.write_text("{% extends 'base.html' %}{% block content %}<article>{{ content|safe }}</article>{% endblock %}")
    
    html = render_template(str(template_dir), 'post.html', {'title': 'My Post', 'content': '<p>Hello</p>'})
    
    soup = BeautifulSoup(html, 'html.parser')
    assert soup.title.text == 'My Post'
    assert soup.find('article').find('p').text == 'Hello'

def test_build_site_default_title(tmp_path):
    # Setup skeleton project
    project_dir = tmp_path
    
    # Create templates
    template_dir = project_dir / "templates"
    template_dir.mkdir()
    (template_dir / "post.html").write_text("<h1>{{ post.title }}</h1><div>{{ post.content|safe }}</div>")
    (template_dir / "index.html").write_text("Hello Index")
    
    # Create content
    content_dir = project_dir / "content" / "posts"
    content_dir.mkdir(parents=True)
    (content_dir / "no_title_post.md").write_text("Hello World")
    
    # Create output dir
    output_dir = project_dir / "public"
    
    build_site(str(project_dir))
    
    # Verify outputs
    no_title_post_html = output_dir / "posts" / "no_title_post.html"
    assert no_title_post_html.exists()
    content = no_title_post_html.read_text()
    assert "<h1>Oraaabz</h1>" in content

def test_build_site(tmp_path):
    # Setup skeleton project
    project_dir = tmp_path
    
    # Create templates
    template_dir = project_dir / "templates"
    template_dir.mkdir()
    (template_dir / "post.html").write_text("<h1>{{ post.title }}</h1><div>{{ post.content|safe }}</div>")
    (template_dir / "index.html").write_text("Hello Index")
    
    # Create content
    content_dir = project_dir / "content" / "posts"
    content_dir.mkdir(parents=True)
    (content_dir / "first_post.md").write_text("---\ntitle: First\n---\nHello World")
    
    # Create output dir via standard python (it should be created by builder)
    output_dir = project_dir / "public"
    
    build_site(str(project_dir))
    
    # Verify outputs
    assert output_dir.exists()
    assert (output_dir / "index.html").exists()
    
    first_post_html = output_dir / "posts" / "first_post.html"
    assert first_post_html.exists()
    content = first_post_html.read_text()
    assert "<h1>First</h1>" in content
    assert "<p>Hello World</p>" in content
