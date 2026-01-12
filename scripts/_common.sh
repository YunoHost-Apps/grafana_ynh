#!/bin/bash

#=================================================
# COMMON VARIABLES AND CUSTOM HELPERS
#=================================================

# Set permissions
myynh_set_permissions () {
	chown -R "$app:$app" "$install_dir"
	chmod -R u=rwx,g=rx,o= "$install_dir"

	chown -R "$app:$app" "$data_dir"
	chmod -R u=rwx,g=rx,o= "$data_dir"

	chown -R "$app:$app" "/var/log/$app"
	chmod u=rwx,g=rx,o= "/var/log/$app"
}
