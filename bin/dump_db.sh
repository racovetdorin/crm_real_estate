#!/bin/bash

date=$(date '+%Y-%m-%d')

filename=remaxmd_$date.sql

echo Commensing db dump in file $filename

pg_dump remaxmd > /tmp/$filename
pg_dump remaxmd > $filename

echo Sending db dump to S3 bucket

aws s3 --endpoint=https://fra1.digitaloceanspaces.com cp /tmp/$filename s3://media-remaxmd/db_dump/$filename

echo Deleting /tmp/$filename

rm /tmp/$filename
