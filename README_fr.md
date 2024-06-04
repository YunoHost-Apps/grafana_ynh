<!--
Nota bene : ce README est automatiquement généré par <https://github.com/YunoHost/apps/tree/master/tools/readme_generator>
Il NE doit PAS être modifié à la main.
-->

# Grafana pour YunoHost

[![Niveau d’intégration](https://dash.yunohost.org/integration/grafana.svg)](https://dash.yunohost.org/appci/app/grafana) ![Statut du fonctionnement](https://ci-apps.yunohost.org/ci/badges/grafana.status.svg) ![Statut de maintenance](https://ci-apps.yunohost.org/ci/badges/grafana.maintain.svg)

[![Installer Grafana avec YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=grafana)

*[Lire le README dans d'autres langues.](./ALL_README.md)*

> *Ce package vous permet d’installer Grafana rapidement et simplement sur un serveur YunoHost.*  
> *Si vous n’avez pas YunoHost, consultez [ce guide](https://yunohost.org/install) pour savoir comment l’installer et en profiter.*

## Vue d’ensemble

Grafana is a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources.

## YunoHost specific features

* installs InfluxDB as time series database
* if the NetData package is installed, configures NetData to feed InfluxDB every minute
* installs Grafana as dashboard server
* creates a Grafana Data Source to fetch data from InfluxDB (and hence NetData!)
* creates a default dashboard to plot some data from NetData (doesn't cover every metric, can be greatly enhanced!)


**Version incluse :** 10.2.3~ynh2

**Démo :** <https://play.grafana.org>

## Captures d’écran

![Capture d’écran de Grafana](./doc/screenshots/Grafana8_Kubernetes.jpg)

## Documentations et ressources

- Site officiel de l’app : <https://grafana.com/>
- Dépôt de code officiel de l’app : <https://github.com/grafana/grafana>
- YunoHost Store : <https://apps.yunohost.org/app/grafana>
- Signaler un bug : <https://github.com/YunoHost-Apps/grafana_ynh/issues>

## Informations pour les développeurs

Merci de faire vos pull request sur la [branche `testing`](https://github.com/YunoHost-Apps/grafana_ynh/tree/testing).

Pour essayer la branche `testing`, procédez comme suit :

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
ou
sudo yunohost app upgrade grafana -u https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
```

**Plus d’infos sur le packaging d’applications :** <https://yunohost.org/packaging_apps>
