# Contribute to this project

🎉 Thank you for considering contributing to **Radicalbit AI Monitoring** 🎉!

We welcome contributions from developers like you. To ensure a smooth contribution process, please follow the guidelines below.

## Commit messages conventions
This project follows the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

Steps to follow:

1. Install [pre-commit](https://pre-commit.com/) because we'll use it as our main linter. It's completely plugin-based, you con follow [these instructions](https://pre-commit.com/#installation) to install it onto your machine.

2. Install and configure the [conventional-pre-commit](https://github.com/compilerla/conventional-pre-commit) plugin that allows to use the linter to enforce the usage of conventional commits.   
This repo is already provided with a proper configuration of the plugin, see setup instructions [here](https://github.com/compilerla/conventional-pre-commit?tab=readme-ov-file#usage)

## Development Environment Setup

In this section we will show how to set up the development environment for the project.

For more info about the development of the ui and api, see [ui](./ui/README.md) and [api](./api/README.md) README.md files.

### Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

We use [docker compose watch](https://docs.docker.com/compose/file-watch/) as our development environment, so be sure docker compose `2.22.0` or greater is installed.

### Start the Environment

Run `docker compose --profile ui up --watch` to run the app in DEV mode.

By running the above command the following containers are started:

1. **ui**: nginx container with the ui built using yarn (see [Dockerfile](./ui/Dockerfile))
1. **api**: FastAPI application server (see [Dockerfile](./api/Dockerfile))
1. **migrations**: alembic container to manage database migrations (see [Dockerfile](./api/migrations.Dockerfile)). For more info on how to create new migrations please refer to [api README.md file](./api/README.md#generate-a-new-migration)
1. **k3s**: K3s cluster where spark jobs are executed
1. **postgres**: PostgreSQL Database
1. **minio**: s3 compatible object storage
1. **adminer**: to interact with the database if needed
1. **createbucket**: container to create the default bucket in minio

Once all the containers are up & running you can make any changes to the api and/or the ui folders and docker compose will restart all the modified containers.

## Code Style

We use [Ruff](https://docs.astral.sh/ruff/) as our main python linter and formatter, and [ESLint](https://eslint.org/) for *Javascript* code.

## Issues and Bugs

If you find any issues or bugs, please open a GitHub issue with a detailed description of the problem and steps to reproduce it.

## Pull Requests

1. Fork the repository and create a new branch for your feature or bug fix
1. Make your changes and ensure all tests pass
1. Open a pull request with a clear title and description
1. Be ready to address any feedback or comments during the code review process

*Notes on Pull Requests:*

- We [check](./.github/workflows/semantic-pr.yaml) that all pull request titles follow the conventional commit format.
- All docker image build on pull request events are disabled by default. You can run the build if needed by commenting on the pull request with a command (available commands are: `/build-api`, `/build-spark`, `/build-ui`, `/build-migrations`, `/build-all`).
