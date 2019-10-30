import enum
import urllib.parse
from collections import namedtuple

import boto3
from werkzeug.exceptions import abort

S3_SCHEME_TYPES = frozenset(["s3", "s3n"])
S3_CLIENT = boto3.client("s3")
MAX_FILE_SIZE = 1024 * 1024 * 1024


class S3Type(enum.Enum):
    Bucket = enum.auto()
    Prefix = enum.auto()
    Key = enum.auto()


class S3Obj(namedtuple("S3Obj", ["path", "time", "size", "type"])):
    @classmethod
    def from_bucket(cls, obj):
        path = obj["Name"]
        path = f"s3://{path}"
        return cls(path=path, time=obj["CreationDate"], size=None, type=S3Type.Bucket)

    @classmethod
    def from_prefix(cls, obj, bucket_name):
        prefix = obj["Prefix"]
        path = f"s3://{bucket_name}/{prefix}"
        return cls(path=path, time=None, size=None, type=S3Type.Prefix)

    @classmethod
    def from_content(cls, obj, bucket_name):
        key = obj["Key"]
        path = f"s3://{bucket_name}/{key}"
        return cls(
            path=path, time=obj["LastModified"], size=obj["Size"], type=S3Type.Key
        )


def split(path):
    url = urllib.parse.urlsplit(path)
    if url.scheme not in S3_SCHEME_TYPES:
        abort(400, f"Invalid scheme in {path}")
    bucket_name = url.netloc
    prefix = url.path
    prefix = prefix.lstrip("/")
    return url.scheme, bucket_name, prefix


def buckets():
    response = S3_CLIENT.list_buckets()["Buckets"]
    return [S3Obj.from_bucket(o) for o in response]


def ls(path, rows=1000, delimiter="/"):
    _, bucket_name, prefix = split(path)
    response = S3_CLIENT.list_objects_v2(
        Bucket=bucket_name, Delimiter=delimiter, MaxKeys=rows, Prefix=prefix
    )
    prefixes = [
        S3Obj.from_prefix(o, bucket_name) for o in response.get("CommonPrefixes", [])
    ]
    keys = [S3Obj.from_content(o, bucket_name) for o in response.get("Contents", [])]
    return prefixes + keys


def content(path):
    _, bucket_name, prefix = split(path)
    object = S3_CLIENT.get_object(Bucket=bucket_name, Key=prefix)
    if object["ContentLength"] > MAX_FILE_SIZE:
        abort(400, "Max file size exceeded")
    if object["ResponseMetadata"]["HTTPStatusCode"] != 200:
        abort(object["ResponseMetadata"]["HTTPStatusCode"])
    return object["Body"].read()


if __name__ == "__main__":
    for b in buckets():
        print("\n".join(str(o) for o in ls(b.path)))
