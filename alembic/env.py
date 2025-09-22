from logging.config import fileConfig
import sys
import pathlib

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- Make the app importable (project root on sys.path) ---
BASE_DIR = pathlib.Path(__file__).resolve().parents[1]  # project root
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# --- Import app settings & metadata AFTER sys.path is set ---
from app.core.config import settings
from app.db.base import Base
from app.db import models  # noqa: F401  # ensure models are imported for autogenerate

# --- Alembic config object ---
config = context.config

# Use the same DB URL as your app (from .env via pydantic-settings)
config.set_main_option("sqlalchemy.url", settings.database_url)

# Configure logging from alembic.ini (if present)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The metadata Alembic should autogenerate from
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # <— helpful for enums/length changes
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # <— helpful here too
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
