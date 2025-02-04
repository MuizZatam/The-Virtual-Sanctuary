from flask import Blueprint, render_template, redirect, url_for, flash
from blog import app, db, photos
from .models import BlogPost
from .forms import BlogPostForm
from datetime import datetime


blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

@blog_bp.route('/')
def index():
    posts = BlogPost.query.all()
    return render_template('blog/index.html', posts=posts)


@blog_bp.route('/post/create', methods=['GET', 'POST'])
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        image = form.image.data
        if image:
            filename = photos.save(image)
            post = BlogPost(
                title=form.title.data,
                content=form.content.data,
                image=filename,
                created_at=datetime.now()
            )
        else:
            post = BlogPost(
                title=form.title.data,
                content=form.content.data,
                created_at=datetime.now()
            )
        db.session.add(post)
        db.session.commit()
        flash('Blog post created successfully.', 'success')
        return redirect(url_for('blog.index'))
    return render_template('blog/create_post.html', form=form)
