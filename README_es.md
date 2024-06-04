<!--
Este archivo README esta generado automaticamente<https://github.com/YunoHost/apps/tree/master/tools/readme_generator>
No se debe editar a mano.
-->

# Grafana para Yunohost

[![Nivel de integración](https://dash.yunohost.org/integration/grafana.svg)](https://dash.yunohost.org/appci/app/grafana) ![Estado funcional](https://ci-apps.yunohost.org/ci/badges/grafana.status.svg) ![Estado En Mantención](https://ci-apps.yunohost.org/ci/badges/grafana.maintain.svg)

[![Instalar Grafana con Yunhost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=grafana)

*[Leer este README en otros idiomas.](./ALL_README.md)*

> *Este paquete le permite instalarGrafana rapidamente y simplement en un servidor YunoHost.*  
> *Si no tiene YunoHost, visita [the guide](https://yunohost.org/install) para aprender como instalarla.*

## Descripción general

Grafana is a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources.

## YunoHost specific features

* installs InfluxDB as time series database
* if the NetData package is installed, configures NetData to feed InfluxDB every minute
* installs Grafana as dashboard server
* creates a Grafana Data Source to fetch data from InfluxDB (and hence NetData!)
* creates a default dashboard to plot some data from NetData (doesn't cover every metric, can be greatly enhanced!)


**Versión actual:** 10.2.3~ynh1

**Demo:** <https://play.grafana.org>

## Capturas

![Captura de Grafana](./doc/screenshots/Grafana8_Kubernetes.jpg)

## Documentaciones y recursos

- Sitio web oficial: <https://grafana.com/>
- Repositorio del código fuente oficial de la aplicación : <https://github.com/grafana/grafana>
- Catálogo YunoHost: <https://apps.yunohost.org/app/grafana>
- Reportar un error: <https://github.com/YunoHost-Apps/grafana_ynh/issues>

## Información para desarrolladores

Por favor enviar sus correcciones a la [`branch testing`](https://github.com/YunoHost-Apps/grafana_ynh/tree/testing

Para probar la rama `testing`, sigue asÍ:

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
o
sudo yunohost app upgrade grafana -u https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
```

**Mas informaciones sobre el empaquetado de aplicaciones:** <https://yunohost.org/packaging_apps>
