#!/bin/bash
set -e

>&2 echo "Postgres init.sh running ..."


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	CREATE USER root;
	CREATE DATABASE starter;
	GRANT ALL PRIVILEGES ON DATABASE starter TO root;
EOSQL