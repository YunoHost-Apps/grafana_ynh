<!--
N.B.: Questo README è stato automaticamente generato da <https://github.com/YunoHost/apps/tree/master/tools/readme_generator>
NON DEVE essere modificato manualmente.
-->

# Grafana per YunoHost

[![Livello di integrazione](https://dash.yunohost.org/integration/grafana.svg)](https://dash.yunohost.org/appci/app/grafana) ![Stato di funzionamento](https://ci-apps.yunohost.org/ci/badges/grafana.status.svg) ![Stato di manutenzione](https://ci-apps.yunohost.org/ci/badges/grafana.maintain.svg)

[![Installa Grafana con YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=grafana)

*[Leggi questo README in altre lingue.](./ALL_README.md)*

> *Questo pacchetto ti permette di installare Grafana su un server YunoHost in modo semplice e veloce.*  
> *Se non hai YunoHost, consulta [la guida](https://yunohost.org/install) per imparare a installarlo.*

## Panoramica

Grafana is a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources.

## YunoHost specific features

* installs InfluxDB as time series database
* if the NetData package is installed, configures NetData to feed InfluxDB every minute
* installs Grafana as dashboard server
* creates a Grafana Data Source to fetch data from InfluxDB (and hence NetData!)
* creates a default dashboard to plot some data from NetData (doesn't cover every metric, can be greatly enhanced!)


**Versione pubblicata:** 10.2.3~ynh1

**Prova:** <https://play.grafana.org>

## Screenshot

![Screenshot di Grafana](./doc/screenshots/Grafana8_Kubernetes.jpg)

## Documentazione e risorse

- Sito web ufficiale dell’app: <https://grafana.com/>
- Repository upstream del codice dell’app: <https://github.com/grafana/grafana>
- Store di YunoHost: <https://apps.yunohost.org/app/grafana>
- Segnala un problema: <https://github.com/YunoHost-Apps/grafana_ynh/issues>

## Informazioni per sviluppatori

Si prega di inviare la tua pull request alla [branch di `testing`](https://github.com/YunoHost-Apps/grafana_ynh/tree/testing).

Per provare la branch di `testing`, si prega di procedere in questo modo:

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
o
sudo yunohost app upgrade grafana -u https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
```

**Maggiori informazioni riguardo il pacchetto di quest’app:** <https://yunohost.org/packaging_apps>
