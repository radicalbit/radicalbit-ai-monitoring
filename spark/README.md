# Radicalbit Platform Spark Jobs

This folder contains files to create the Spark docker image that will be used to calculate metrics.

The custom image is created using the `Dockerfile` and it is a base Spark image where are installed additional dependencies and loaded with custom jobs located in the `jobs` folder.

### Development

This is a poetry project that can be used to develop and test the jobs before putting them in the docker image.

To create an additional job, add a `.py` file in `jobs` folder (take as an example `reference_job.py` for the boilerplate) and write unit tests

#### Formatting and linting

```bash
poetry run ruff format
```

```bash
poetry run ruff check --fix
```

### Testing

```bash
poetry run pytest
```

