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

---

## ⚙️ Core Components

| Layer | Component | Description |
|-------|------------|-------------|
| **Edge** | 🐍 **Python Stream Producer** | Continuously reads local sensors or logs and publishes structured JSON messages to Redis Streams or Redpanda. |
| **Broker** | 🧩 **Redis Streams / Redpanda** | Acts as the lightweight message queue between Edge nodes and the central Spark cluster. |
| **Compute** | 🔥 **Spark Structured Streaming** | Performs real-time aggregation, cleaning, and anomaly detection across all Edge nodes. |
| **Storage** | ☁️ **MinIO / TimescaleDB** | Stores processed results, historical archives, and time-series metrics. |
| **Orchestration** | ⚙️ **Airflow** | Automates scheduled ETL runs, uploads, and cluster monitoring workflows. |
| **Visualization** | 📊 **Grafana / Streamlit** | Provides real-time dashboards and system health visualization for devices and KPIs. |

---

## 📂 Project File Structure

```text
Pi-Edge-Spark/
├── conf/
│   ├── cluster.yaml              # Cluster configuration (auto or manual worker list)
│   └── spark-env.sh              # Auto-generated Spark master environment file
│
├── data/
│   ├── raw/                      # Edge-sourced raw CSV or JSON input data
│   └── processed/                # Processed & aggregated data outputs
│
├── dags/
│   └── pi_edge_streaming_dag.py  # Airflow DAG for ETL orchestration and upload
│
├── scripts/
│   ├── init_cluster_env.py       # Detects master IP, writes spark-env.sh
│   ├── edge_producer.py          # Example edge node streaming data producer
│   ├── upload_to_minio.py        # Uploads processed results to MinIO
│   ├── setup_minio.py            # Initializes MinIO bucket and access policy
│   └── run_local_test.sh         # Local cluster test runner script
│
├── spark_jobs/
│   ├── streaming_etl.py          # Core Spark Structured Streaming job
│   └── batch_etl.py              # Offline fallback ETL process
│
├── docker/
│   ├── docker-compose.yml        # Optional: Spark + Redis + MinIO stack
│   └── airflow.dockerfile        # Lightweight Airflow image (for Pi/ARM)
│
├── requirements.txt              # Python dependency list
└── README.md                     # Project documentation
```