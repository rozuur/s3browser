import csv
import io
import mimetypes
import magic
from smart_open import open
import string
from collections import namedtuple

from flask import render_template, send_file
from flask_table import Table, Col, LinkCol, DatetimeCol, create_table

from app import app
from app.utils import s3, path

app.config.from_object("config")


class S3Objects(Table):
    # To understand LinkCol https://github.com/plumdog/flask_table/blob/master/examples/simple_app.py
    path = LinkCol(
        "Path", endpoint="browse_path", url_kwargs=dict(s3path="path"), attr="path"
    )
    time = DatetimeCol("Time", datetime_format="yyyy.MM.dd HH:mm:ss")
    size = Col("Size")


@app.route("/ping")
def ping():
    return "pong"


def column_name(index):
    letters = string.ascii_uppercase
    if index == 0:
        return letters[0]

    base = len(letters)
    result = []
    while index:
        result.append(letters[index % base])
        index //= base
    return "".join(result)


def csv_table(content, delimiter):
    reader = csv.reader(io.StringIO(content.decode("utf-8")), delimiter=delimiter)

    headers = next(reader)
    TableCls = create_table("TableCls")
    column_names = [column_name(index) for index, _ in enumerate(headers)]
    app.logger.debug("Column names %s", column_names)
    for col, name in zip(column_names, headers):
        TableCls.add_column(col, Col(name))

    ItemCls = namedtuple("ItemCls", column_names)
    table = TableCls((ItemCls(*r) for r in reader), table_id="s3Table")
    return table


def render_file(filename, parents):
    mimetype = magic.from_buffer(open(filename, "rb").read(1024), mime=True)
    app.logger.info("%s mimetype is %s", filename, mimetype)
    content = s3.content(filename)
    if mimetype in ("text/csv", "text/tab-separated-values"):
        delimiter = "\t" if mimetype == "text/tab-separated-values" else ","
        table = csv_table(content, delimiter)
        return render_template("s3list.html", crumbs=parents, s3objects=table)
    return send_file(io.BytesIO(content), mimetype=mimetype)


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
        return render_file(filename, parents)
    else:
        s3objects = S3Objects(s3files, table_id="s3Table")
        return render_template("s3list.html", crumbs=parents, s3objects=s3objects)
