import io
import mimetypes

from flask import render_template, send_file
from flask_table import Table, Col, LinkCol

from app import app
from app.utils import s3, path

app.config.from_object('config')


class S3Objects(Table):
    # To understand LinkCol https://github.com/plumdog/flask_table/blob/master/examples/simple_app.py
    path = LinkCol('Path', endpoint='browse_path', url_kwargs=dict(s3path='path'), attr='path')
    time = Col('Time')
    size = Col('Size')


@app.route('/ping')
def ping():
    return 'pong'


@app.route('/', defaults={'s3path': ''})
@app.route('/path/', defaults={'s3path': ''})
@app.route('/path/<path:s3path>')
def browse_path(s3path):
    if s3path:
        s3files = s3.ls(s3path)
        _, bucket, prefix = s3.split(s3path)
        parents = path.crumbs(bucket, prefix)
    else:
        s3files = s3.buckets()
        parents = []
    if len(s3files) == 1 and s3files[0].path == s3path:
        filename = s3files[0].path
        content = s3.content(filename)
        mimetype = mimetypes.MimeTypes().guess_type(filename)[0]
        return send_file(io.BytesIO(content), mimetype=mimetype)
    else:
        s3objects = S3Objects(s3files, table_id="s3Table")
        return render_template('s3list.html', crumbs=parents, s3objects=s3objects)
