#!/bin/sh -e

# https://discuss.circleci.com/t/redis-server-problems-unable-to-connect-localhost-6379/4040/3

until bash -c "sudo service redis-server status"; do
  >&2 echo "Redis not running, trying to kick start it"
  bash -c "sudo service redis-server start"
  sleep 1
done