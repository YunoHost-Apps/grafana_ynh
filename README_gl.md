<!--
NOTA: Este README foi creado automáticamente por <https://github.com/YunoHost/apps/tree/master/tools/readme_generator>
NON debe editarse manualmente.
-->

# Grafana para YunoHost

[![Nivel de integración](https://dash.yunohost.org/integration/grafana.svg)](https://dash.yunohost.org/appci/app/grafana) ![Estado de funcionamento](https://ci-apps.yunohost.org/ci/badges/grafana.status.svg) ![Estado de mantemento](https://ci-apps.yunohost.org/ci/badges/grafana.maintain.svg)

[![Instalar Grafana con YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=grafana)

*[Le este README en outros idiomas.](./ALL_README.md)*

> *Este paquete permíteche instalar Grafana de xeito rápido e doado nun servidor YunoHost.*  
> *Se non usas YunoHost, le a [documentación](https://yunohost.org/install) para saber como instalalo.*

## Vista xeral

Grafana is a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources.

## YunoHost specific features

* installs InfluxDB as time series database
* if the NetData package is installed, configures NetData to feed InfluxDB every minute
* installs Grafana as dashboard server
* creates a Grafana Data Source to fetch data from InfluxDB (and hence NetData!)
* creates a default dashboard to plot some data from NetData (doesn't cover every metric, can be greatly enhanced!)


**Versión proporcionada:** 10.2.3~ynh1

**Demo:** <https://play.grafana.org>

## Capturas de pantalla

![Captura de pantalla de Grafana](./doc/screenshots/Grafana8_Kubernetes.jpg)

## Documentación e recursos

- Web oficial da app: <https://grafana.com/>
- Repositorio de orixe do código: <https://github.com/grafana/grafana>
- Tenda YunoHost: <https://apps.yunohost.org/app/grafana>
- Informar dun problema: <https://github.com/YunoHost-Apps/grafana_ynh/issues>

## Info de desenvolvemento

Envía a túa colaboración á [rama `testing`](https://github.com/YunoHost-Apps/grafana_ynh/tree/testing).

Para probar a rama `testing`, procede deste xeito:

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
ou
sudo yunohost app upgrade grafana -u https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
```

**Máis info sobre o empaquetado da app:** <https://yunohost.org/packaging_apps>
