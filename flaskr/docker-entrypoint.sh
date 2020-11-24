#!/bin/sh
set -e
if [ "$1" = "uwsgi" ]; then
  exec uwsgi --ini flaskr/flaskr.ini
fi
exec "$@"
