#!/usr/bin/env sh
set -e

# Normalize postgres scheme if provider gives postgres://
if [ -n "$DATABASE_URL" ] && echo "$DATABASE_URL" | grep -q "^postgres://"; then
  export DATABASE_URL="$(echo "$DATABASE_URL" | sed 's#^postgres://#postgresql://#')"
fi

# If alembic.ini isn’t at repo root, set ALEMBIC_CONFIG=app/alembic.ini in Railway Variables
alembic ${ALEMBIC_CONFIG:+-c "$ALEMBIC_CONFIG"} upgrade head

# Start API on the platform port
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers ${UVICORN_WORKERS:-4}
