from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES
from .routes import blog_bp

app = Flask(__name__)
app.config.from_object('config')

# Configure file uploads
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Configure SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

from blog.routes import *
