from __future__ import with_statement
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context

# --- Import your Base (this makes all models visible to Alembic)
from app.database import Base
from app.models import user, book, category

# --- Load config
config = context.config
fileConfig(config.config_file_name)

# --- Assign metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with a URL
    and not an Engine, though an Engine is acceptable here as well.
    By skipping the Engine creation, we don't even need a DBAPI.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Actual migration execution in online mode."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode with async engine."""
    from app.database import engine  # Import async engine

    async with engine.begin() as conn:
        await conn.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
