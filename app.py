from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['POST', 'GET'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        # read the database?
        blogPosts = db.session.query(BlogPost).all()
        db.session.commit()
        return render_template('posts.html', posts=blogPosts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    raise NotImplemented


@app.route('/posts/new', methods=['GET'])
def new_post():
    post_title = request.args.get('title', '')
    post_content = request.args.get('content', '')
    author = request.args.get('author', '')
    if (post_content == '' and post_content == '' and author == ''):
        return render_template('new_post.html')
    else:
        new_post = BlogPost(title=post_title, content=post_content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return "You did it!"
    


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
