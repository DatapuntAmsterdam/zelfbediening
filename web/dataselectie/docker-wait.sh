#!/usr/bin/env bash

set -u
set -e

# wait for elastic
while ! nc -z elasticsearch 9200
do
	echo "Waiting for elastic..."
	sleep 2
done

# wait for postgres BAG
while ! nc -z database_BAG 5432
do
	echo "Waiting for postgres..."
	sleep 2
done

# wait for postgres dataselectie
while ! nc -z database_dataselectie 5432
do
	echo "Waiting for postgres..."
	sleep 2
done
