# Radicalbit Platform Python SDK

Python SDK to work with Radicalbit Platform.

### How to set up ###

The project is based on poetry for managing dependencies.

You should have poetry installed on your local machine. You can follow the instruction on https://python-poetry.org.

After you have poetry installed you can install the project's dependencies run:

```bash
poetry install
```

To run code formatter use:

```bash
poetry run ruff format
```

### AWS authentication ###

There are multiple ways to authenticate to AWS S3 API.
The order in witch the client searches for credentials is:

1. passing [`AwsCredentials`](./radicalbit_platform_sdk/models/aws_credentials.py) to functions
2. using [environment variables](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-envvars.html#envvars-set)
3. using shared credentials file `~/.aws/credentials`
4. using AWS config file `~/.aws/config`

### How to run tests ###

To run the tests execute:

```bash
# Run unit tests
poetry run pytest -v

# Run code format validation
poetry run ruff check
```