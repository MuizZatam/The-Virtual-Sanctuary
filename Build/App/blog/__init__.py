from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from .routes import blog_bp

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Configure file uploads
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from blog.routes import *
