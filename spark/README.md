# Radicalbit Platform Spark Jobs

This folder contains files to create the Spark docker image that will be used to calculate metrics.

The custom image is created using the `Dockerfile` and it is a base Spark image where are installed some additional dependencies and loaded with the custom jobs located in the `jobs` folder.

To create an additional job, add a `.py` file in `jobs` folder (take as an example `reference_job.py` for the boilerplate)

### Development

This is a poetry project that can be used to develop and test the jobs before putting them in the docker image.

NB: if additional python dependencies are needed, pleas add them in `Dockerfile` accordingly, and not only in the `pyproject.toml`

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

