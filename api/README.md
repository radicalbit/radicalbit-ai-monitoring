# Radicalbit Platform REST API

## How to set up ##

The project is based on poetry for managing dependencies.

You should have poetry installed on your local machine. You can follow the instruction on https://python-poetry.org.

After you have poetry installed you can install the project's dependencies run:

```bash
poetry install
```

## Format

This project uses `ruff` for formatting and linting.

Run

```bash
poetry run ruff format
```

to format, and 

```bash
poetry run ruff check
```

to check.


## Test

Please install a PostgreSQL database locally. For example, on a macOS platform, execute:

```bash
brew install postgresql
```

Note: If any errors occur during pytest runs, please stop the local database service by executing:

```bash
brew services stop postgresql
```

Tests are done with `pytest`

Run

```bash
poetry run pytest -v
```

## OpenAPI

The OpenAPI specs are available under `http://localhost:9000/docs`

## Migrations

We use [alembic](https://pypi.org/project/alembic/) as engine to manage database migrations.

Database migrations are automatically managed by alembic in docker-compose file. It will connect to the database and apply the migrations defined in [alembic](./alembic/versions/) folder.

### Generate a new migration

We use [sqlalchemy](https://docs.sqlalchemy.org/en/20/) to define the database tables. All table clas are stored in [./app/db/tables/](./app/db/tables/) folder.


If you have updated a class inside the above folder, you can use the docker-compose file to generate the new migration file by using alembic command:

```bash
docker compose run migrations /bin/sh -c "alembic revision --autogenerate -m "GIVE A NAME TO THIS REVISION""
```

this will ooutput a new migration file that is going to be used by `migrations` Docker image.

### Generate migration for a new Table

If you need to create a new table in the database, you have to create a new python class in the [./app/db/tables/](./app/db/tables/) and you need to run the same command described above:

```bash
docker compose run migrations /bin/sh -c "alembic revision --autogenerate -m "GIVE A NAME TO THIS REVISION""
```

***Notes***: Alembic watches for all BaseTables classes imported in the [env.py](./alembic/env.py) file. If you add a new file for the table, be sure to import the class in the env.py file.

