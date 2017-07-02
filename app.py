# imports
import ipdb
from flask import Flask, render_template, redirect, url_for, flash, request
from datetime import date
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand


# instances
app = Flask(__name__)

# config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'x17F\x85Z\xb2G\x8e\xa5\xdb\xdf\xe02\xf4&n\x8a:\xc7_\xe1xbu'

# instances

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# models


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    date_pub = db.Column(db.Date)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content, date_pub=None):
        self.title = title
        if self.date_pub is None:
            self.date_pub = date.today()
        self.content = content

    def __repr__(self):
        return '<Title {}>'.format(self.title)


@app.route('/')
@app.route('/index')
def index():
    post = db.Post.query.all()
    return render_template('index.html', post=post)


@app.route('/add', methods=['POST', 'GET'])
def add():
    error = None
    if request.method == 'POST':
        post = Post(request.form['title'], request.form['content'])
        db.session.add(post)
        db.session.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login')
def login():
   """ ```
    error = None
    if request.method == 'POST':
        if request.form['']
    return render_template('login.html')

"""

if __name__ == '__main__':
    manager.run()
