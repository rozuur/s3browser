S3 Browser
======

Simple S3 file browser

### Docker

To build `docker build --tag s3browser .`

Create a file `aws.env` with environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

`*.env` are ignored in  `.gitignore` and `.dockerignore`

And run docker with above env file `docker run -t -i --env-file aws.env -p9000:9000 s3browser ./s3browser/start_gunicorn.sh`

**Health Check** url is `/ping`

#### Acknowledgements

Tables are displayed using [Vanilla DataTables](https://github.com/Mobius1/Vanilla-DataTables)

CSS is modified from [milligram](https://github.com/milligram/milligram.github.io)


Inspired by an internal tool of Bloomreach, which was developed by Antariksh Bothale