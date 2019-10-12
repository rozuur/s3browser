Just use [pip-tools](https://github.com/jazzband/pip-tools)

Add a new dependency to `requirements.in` and run `pip-compile requirements.in` to generate `requrirements.txt`

All the dev requirements are present in `dev-requirements.in`

And to install packages use `pip`