#!/bin/bash

MONGO_URI_SOURCE=$1
MONGO_URI_TARGET=$2
DB_NAME_SOURCE="${MONGO_URI_SOURCE##*/}"
DB_NAME_TARGET="${MONGO_URI_TARGET##*/}"

ls .
echo "Davide"
#python ./anonymize.py MONGO_URI_TARGET