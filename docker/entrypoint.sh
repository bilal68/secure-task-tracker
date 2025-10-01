#!/usr/bin/env sh
set -e

# Normalize postgres scheme if provider gives postgres://
if [ -n "$DATABASE_URL" ] && echo "$DATABASE_URL" | grep -q "^postgres://"; then
  export DATABASE_URL="$(echo "$DATABASE_URL" | sed 's#^postgres://#postgresql://#')"
fi

# Optional: ensure short DB connect timeout to fail fast if misconfigured
if [ -n "$DATABASE_URL" ] && echo "$DATABASE_URL" | grep -vq "connect_timeout="; then
  sep=$(echo "$DATABASE_URL" | grep -q '?' && echo '&' || echo '?')
  export DATABASE_URL="${DATABASE_URL}${sep}connect_timeout=5"
fi

# Run migrations
alembic ${ALEMBIC_CONFIG:+-c "$ALEMBIC_CONFIG"} upgrade head

# Run seed only when asked (set RUN_SEED=true in Railway → Variables, then remove it)
if [ "${RUN_SEED}" = "1" ] || [ "${RUN_SEED}" = "true" ]; then
  echo "RUN_SEED is set → running seed script..."
  python app/scripts/seed.py --create-admin --admin-email=admin@yourdomain.com --admin-password=yourpassword --users=5 --tasks-per-user=10
  echo "Seed complete."
fi
# Start API on the platform port
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers ${UVICORN_WORKERS:-4}
