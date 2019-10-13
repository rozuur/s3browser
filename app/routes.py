import io
import mimetypes

from flask import render_template, send_file
from flask_table import Table, Col, LinkCol, DatetimeCol

from app import app
from app.utils import s3, path

app.config.from_object("config")


class S3Objects(Table):
    # To understand LinkCol https://github.com/plumdog/flask_table/blob/master/examples/simple_app.py
    path = LinkCol(
        "Path", endpoint="browse_path", url_kwargs=dict(s3path="path"), attr="path"
    )
    time = DatetimeCol("Time")
    size = Col("Size")


@app.route("/ping")
def ping():
    return "pong"


@app.route("/", defaults={"s3path": ""})
@app.route("/path/", defaults={"s3path": ""})
@app.route("/path/<path:s3path>")
def browse_path(s3path):
    if s3path:
        s3files = s3.ls(s3path)
        _, bucket, prefix = s3.split(s3path)
        parents = path.crumbs(bucket, prefix)
        app.logger.debug("parents of %s is %s", s3path, parents)
    else:
        s3files = s3.buckets()
        parents = []
    if len(s3files) == 1 and s3files[0].path == s3path and not s3path.endswith("/"):
        filename = s3files[0].path
        mimetype = mimetypes.MimeTypes().guess_type(filename)[0]
        app.logger.info("%s mimetype is %s", filename, mimetype)
        content = s3.content(filename)
        return send_file(io.BytesIO(content), mimetype=mimetype)
    else:
        s3objects = S3Objects(s3files, table_id="s3Table")
        return render_template("s3list.html", crumbs=parents, s3objects=s3objects)
