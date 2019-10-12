from collections import namedtuple


class Path(namedtuple('Path', 'href value')):
    pass


def _parent(path, delim):
    return path.rsplit(delim, 1)


def _crumbs(path, delim="/"):
    while path:
        try:
            new_path, base = _parent(path, delim)
            yield path, base
            path = new_path
        except ValueError:
            yield path, path
            break


def crumbs(bucket, path):
    bucket_crumb = [Path(href=f"s3://{bucket}/", value=bucket)]
    path_crumb = [Path(href=f"s3://{bucket}/{path}/", value=base)
                  for path, base in reversed(list(_crumbs(path)))][:-1]
    return bucket_crumb + path_crumb


if __name__ == '__main__':
    result = crumbs("bucket", "a/b/c/d/e")
    print(result)
    assert result[-1] == Path(href='s3://bucket/a/b/c/d/', value='d')
    assert result[1] == Path(href='s3://bucket/a/', value='a')
    assert result[0] == Path(href='s3://bucket', value='bucket')
