from collections import namedtuple


class Path(namedtuple('Path', 'href value')):
    pass


def _hierarchy(path):
    parts = path.split("/")
    last = ""
    for part in parts:
        if last:
            yield f"{last}/{part}", part
            last = f"{last}/{part}"
        else:
            yield part, part
            last = part


def hierarchy(bucket, path):
    return [Path(href=f"s3://{bucket}/{prefix}/", value=part)
            for prefix, part in _hierarchy(path)][:-1]


if __name__ == '__main__':
    hierarchies = hierarchy("bucket", "a/b/c/d/e")
    assert hierarchies[-1] == Path(href='s3://bucket/a/b/c/d/e', value='e')
