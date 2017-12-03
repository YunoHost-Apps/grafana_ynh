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
# Install needed repositories and install dependencies
# usage: install_dependencies
install_dependencies() {
  # Install needed dependency for HTTPS apt access
  # (that dependency could be handled upstream in YunoHost)
  ynh_package_install apt-transport-https

  # Test repositories existence, in case of failed installation
  influxdb_repository_present=""
  grafana_repository_present=""
  [[ -f $INFLUXDB_REPOSITORY ]] && influxdb_repository_present="true"
  [[ -f $GRAFANA_REPOSITORY ]] && grafana_repository_present="true"

  # Install needed apt repository for InfluxDB
  curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
  source /etc/os-release
  test $VERSION_ID = "8" && echo "deb https://repos.influxdata.com/debian jessie stable" | sudo tee $INFLUXDB_REPOSITORY

  # Install needed apt repository for Grafana
  machine=$(uname -m)
  # Add the repos depending on processor architecture
   if [[ "$machine" =~ "x86" ]]; then 
    # x86 processor --> we use the official repository
    curl -s https://packagecloud.io/install/repositories/grafana/stable/script.deb.sh | sudo bash
  elif [[ "$machine" =~ "armv6" ]] ; then
    # For ARM, use fg2it repository
    # https://github.com/fg2it/grafana-on-raspberry
    curl https://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -
    echo "deb http://dl.bintray.com/fg2it/deb-rpi-1b jessie main" | sudo tee $GRAFANA_REPOSITORY
  elif [[ "$machine" =~ "armv7" ]] ; then
    curl https://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -
    echo "deb http://dl.bintray.com/fg2it/deb jessie main" | sudo tee $GRAFANA_REPOSITORY
  fi

  # Install packages
  # We install them as dependencies as they may already be installed and used for other purposes
  ynh_install_app_dependencies influxdb, grafana \
  || {
    # Remove apt repositories if they were added
    [[ -n "$influxdb_repository_present" ]] && sudo rm $INFLUXDB_REPOSITORY
    [[ -n "$grafana_repository_present" ]] && sudo rm $GRAFANA_REPOSITORY
    ynh_die "Unable to install Debian packages"
  }
}

# ======== Future YunoHost helpers ========

# Delete a file checksum from the app settings
#
# $app should be defined when calling this helper
#
# usage: ynh_remove_file_checksum file
# | arg: file - The file for which the checksum will be deleted
ynh_delete_file_checksum () {
	local checksum_setting_name=checksum_${1//[\/ ]/_}	# Replace all '/' and ' ' by '_'
	ynh_app_setting_delete $app $checksum_setting_name
}
