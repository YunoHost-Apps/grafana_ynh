## Connecting data sources

A fresh Grafana has no data sources: on its own it does not collect any metrics or logs, so the dashboard list will stay empty. The easiest way to fill it on YunoHost is to combine Grafana with these apps from the catalog:

- [Prometheus](https://apps.yunohost.org/app/prometheus) + [node_exporter](https://apps.yunohost.org/app/node_exporter) for **metrics** (CPU, RAM, disk, network…)
- [Loki](https://apps.yunohost.org/app/loki) (bundles Promtail) for **logs**

### Metrics: Prometheus + node_exporter

1. Install the `prometheus` and `node_exporter` apps.

2. Prometheus does not scrape node_exporter automatically. Append a scrape job to `/var/www/prometheus/prometheus.yml`:

   ```yaml
   scrape_configs:
     - job_name: node
       static_configs:
         - targets: ["127.0.0.1:9100"]
   ```

   then run `systemctl restart prometheus`.

3. In Grafana, go to *Connections → Data sources → Add data source → Prometheus*. The URL must contain the port **and** the installation path of the Prometheus app, because the YunoHost package runs Prometheus with a route prefix:

   ```
   http://localhost:<port><path>     e.g.  http://localhost:9090/prometheus
   ```

   You can look both values up with:

   ```bash
   yunohost app setting prometheus port
   yunohost app setting prometheus path
   ```

   Note that the port is **not always 9090**: if that port is already taken on your server (for example by Cockpit), YunoHost automatically picks a different one during installation.

4. To get a complete server dashboard without building anything yourself, go to *Dashboards → New → Import* and load dashboard ID **1860** ("Node Exporter Full") with the Prometheus data source you just created.

### Logs: Loki + Promtail

1. Install the `loki` app. It also sets up Promtail, the agent that reads log files and ships them to Loki.

2. Promtail ships **without any scrape targets**, so out of the box no logs are collected at all. Create a drop-in file, e.g. `/etc/loki/promtail.d/scrape.yaml`:

   ```yaml
   scrape_configs:
     - job_name: system
       static_configs:
         - targets: [localhost]
           labels:
             job: syslog
             __path__: /var/log/syslog
         - targets: [localhost]
           labels:
             job: auth
             __path__: /var/log/auth.log
     - job_name: nginx
       static_configs:
         - targets: [localhost]
           labels:
             job: nginx
             __path__: /var/log/nginx/*.log
   ```

3. Most system logs (`/var/log/syslog`, `/var/log/nginx/*`) are only readable for the `adm` group. Allow the `loki` user to read them, then restart Promtail:

   ```bash
   usermod -aG adm loki
   systemctl restart loki-promtail
   ```

   You can verify that lines are flowing with:

   ```bash
   curl -s http://127.0.0.1:9080/metrics | grep promtail_sent_entries_total
   ```

4. In Grafana, add a data source of type *Loki* with the URL `http://localhost:3100` (look the port up with `yunohost app setting loki port_http` if you changed it). Logs can then be browsed under *Explore*, for example with the query `{job="nginx"}`.

### Bonus: reusing Netdata's metrics

If the [Netdata](https://apps.yunohost.org/app/netdata) app is installed, its several thousand metrics (nginx, PHP-FPM, databases, per-application details…) can be pulled into Prometheus as well — no extra exporters needed. Add to `/var/www/prometheus/prometheus.yml`:

```yaml
  - job_name: netdata
    metrics_path: /api/v1/allmetrics
    params:
      format: [prometheus]
    honor_labels: true
    scrape_interval: 30s
    static_configs:
      - targets: ["127.0.0.1:19999"]
```

## Limitations

- Organizations creation doesn't play well with LDAP integration; it is disabled for standard users, but can't be disabled for administrators: **please do not create organizations**!
