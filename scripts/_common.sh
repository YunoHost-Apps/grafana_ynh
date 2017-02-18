#!/bin/bash
#
# Common variables
#
INFLUXDB_REPOSITORY="/etc/apt/sources.list.d/influxdb.list"
GRAFANA_REPOSITORY="/etc/apt/sources.list.d/grafana_stable.list"

#
# Common helpers
#

# Fix path if needed
# usage: fix_patch PATH_TO_FIX
fix_path() {
  local path=$1
  if [ "${path:0:1}" != "/" ] && [ ${#path} -gt 0 ]; then
         path="/$path"
  fi
  if [ "${path:${#path}-1}" == "/" ] && [ ${#path} -gt 1 ]; then
         path="${path:0:${#path}-1}"
  fi
  echo "$path"
}