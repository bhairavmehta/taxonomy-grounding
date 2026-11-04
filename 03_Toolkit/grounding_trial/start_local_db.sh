#!/usr/bin/env bash
# Start a throw-away local PostgreSQL with pgvector for the trial (Linux/macOS).
# Needs PostgreSQL 14+ and the pgvector extension installed (e.g. apt install postgresql-16-pgvector, or brew install pgvector).
# On a company computer, use your approved PostgreSQL instead and pass --db to run_trial.py.
set -euo pipefail
PGBIN=${PGBIN:-$(dirname "$(command -v initdb || echo /usr/lib/postgresql/16/bin/initdb)")}
DATA=${PGDATA_DIR:-./pgdata}
[ -d "$DATA" ] || "$PGBIN/initdb" -D "$DATA" -A trust -U grounding >/dev/null
"$PGBIN/pg_ctl" -D "$DATA" -o "-p 5433 -k /tmp" -l pg.log start
sleep 2
psql -h /tmp -p 5433 -U grounding -d postgres -tc "SELECT 1 FROM pg_database WHERE datname='grounding'" | grep -q 1 || psql -h /tmp -p 5433 -U grounding -d postgres -c "CREATE DATABASE grounding"
echo "Database ready: postgresql://grounding@localhost:5433/grounding"
