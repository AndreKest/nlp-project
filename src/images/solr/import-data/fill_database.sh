#!/bin/bash
set -e

echo "Wait for solr"
wait-for-solr.sh --solr-url http://localhost:8983

# Give some extra time
sleep 3

echo "Start Import Data"
post -c court-decisions /docker-entrypoint-initdb.d/data/*.xml
echo "End Import Data"

exit 0