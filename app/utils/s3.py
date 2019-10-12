import enum
import urllib.parse
from collections import namedtuple

import boto3 as boto3

client = boto3.client('s3')


class S3Type(enum.Enum):
    Bucket = enum.auto()
    Prefix = enum.auto()
    Key = enum.auto()


class S3Obj(namedtuple('S3Obj', ['path', 'time', 'size', 'type'])):
    @classmethod
    def from_bucket(cls, obj):
        path = obj['Name']
        path = f"s3://{path}"
        return cls(path=path, time=obj['CreationDate'], size=None, type=S3Type.Bucket)

    @classmethod
    def from_prefix(cls, obj, bucket_name):
        prefix = obj['Prefix']
        path = f"s3://{bucket_name}/{prefix}"
        return cls(path=path, time=None, size=None, type=S3Type.Prefix)

    @classmethod
    def from_content(cls, obj, bucket_name):
        key = obj['Key']
        path = f"s3://{bucket_name}/{key}"
        return cls(path=path, time=obj['LastModified'], size=obj['Size'], type=S3Type.Key)


def buckets():
    response = client.list_buckets()['Buckets']
    return [S3Obj.from_bucket(o) for o in response]


def ls(path, rows=42, delimiter='/'):
    url = urllib.parse.urlsplit(path)
    bucket_name = url.netloc
    prefix = url.path
    prefix = prefix.lstrip("/")
    response = client.list_objects_v2(
        Bucket=bucket_name,
        Delimiter=delimiter,
        MaxKeys=rows,
        Prefix=prefix
    )
    prefixes = [S3Obj.from_prefix(o, bucket_name) for o in response.get('CommonPrefixes', [])]
    keys = [S3Obj.from_content(o, bucket_name) for o in response.get('Contents', [])]
    return prefixes + keys


if __name__ == '__main__':
    for b in buckets():
        print("\n".join(str(o) for o in ls(b.path)))
