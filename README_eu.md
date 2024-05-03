<!--
Ohart ongi: README hau automatikoki sortu da <https://github.com/YunoHost/apps/tree/master/tools/readme_generator>ri esker
EZ editatu eskuz.
-->

# Grafana YunoHost-erako

[![Integrazio maila](https://dash.yunohost.org/integration/grafana.svg)](https://dash.yunohost.org/appci/app/grafana) ![Funtzionamendu egoera](https://ci-apps.yunohost.org/ci/badges/grafana.status.svg) ![Mantentze egoera](https://ci-apps.yunohost.org/ci/badges/grafana.maintain.svg)

[![Instalatu Grafana YunoHost-ekin](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=grafana)

*[Irakurri README hau beste hizkuntzatan.](./ALL_README.md)*

> *Pakete honek Grafana YunoHost zerbitzari batean azkar eta zailtasunik gabe instalatzea ahalbidetzen dizu.*  
> *YunoHost ez baduzu, kontsultatu [gida](https://yunohost.org/install) nola instalatu ikasteko.*

## Aurreikuspena

Grafana is a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources.

## YunoHost specific features

* installs InfluxDB as time series database
* if the NetData package is installed, configures NetData to feed InfluxDB every minute
* installs Grafana as dashboard server
* creates a Grafana Data Source to fetch data from InfluxDB (and hence NetData!)
* creates a default dashboard to plot some data from NetData (doesn't cover every metric, can be greatly enhanced!)


**Paketatutako bertsioa:** 10.2.3~ynh2

**Demoa:** <https://play.grafana.org>

## Pantaila-argazkiak

![Grafana(r)en pantaila-argazkia](./doc/screenshots/Grafana8_Kubernetes.jpg)

## Dokumentazioa eta baliabideak

- Aplikazioaren webgune ofiziala: <https://grafana.com/>
- Jatorrizko aplikazioaren kode-gordailua: <https://github.com/grafana/grafana>
- YunoHost Denda: <https://apps.yunohost.org/app/grafana>
- Eman errore baten berri: <https://github.com/YunoHost-Apps/grafana_ynh/issues>

## Garatzaileentzako informazioa

Bidali `pull request`a [`testing` abarrera](https://github.com/YunoHost-Apps/grafana_ynh/tree/testing).

`testing` abarra probatzeko, ondorengoa egin:

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
edo
sudo yunohost app upgrade grafana -u https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
```

**Informazio gehiago aplikazioaren paketatzeari buruz:** <https://yunohost.org/packaging_apps>
