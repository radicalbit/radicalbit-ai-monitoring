# Radicalbit Platform Spark Jobs

This folder contains files to create the Spark docker image that will be used to calculate metrics.

The custom image is created using the `Dockerfile` and it is a base Spark image where are installed additional dependencies and loaded with custom jobs located in the `jobs` folder.

### Development

This is a poetry project that can be used to develop and test the jobs before putting them in the docker image.

To create an additional job, add a `.py` file in `jobs` folder (take as an example `reference_job.py` for the boilerplate) and write unit tests

### End-to-end testing

Before publishing the image is possible to test the platform with new development or improvement done in the spark image.

From this project folder, run

```bash
docker build . -t radicalbit-spark-py:develop && docker save radicalbit-spark-py:develop -o ../docker/k3s_data/images/radicalbit-spark-py:develop.tar
```

This will build and save the new image in `/docker/k3s_data/images/`.

To use this image in the Radicalbit Platform, the docker compose must be modified adding the following environment variable in the `api` container:

```
SPARK_IMAGE: "radicalbit-spark-py:develop"
```

When the k3s cluster inside the docker compose will start, it will automatically load the saved image that can be used to test the code during the development.

NB: when a new image is built and saved, the k3s container must be restarted

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

