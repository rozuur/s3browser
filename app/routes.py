from flask import render_template
from flask_table import Table, Col, LinkCol

from app import app
from app.utils import s3, path


class S3Objects(Table):
    # To understand LinkCol https://github.com/plumdog/flask_table/blob/master/examples/simple_app.py
    path = LinkCol('Path', endpoint='browse_path', url_kwargs=dict(s3path='path'), attr='path')
    time = Col('Time')
    size = Col('Size')
    type = Col('Type')


@app.route('/', defaults={'s3path': ''})
@app.route('/path/', defaults={'s3path': ''})
@app.route('/path/<path:s3path>')
def browse_path(s3path):
    env = {
        'endpoint': 'local.s3browser.com'
    }
    s3files = s3.ls(s3path) if s3path else s3.buckets()
    _, bucket, prefix = s3.split(s3path)
    hierarchy = path.hierarchy(bucket, prefix)
    print(hierarchy, prefix)
    return render_template('index.html', env=env, hierarchy=hierarchy, s3objects=S3Objects(s3files))
