from . import main
from flask import render_template


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/article', methods=['GET','POST'])
def article():
    return render_template('article.html')
