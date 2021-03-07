import bleach
from flask import render_template, flash, redirect, url_for, jsonify
from markdown import markdown

from app import app
#导入表单处理方法
from flask_login import login_required
from flask_login import current_user, login_user, logout_user
from app.models import User,BlogPost
from app import db
from flask import request
from werkzeug.urls import url_parse
from app.forms import EditProfileForm,LoginForm,RegistrationForm,PostForm
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username':'duke'}
    posts = [
        {
            'author':{'username':'刘'},
            'body':'这是模板模块中的循环例子～1'

        },
        {
            'author': {'username': '忠强'},
            'body': '这是模板模块中的循环例子～2'
        }
    ]
    return render_template('index.html',title='我的',user=user,posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    # 根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('无效的用户名或密码')

            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # 此时的next_page记录的是跳转至登录页面是的地址
        next_page = request.args.get('next')
        # 如果next_page记录的地址不存在那么就返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # 综上，登录后要么重定向至跳转前的页面，要么跳转至首页
        return redirect(next_page)
    return render_template('login.html',title='登录',form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user,'body':'测试Post #1号'},
        {'author':user,'body':'测试Post #2号'}
    ]

    return render_template('user.html',user=user,posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('你的提交已变更.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='个人资料编辑',
                           form=form)

@app.route('/blogpost')
def new_post():
    form=PostForm()
    flash("1")
    if form.validate_on_submit():
        allowed_tags = ['a', 'ul', 'strong', 'p', 'h1', 'h2', 'h3']
        html_body = markdown(form.body.data, output_format='html')
        html_body = bleach.clean(html_body, tags=allowed_tags, strip=True)
        html_body = bleach.linkify(html_body)
        blogpost = BlogPost(html_body=html_body,body=form.body)
        db.session.add(blogpost)
        db.session.commit()

    return render_template('blogpost.html', title='blog编辑',
                           form=form)
@app.route('/posts/<int:id>',methods=['GET'])
def get_post(id):
    posts=BlogPost.query.id(id)

    return 'hello'