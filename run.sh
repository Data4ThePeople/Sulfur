#!/bin/sh
# Rebuild everything. ./run.sh --fetch pulls fresh data first.
set -e
cd "$(dirname "$0")/scripts"
PY=../.venv/bin/python
if [ "$1" = "--fetch" ]; then
  for s in eia fred usda worldbank usgs census statcan; do $PY fetch_$s.py; done
fi
$PY process.py > /dev/null
$PY charts.py > /dev/null
$PY build.py
$PY tieout.py
