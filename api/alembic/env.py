from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.core import get_config

from app.db.tables.model_table import *
from app.db.tables.reference_dataset_table import *
from app.db.tables.reference_dataset_metrics_table import *
from app.db.tables.current_dataset_table import *
from app.db.tables.current_dataset_metrics_table import *
from app.db.tables.completion_dataset_table import *
from app.db.tables.completion_dataset_metrics_table import *
from app.db.tables.project_table import *
from app.db.tables.commons.json_encoded_dict import JSONEncodedDict
from app.db.database import Database, BaseTable

database = Database(conf=get_config().db_config)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option("sqlalchemy.url", database.db_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = BaseTable.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name in [target_metadata.schema]
    else:
        return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_item=render_item,
        version_table_schema=target_metadata.schema,
        include_schemas=True,
        include_name=include_name
    )

    # Here we need to enforce public if schema target_metadata.schema is None, which is default schema (public for postgres) for alembic
    target_schema = 'public' if target_metadata.schema is None else target_metadata.schema

    with context.begin_transaction():
        context.execute(f'create schema if not exists "{target_schema}";')
        context.execute(f'set search_path to "{target_schema}"')
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
            version_table_schema=target_metadata.schema,
            include_schemas=True,
            include_name=include_name
        )

        # Here we need to enforce public if schema target_metadata.schema is None, which is default schema (public for postgres) for alembic
        target_schema = 'public' if target_metadata.schema is None else target_metadata.schema

        with context.begin_transaction():
            context.execute(f'create schema if not exists "{target_schema}";')
            context.execute(f'set search_path to "{target_schema}"')
            context.run_migrations()


def render_item(type_, obj, autogen_context):
    if type_ == "type" and isinstance(obj, JSONEncodedDict):
        autogen_context.imports.add(
            "from app.db.tables.commons.json_encoded_dict import JSONEncodedDict"
        )
        return "%r" % obj

    return False


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
