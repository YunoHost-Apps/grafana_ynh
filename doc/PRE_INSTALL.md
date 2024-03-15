## Limitations

* The default dashboard may be updated in a further release of this package, so please make sure you create your own dashboards!
* Grafana needs InfluxDB to properly work, so it will be installed as a dependency
* Organizations creation doesn't play well with LDAP integration; it is disabled for standard users, but can't be disabled for administrators: **please do not create organizations**!
