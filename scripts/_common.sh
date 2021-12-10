#!/bin/bash

#=================================================
# COMMON VARIABLES
#=================================================

# Debian package version for Grafana
GRAFANAVERSION="8.0.7"

# dependencies used by the app
pkg_dependencies="influxdb"

ARCHITECTURE=$(dpkg --print-architecture)

#arm64
sha256_arm64=ebfa946af9e5414a9dd9cfc83cb6973fbfb366b81790f19d9dd0fd563142282d

#armv6
sha256_armhf_v6=78ae6990b3d4787f825278300c5779bcc1c89e5cb8ccbf6d7040aab421bb9948

#armv7
sha256_armhf=5b24999e1da04a6031ecca1a1a95386f87b4b23bbd0c59f61ebeea18557b5877

#amd64
sha256_amd64=ddfdd290c94768c2538b8546fd6c0ed2a0f0d2f3a5501e73a97f18edf4b9a167

url=https://dl.grafana.com/enterprise/release/grafana-enterprise_${GRAFANAVERSION}_$ARCHITECTURE.deb

url_armv6=https://dl.grafana.com/enterprise/release/grafana-enterprise-rpi_${GRAFANAVERSION}_$ARCHITECTURE.deb

if [ -n "$(uname -m | grep armv6)" ]
then
    grafana_deb_url="$url_armv6"
    sha256sum=sha256_armhf_v6
else
    grafana_deb_url="$url"
    sha256sumvar=sha256_${ARCHITECTURE}
    sha256sum=${!sha256sumvar}
fi

#=================================================
# PERSONAL HELPERS
#=================================================

#=================================================
# EXPERIMENTAL HELPERS
#=================================================

#=================================================
# FUTURE OFFICIAL HELPERS
#=================================================
