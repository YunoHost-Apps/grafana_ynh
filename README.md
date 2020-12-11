# Grafana for YunoHost

[![Integration level](https://dash.yunohost.org/integration/grafana.svg)](https://dash.yunohost.org/appci/app/grafana) ![](https://ci-apps.yunohost.org/ci/badges/grafana.status.svg) ![](https://ci-apps.yunohost.org/ci/badges/grafana.maintain.svg)  
[![Install grafana with YunoHost](https://install-app.yunohost.org/install-with-yunohost.png)](https://install-app.yunohost.org/?app=grafana)

> *This package allows you to install grafana quickly and simply on a YunoHost server.  
If you don't have YunoHost, please see [here](https://yunohost.org/#/install) to know how to install and enjoy it.*

## Overview
**Important: This package is designed to be fed by the NetData application for monitoring measures, so please make sure the YunoHost [NetData package](https://github.com/YunoHost-Apps/netdata_ynh/) is installed before installing it!**

NetData only collects, displays and sets alarms based on data from the last hour; this packages allows to archive every metrics and put up statistics and dashboards on the long term.

Note: You can use it without NetData, but you'll have to install a collection application (e.g. collectd) to gather data.

**Shipped version:** 7.3.3

## Screenshots

![](https://grafana.com/api/dashboards/1295/images/838/image)

## Demo

* [Official demo](https://play.grafana.org)

## Configuration

**Important at first login:**

* you have to go the Grafana Menu (Grafana icon), select your account menu and select *Switch to Main Org.*
* you can now access the default NetData dashboard via the Home menu

**Don't hesitate to create new dashboards**: the default dashboard contains metrics from NetData, but only generic ones that are generated on every machine. NetData dynamically detects services and applications (e.g.redis, nginx, etc.) and enriches its dashboard and generated metrics. Many NetData metrics don't appear in the provided default Grafana dashboard!

## Documentation

 * Official Grafana documentation: https://grafana.com/docs/grafana/latest/
 * Official InfluxdB documentation: https://docs.influxdata.com/influxdb/
 * YunoHost documentation: If specific documentation is needed, feel free to contribute.

## YunoHost specific features

* installs InfluxDB as time series database
* if the NetData package is installed, configures NetData to feed InfluxDB every minute
* installs Grafana as dashboard server
* creates a Grafana Data Source to fetch data from InfluxDB (and hence NetData!)
* creates a default dashboard to plot some data from NetData (doesn't cover every metric, can be greatly enhanced!)

#### General architecture

![image](https://cloud.githubusercontent.com/assets/2662304/20649711/29f182ba-b4ce-11e6-97c8-ab2c0ab59833.png)

#### Multi-users support

LDAP and HTTP auth are supported.

#### Supported architectures

* x86-64 - [![Build Status](https://ci-apps.yunohost.org/ci/logs/grafana%20%28Apps%29.svg)](https://ci-apps.yunohost.org/ci/apps/grafana/)
* ARMv8-A - [![Build Status](https://ci-apps-arm.yunohost.org/ci/logs/grafana%20%28Apps%29.svg)](https://ci-apps-arm.yunohost.org/ci/apps/grafana/)

## Limitations

* The default dashboard may be updated in a further release of this package, so please make sure you create your own dashboards!
* Organizations creation doesn't play well with LDAP integration; it is disabled for standard users, but can't be disabled for administrators: **please do not create organizations**!

## Additional information

None.

## Links

 * Report a bug: https://github.com/YunoHost-Apps/grafana_ynh/issues
 * Grafana website: https://grafana.com/
 * Grafana upstream app repository: https://github.com/grafana/
 * InfluxDB website: https://www.influxdata.com/
 * InfluxDB upstream app repository: https://github.com/influxdata/influxdb
 * YunoHost website: https://yunohost.org/

---

## Developers info

Please do your pull request to the [testing branch](https://github.com/YunoHost-Apps/grafana_ynh/tree/testing).

To try the testing branch, please proceed like that.
```
sudo yunohost app install https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
or
sudo yunohost app upgrade grafana -u https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
```
