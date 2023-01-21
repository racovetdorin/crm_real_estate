#!/bin/bash

# Script that allows to load a database on localhost
# NOTE: If you run on MacOS, make sure you have BREW and coreutils installed for realpath to work.

if [ -f "backup.sql.imported" ] ; then
  echo "A backup has been  prior loaded. To load again a new database, remove .imported."
  exit 1
fi

file=$(find . -maxdepth 2 -name "backup.sql")

if [ ! $file ] ; then
  echo "No backup has been found. Please make sure you named correctly your backup (backup.sql) and your backup is
  at the same level with the script."
  exit 1
fi

path_to_backup=$(realpath $file)

export PSQL_DB_USER=user
export PSQL_DB_NAME=impakt
export PSQL_DB_PASSWORD=password
export PSQL_DB_HOST=db


export PGPASSWORD=$PSQL_DB_PASSWORD

apt -y update
apt -y upgrade
apt-get install postgresql-client -y

dropdb $PSQL_DB_NAME -h $PSQL_DB_HOST -U $PSQL_DB_USER
createdb $PSQL_DB_NAME -h $PSQL_DB_HOST -U $PSQL_DB_USER
psql -d $PSQL_DB_NAME -h $PSQL_DB_HOST -U $PSQL_DB_USER < $path_to_backup

mv $path_to_backup "backup.sql.imported"
