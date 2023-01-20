from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
import os
from scrapy_testes import execute_sql
from valid_auth import valid_login
from autenti_oficial import login_required
from usuários import User
app = Flask(__name__,template_folder='template')
app.secret_key = 'the random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@local_host:5432/postgres'
db = SQLAlchemy(app)
