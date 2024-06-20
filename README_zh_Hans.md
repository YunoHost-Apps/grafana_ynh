<!--
注意：此 README 由 <https://github.com/YunoHost/apps/tree/master/tools/readme_generator> 自动生成
请勿手动编辑。
-->

# YunoHost 上的 Grafana

[![集成程度](https://dash.yunohost.org/integration/grafana.svg)](https://dash.yunohost.org/appci/app/grafana) ![工作状态](https://ci-apps.yunohost.org/ci/badges/grafana.status.svg) ![维护状态](https://ci-apps.yunohost.org/ci/badges/grafana.maintain.svg)

[![使用 YunoHost 安装 Grafana](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=grafana)

*[阅读此 README 的其它语言版本。](./ALL_README.md)*

> *通过此软件包，您可以在 YunoHost 服务器上快速、简单地安装 Grafana。*  
> *如果您还没有 YunoHost，请参阅[指南](https://yunohost.org/install)了解如何安装它。*

## 概况

Grafana is a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources.

## YunoHost specific features

* installs InfluxDB as time series database
* if the NetData package is installed, configures NetData to feed InfluxDB every minute
* installs Grafana as dashboard server
* creates a Grafana Data Source to fetch data from InfluxDB (and hence NetData!)
* creates a default dashboard to plot some data from NetData (doesn't cover every metric, can be greatly enhanced!)


**分发版本：** 10.2.3~ynh2

**演示：** <https://play.grafana.org>

## 截图

![Grafana 的截图](./doc/screenshots/Grafana8_Kubernetes.jpg)

## 文档与资源

- 官方应用网站： <https://grafana.com/>
- 上游应用代码库： <https://github.com/grafana/grafana>
- YunoHost 商店： <https://apps.yunohost.org/app/grafana>
- 报告 bug： <https://github.com/YunoHost-Apps/grafana_ynh/issues>

## 开发者信息

请向 [`testing` 分支](https://github.com/YunoHost-Apps/grafana_ynh/tree/testing) 发送拉取请求。

如要尝试 `testing` 分支，请这样操作：

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
或
sudo yunohost app upgrade grafana -u https://github.com/YunoHost-Apps/grafana_ynh/tree/testing --debug
```

**有关应用打包的更多信息：** <https://yunohost.org/packaging_apps>
