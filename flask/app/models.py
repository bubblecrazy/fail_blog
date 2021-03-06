from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask import url_for
# ...
from flask_login import UserMixin
from markdown import markdown
import bleach

class User(UserMixin, db.Model):
    # ...
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # back是反向引用,User和Post是一对多的关系，backref是表示在Post中新建一个属性author，关联的是Post中的user_id外键关联的User对象。
    #lazy属性常用的值的含义，select就是访问到属性的时候，就会全部加载该属性的数据;joined则是在对关联的两个表进行join操作，从而获取到所有相关的对象;dynamic则不一样，在访问属性的时候，并没有在内存中加载数据，而是返回一个query对象, 需要执行相应方法才可以获取对象，比如.all()
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    def __repr__(self):
        return '<用户名:{}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db .Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class BlogPost(db.Model):
    __tablename__ = 'blogposts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    html_body = db.Column(db.Text)

    def to_json(self):
        json_post = {
            'url': url_for('app.get_post', id=self.id, _external=True),
            'body': self.body,
            'html_body': self.html_body
        }
        return json_post

    @staticmethod

    def from_json(json_post):
        body = json_post.get('body')
        return BlogPost(body=body)