Grafana is installed, but it does not collect any data by itself — without a data source, the dashboard list will stay empty.

To monitor your YunoHost server, the recommended companions are the **Prometheus** + **node_exporter** apps (metrics) and the **Loki** app (logs). See the *Documentation* tab of this app (ADMIN.md) for a step-by-step guide, including the YunoHost-specific data source URLs and a ready-to-use Promtail configuration.
