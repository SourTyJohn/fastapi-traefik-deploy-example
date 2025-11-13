#!/bin/bash
set -e

# split string by "," symbol
IFS=","


function create_db() {
    psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" postgres \
        -c "CREATE DATABASE $1 OWNER $POSTGRES_USER;"

    echo "Created database: $1"
}

# create databases by names from DATABASES env variables
for db_name in ${DATABASES}; do
    create_db $db_name
done


unset IFS
