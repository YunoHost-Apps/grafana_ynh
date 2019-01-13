#!/bin/bash
#
# Common variables
#
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
  grafana_repository_present=""
  [[ -f $GRAFANA_REPOSITORY ]] && grafana_repository_present="true"

  # Install needed apt repository for Grafana
  machine=$(uname -m)
  # Add the repos depending on processor architecture

  if [[ "$machine" =~ "armv6" ]] ; then
    # For ARM, use fg2it repository
    # https://github.com/fg2it/grafana-on-raspberry
    curl https://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -
    echo "deb http://dl.bintray.com/fg2it/deb-rpi-1b stretch main" | sudo tee $GRAFANA_REPOSITORY
  else
    # x86 processor --> we use the official repository
    curl https://packages.grafana.com/gpg.key | sudo apt-key add -
    echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee $GRAFANA_REPOSITORY
  fi

  # Install packages
  # We install them as dependencies as they may already be installed and used for other purposes
  ynh_install_app_dependencies influxdb, grafana \
  || {
    # Remove apt repositories if they were added
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

# Start or restart a service and follow its booting
#
# usage: ynh_check_starting "Line to match" [Log file] [Timeout] [Service name]
#
# | arg: Line to match - The line to find in the log to attest the service have finished to boot.
# | arg: Log file - The log file to watch; specify "systemd" to read systemd journal for specified service
#    /var/log/$app/$app.log will be used if no other log is defined.
# | arg: Timeout - The maximum time to wait before ending the watching. Defaut 300 seconds.
# | arg: Service name
ynh_check_starting () {
	local line_to_match="$1"
	local service_name="${4:-$app}"
	local app_log="${2:-/var/log/$service_name/$service_name.log}"
	local timeout=${3:-300}

	echo "Starting of $service_name" >&2
	systemctl stop $service_name
	local templog="$(mktemp)"
	# Following the starting of the app in its log
	if [ "$app_log" == "systemd" ] ; then
		# Read the systemd journal
		journalctl -u $service_name -f --since=-45 > "$templog" &
	else
		# Read the specified log file
		tail -F -n0 "$app_log" > "$templog" &
	fi
	# Get the PID of the last command
	local pid_tail=$!
	systemctl start $service_name

	local i=0
	for i in `seq 1 $timeout`
	do
		# Read the log until the sentence is found, which means the app finished starting. Or run until the timeout.
		if grep --quiet "$line_to_match" "$templog"
		then
			echo "The service $service_name has correctly started." >&2
			break
		fi
		echo -n "." >&2
		sleep 1
	done
	if [ $i -eq $timeout ]
	then
		echo "The service $service_name didn't fully start before the timeout." >&2
	fi

	echo ""
	ynh_clean_check_starting
}
# Clean temporary process and file used by ynh_check_starting
# (usually used in ynh_clean_setup scripts)
#
# usage: ynh_clean_check_starting

ynh_clean_check_starting () {
	# Stop the execution of tail.
	kill -s 15 $pid_tail 2>&1
	ynh_secure_remove "$templog" 2>&1
}
