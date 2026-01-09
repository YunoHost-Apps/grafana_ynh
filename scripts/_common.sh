#!/bin/bash

#=================================================
# COMMON VARIABLES AND CUSTOM HELPERS
#=================================================

log_file="/var/log/$app/${app%_*}.log"

# Set permissions
myynh_set_permissions () {
	chown -R "$app": "$install_dir"
	chmod -R u=rwx,g=rwx,o= "$install_dir"

	mkdir -p "$data_dir/plugins"
	chown -R "$app": "$data_dir"
	chmod -R u=rwx,g=rwx,o= "$data_dir"

	mkdir -p "/var/log/$app"
	chown -R "$app": "/var/log/$app"
	chmod u=rwx,g=rx,o=rw "/var/log/$app"
}
