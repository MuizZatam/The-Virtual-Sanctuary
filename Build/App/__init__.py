from flask import Flask
from .blog.routes import blog_bp

app = Flask(__name__)

app.register_blueprint(blog_bp, url_prefix='/blog')

# Other app setup and configuration
