import os
import markdown
import frontmatter
from jinja2 import Environment, FileSystemLoader
import shutil

def parse_markdown(markdown_content):
    """Parses markdown content with frontmatter, returns (metadata, html)."""
    post = frontmatter.loads(markdown_content)
    # Use codehilite for syntax highlighting, and fenced_code for ``` blocks
    html_content = markdown.markdown(post.content, extensions=['fenced_code', 'codehilite'])
    return post.metadata, html_content

def render_template(template_dir, template_name, context):
    """Renders a Jinja2 template and returns the HTML string."""
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    return template.render(**context)

def build_site(project_dir):
    """Builds the static site by converting markdown to HTML and applying templates."""
    project_dir = os.path.abspath(project_dir)
    content_dir = os.path.join(project_dir, 'content', 'posts')
    pages_dir = os.path.join(project_dir, 'content', 'pages')
    template_dir = os.path.join(project_dir, 'templates')
    public_dir = os.path.join(project_dir, 'public')
    static_dir = os.path.join(project_dir, 'static')
    
    # Clean output directory
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)
        
    posts = []
    
    if os.path.exists(content_dir):
        for filename in os.listdir(content_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(content_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                meta, html = parse_markdown(content)
                meta['content'] = html
                
                # Default title if not provided
                if 'title' not in meta:
                    meta['title'] = 'Oraaabz'
                    
                # Create post specific URL / filename
                output_filename = filename.replace('.md', '.html')
                posts_output_dir = os.path.join(public_dir, 'posts')
                os.makedirs(posts_output_dir, exist_ok=True)
                
                post_html = render_template(template_dir, 'post.html', {'post': meta})
                with open(os.path.join(posts_output_dir, output_filename), 'w', encoding='utf-8') as f:
                    f.write(post_html)
                    
                # Add extra fields for the index page rendering
                meta['url'] = f'/posts/{output_filename}'
                posts.append(meta)
                
    # Sort posts by date if exists, reverse chronological
    posts.sort(key=lambda x: x.get('date', ''), reverse=True)

    # Process pages
    if os.path.exists(pages_dir):
        for filename in os.listdir(pages_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(pages_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                meta, html = parse_markdown(content)
                meta['content'] = html
                
                if 'title' not in meta:
                    meta['title'] = 'Oraaabz'
                    
                output_filename = filename.replace('.md', '.html')
                page_template = 'page.html'
                if not os.path.exists(os.path.join(template_dir, page_template)):
                    page_template = 'post.html' # fallback
                
                page_html = render_template(template_dir, page_template, {'post': meta})
                with open(os.path.join(public_dir, output_filename), 'w', encoding='utf-8') as f:
                    f.write(page_html)

    # Render index.html
    if os.path.exists(os.path.join(template_dir, 'index.html')):
        index_html = render_template(template_dir, 'index.html', {'posts': posts})
        with open(os.path.join(public_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(index_html)
            
    # Copy static assets if they exist (CSS, JS, images)
    if os.path.exists(static_dir):
        shutil.copytree(static_dir, os.path.join(public_dir, 'static'))

if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Building site in {current_dir}...")
    build_site(current_dir)
    print("Done!")
