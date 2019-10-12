from flask import render_template

from app import app


@app.route('/')
def index():
    env = {
        'endpoint': 'local.s3browser.com'
    }
    return render_template('index.html', env=env)
