# -*- coding: utf-8 -*-
# @Time : 2019-12-19 9:55
# @Author : dml19
# @File : views.py
# @Software: PyCharm 
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from watchlist import app, db
from watchlist.models import Movie, User


# 返回渲染好的模板作为响应
@app.route('/', methods=['GET', 'POST'])
def index():
	# 创建电影条目
	if request.method == "POST":  # 判断是否是 POST 请求
		if not current_user.is_authenticated:  # 如果当前用户未认证
			return redirect(url_for('index'))  # 重定向到主页
		
		# 获取表单数据
		title = request.form.get('title')  # 传入表单对应字段的 name 值
		year = request.form.get('year')
		# 验证数据
		if not title or not year or len(year) > 4 or len(title) > 60:
			flash('Invalid input.')  # 显示错误提示
			return redirect(url_for('index'))  # 重定向回主页
		# 保存表单数据回数据库
		movie = Movie(title=title, year=year)  # 创建记录
		db.session.add(movie)  # 添加到数据库会话
		db.session.commit()  # 提交数据库会话
		flash('Item create.')  # 显示成功创建的提示
		return redirect(url_for('index'))  # 重定向回主页
	
	movies = Movie.query.all()
	return render_template('index.html', movies=movies)


# 编辑电影条目
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
	movie = Movie.query.get_or_404(movie_id)
	
	if request.method == 'POST':  # 处理编辑表单的提交请求
		title = request.form['title']
		year = request.form['year']
		
		if not title or not year or len(year) > 4 or len(title) > 60:
			flash('Invalid input.')
			return redirect(url_for('edit', movie_id=movie_id))  # 重定向回应的编辑页面
		
		movie.title = title  # 更新标题
		movie.year = year  # 更新年份
		db.session.commit()  # 提交数据会话
		flash('Item updated.')
		return redirect(url_for('index'))  # 重定向回主页
	
	return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


# 删除电影条目
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete(movie_id):
	movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
	db.session.delete(movie)  # 删除对应的记录
	db.session.commit()  # 提交数据库会话
	flash('Item deleted.')
	return redirect(url_for('index'))  # 重定向回主页


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
	if request.method == 'POST':
		name = request.form['name']
		
		if not name or len(name) > 20:
			flash('Invalid input.')
			return redirect(url_for('settings'))
		
		current_user.name = name
		# current_user 会返回当前登录用户的数据库记录对象
		# 等同于下面的用法
		# user = User.query.first()
		# user.name = name
		db.session.commit()
		flash('Settings updated.')
		return redirect(url_for('index'))
	
	return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.methods == 'POST':
		username = request.form['username']
		password = request.form['password']
		
		if not username or not password:
			flash('Invalid input.')
			return redirect(url_for('login'))
		
		user = User.query.first()
		
		if username == user.username and user.validate_password(password):
			login_user(user)
			flash('Login success.')
			return redirect(url_for('index'))
		
		flash('Invalid username or password.')
		return redirect(url_for('login'))
	
	return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Goodbye.')
	return redirect(url_for('index'))
