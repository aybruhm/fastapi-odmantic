# FastAPI-Odmantic

FastAPI production-ready template using Odmantic (MongoDB).

## Docker

You can start the project with docker using this command:

```bash
make run_dev
```

This command exposes the web application on port `2555`, mounts current directory and enables autoreload.

To view the database admin, navigate to: `0.0.0.0:5001`. The name of the database is going to be whatever you have replace `<project_name>` with.

But you have to rebuild image every time you modify `Pipfile.lock` or `Pipfile` with this command:

```bash
make build_dev
make up_dev
```

## Configuration

This application can be configured with environment variables.

Create an `.env` file from the `.env.template` file in the root directory and place all environment variables.
