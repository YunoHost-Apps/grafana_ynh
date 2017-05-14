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
  ynh_app_dependencies influxdb, grafana \
  || {
    # Remove apt repositories if they were added
    [[ -n "$influxdb_repository_present" ]] && sudo rm $INFLUXDB_REPOSITORY
    [[ -n "$grafana_repository_present" ]] && sudo rm $GRAFANA_REPOSITORY
    ynh_die "Unable to install Debian packages"
  }
}


# ======== Future YunoHost helpers ========
# Install dependencies with a equivs control file
#
# usage: ynh_app_dependencies dep [dep [...]]
# | arg: dep - the package name to install in dependence
ynh_app_dependencies () {
    dependencies=$@
    manifest_path="../manifest.json"
    if [ ! -e "$manifest_path" ]; then
    	manifest_path="../settings/manifest.json"	# Into the restore script, the manifest is not at the same place
    fi
    version=$(sudo python3 -c "import sys, json;print(json.load(open(\"$manifest_path\"))['version'])")	# Retrieve the version number in the manifest file.
    dep_app=${app//_/-}	# Replace all '_' by '-'
    cat > ./${dep_app}-ynh-deps.control << EOF	# Make a control file for equivs-build
Section: misc
Priority: optional
Package: ${dep_app}-ynh-deps
Version: ${version}
Depends: ${dependencies// /, }
Architecture: all
Description: Fake package for ${app} (YunoHost app) dependencies
 This meta-package is only responsible of installing its dependencies.
EOF
    ynh_package_install_from_equivs ./${dep_app}-ynh-deps.control \
        || ynh_die "Unable to install dependencies"	# Install the fake package and its dependencies
}

# Remove fake package and its dependencies
#
# Dependencies will removed only if no other package need them.
#
# usage: ynh_remove_app_dependencies
ynh_remove_app_dependencies () {
    dep_app=${app//_/-}	# Replace all '_' by '-'
    ynh_package_autoremove ${dep_app}-ynh-deps	# Remove the fake package and its dependencies if they not still used.
}

# Find a free port and return it
#
# example: port=$(ynh_find_port 8080)
#
# usage: ynh_find_port begin_port
# | arg: begin_port - port to start to search
ynh_find_port () {
	port=$1
	test -n "$port" || ynh_die "The argument of ynh_find_port must be a valid port."
	while netcat -z 127.0.0.1 $port       # Check if the port is free
	do
		port=$((port+1))	# Else, pass to next port
	done
	echo $port
}
