Grafana for YunoHost
-----------------------------

**Important: This package is designed to be fed by the NetData application for monitoring measures, so please make sure the YunoHost [NetData package](https://github.com/YunoHost-Apps/netdata_ynh/) is installed before installing it!**

NetData only collects, displays and sets alarms based on data from the last hour; this packages allows to archive every metrics and put up statistics and dashboards on the long term.

Note: You can use it without NetData, but you'll have to install a collection application (e.g. collectd) to gather data.

**Important at first login:**

* you have to go the Grafana Menu (Grafana icon), select your account menu and select *Switch to Main Org.*
* you can now access the default NetData dashboard via the Home menu

**Don't hesitate to create new dashboards**: the default dashboard contains metrics from NetData, but only generic ones that are generated on every machine. NetData dynamically detects services and applications (e.g.redis, nginx, etc.) and enriches its dashboard and generated metrics. Many NetData metrics don't appear in the provided default Grafana dashboard!

**Warning**: The default dashboard may be updated in a further release of this package, so please make sure you create your own dashboards!


---
# Package description:

* installs InfluxDB as time series database
* if the NetData package is installed, configures NetData to feed InfluxDB every minute
* installs Grafana as dashboard server
* creates a Grafana Data Source to fetch data from InfluxDB (and hence NetData!)
* creates a default dashboard to plot some data from NetData (doesn't cover every metric, can be greatly enhanced!)

It has been tested on x86_64 and ARM.

## General architecture

![image](https://cloud.githubusercontent.com/assets/2662304/20649711/29f182ba-b4ce-11e6-97c8-ab2c0ab59833.png)


---
# InfluxDB
InfluxDB is an open source **time series database** with
**no external dependencies**. It's useful for recording metrics,
events, and performing analytics.

**Shipped version:** versions from Debian repositories (updated with the system)

## Features

* Built-in [HTTP API](https://docs.influxdata.com/influxdb/latest/guides/writing_data/) so you don't have to write any server side code to get up and running.
* Data can be tagged, allowing very flexible querying.
* SQL-like query language.
* Simple to install and manage, and fast to get data in and out.
* It aims to answer queries in real-time. That means every data point is
  indexed as it comes in and is immediately available in queries that
  should return in < 100ms.
  
---
# Grafana

Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, Elasticsearch, OpenTSDB, Prometheus and InfluxDB.

![](http://grafana.org/assets/img/features/dashboard_ex1.png)

## Features
### Graphite Target Editor
- Graphite target expression parser
- Feature rich query composer
- Quickly add and edit functions & parameters
- Templated queries
- [See it in action](http://docs.grafana.org/datasources/graphite/)

### Graphing
- Fast rendering, even over large timespans
- Click and drag to zoom
- Multiple Y-axis, logarithmic scales
- Bars, Lines, Points
- Smart Y-axis formatting
- Series toggles & color selector
- Legend values, and formatting options
- Grid thresholds, axis labels
- [Annotations](http://docs.grafana.org/reference/annotations/)
- Any panel can be rendered to PNG (server side using phantomjs)

### Dashboards
- Create, edit, save & search dashboards
- Change column spans and row heights
- Drag and drop panels to rearrange
- [Templating](http://docs.grafana.org/reference/templating/)
- [Scripted dashboards](http://docs.grafana.org/reference/scripting/)
- [Dashboard playlists](http://docs.grafana.org/reference/playlist/)
- [Time range controls](http://docs.grafana.org/reference/timerange/)
- [Share snapshots publicly](http://docs.grafana.org/v2.0/reference/sharing/)

### Elasticsearch
- Feature rich query editor UI

### InfluxDB
- Use InfluxDB as a metric data source, annotation source
- Query editor with series and column typeahead, easy group by and function selection

### OpenTSDB
- Use as metric data source
- Query editor with metric name typeahead and tag filtering

# Links

 * Report a bug: https://github.com/YunoHost-Apps/grafana_ynh/issues
 * InfluxDB website: https://www.influxdata.com/
 * Grafana website: http://grafana.org/
 * YunoHost website: https://yunohost.org/
