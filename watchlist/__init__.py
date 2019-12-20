# -*- coding: utf-8 -*-
# @Time : 2019-12-16 15:48
# @Author : dml19
# @File : __init__.py
# @Software: PyCharm
import os
import sys

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
	prefix = 'sqlite:///'
else:
	prefix = "sqlite:////"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),
                                                              os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

# 在扩展类实例化前加载配置
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app
login_manager = LoginManager(app)  # 实例化扩展类


@login_manager.user_loader
def load_user(user_id):
	from watchlist.models import User
	user = User.query.get(int(user_id))
	return user


login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'


# 模板上下文处理函数
@app.context_processor
def inject_user():  # 函数名可以随意修改
	from watchlist.models import User
	user = User.query.first()
	return dict(user=user)  # 需要返回字典，等同于 return {‘user’：user }
