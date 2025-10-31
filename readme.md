# 🧠 Pi-Edge-Spark  
**Pi-Edge-Spark** is a distributed real-time ETL and streaming analytics platform  
built for edge clusters such as Raspberry Pi networks.  

It combines **PySpark Structured Streaming**, **Redis Streams**, and **MinIO**  
to provide an online data-processing framework where each edge node continuously  
produces sensor or event data, and a central Spark cluster performs live analytics,  
aggregation, and anomaly detection.

---

## ✨ Features

- **Dynamic edge discovery** — supports variable number of worker nodes.
- **Secure architecture** — no IPs hard-coded; cluster info injected at runtime.
- **Streaming ETL** — continuous ingestion + online aggregation.
- **Edge-to-Cloud bridge** — lightweight message broker (Redis Streams / Redpanda).
- **Hybrid storage** — MinIO (S3-compatible) for history, TimescaleDB for metrics.
- **Airflow orchestration** — DAGs trigger ETL & upload jobs automatically.
- **Visual analytics** — optional Grafana or Streamlit dashboards.

---

## 🧱 Architecture Overview
```text
    ┌──────────────────────────────────────────────┐
    │               Airflow DAGs                   │
    │  • Schedule ETL and upload jobs              │
    │  • Monitor cluster health                    │
    └──────────────────────────────────────────────┘
                       │
                       ▼
    ┌──────────────────────────────────────────────┐
    │        Spark Structured Streaming Cluster     │
    │  • Subscribe to Redis / Kafka topics          │
    │  • Aggregate, clean, and detect anomalies     │
    │  • Output → MinIO / TimescaleDB               │
    └──────────────────────────────────────────────┘
                       ▲
                       │
    ┌──────────────┬──────────────┬──────────────┐
    │ Edge Node 1  │ Edge Node 2  │ Edge Node N  │
    │──────────────│──────────────│──────────────│
    │ • Sensor data│ • File tail  │ • MQTT input  │
    │ • Python pub │ • Redis pub  │ • local ETL   │
    └──────────────┴──────────────┴──────────────┘
                       │
                       ▼
             Message Broker Layer
      (Redis Streams / Kafka / Redpanda)
```
