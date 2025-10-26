# 🧠 Pi-Edge-Spark  
**Edge-Orchestrated Data Processing with Apache Spark on Raspberry Pi**

---

## 📘 Overview
**Pi-Edge-Spark** demonstrates how to use **Apache Spark** as a central orchestrator to coordinate multiple **edge-computing devices** (such as Raspberry Pi) for distributed **data cleaning, preprocessing, and aggregation**.

Instead of sending all raw data to the cloud, each edge node performs lightweight ETL locally — reducing bandwidth and latency — while Spark manages job distribution and global analytics.

> 💡 Goal: Build a mini **Edge-Cloud Collaborative Data Pipeline** powered by Spark + Python.

## 🏗️ System Architecture

```text
                  ┌───────────────────────────────┐
                  │       Spark Master (Cloud)    │
                  │ ───────────────────────────── │
                  │ • Job Orchestrator            │
                  │ • Global Aggregation          │
                  └──────────────┬────────────────┘
                                 │ Spark Jobs (HTTP/MQTT)
             ┌───────────────────┼───────────────────┐
             │                   │                   │
      ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
      │  Edge Node 1 │    │  Edge Node 2 │    │  Edge Node 3 │
      │ (Raspberry)  │    │ (Raspberry)  │    │ (Raspberry)  │
      │ ─────────────│    │ ─────────────│    │ ─────────────│
      │ • SparkWorker│    │ • SparkWorker│    │ • SparkWorker│
      │ • Edge Agent │    │ • Edge Agent │    │ • Edge Agent │
      │ • Local ETL  │    │ • Local ETL  │    │ • Local ETL  │
      └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
             │                   │                   │
        Cleaned CSV          Cleaned CSV         Cleaned CSV
             └───────────────→───────────────→───────────────┘
                       Aggregated by Spark Master
```

## ⚙️ Features
- 🧩 **Edge-aware Spark Jobs** — Spark Driver sends ETL tasks to Raspberry Pi nodes.  
- 🧮 **Distributed Data Cleaning** — Each edge node runs its own Python ETL agent.  
- 📤 **Unified Aggregation** — Cleaned data is sent back to the Spark cluster or shared storage.  
- 🌐 **Lightweight Communication** — Implemented via REST API (Flask) or MQTT.  
- ⚡ **Low-Cost Deployment** — Runs entirely on 4 Raspberry Pi boards.  

---

## 📂 Project Structure

```text
pi-edge-spark/
├── edge_jobs/                     # Edge node ETL and preprocessing scripts
│   ├── edge_clean_job.py          # Cleans local raw data on Raspberry Pi
│   └── edge_feature_job.py        # Extracts local statistical features
│
├── spark_jobs/                    # Spark driver orchestration and aggregation
│   ├── distribute_task.py         # Sends ETL tasks to edge nodes via HTTP
│   ├── aggregate_results.py       # Aggregates cleaned data from all edges
│   └── utils/
│       └── edge_comm.py           # Communication helper (REST / MQTT)
│
├── edge_agent/                    # Lightweight Flask agent running on edge
│   └── edge_server.py             # Listens for Spark task requests and runs jobs
│
├── conf/                          # Spark configuration files
│   ├── spark-env.sh               # Environment variables for Spark runtime
│   └── workers                    # List of edge worker IP addresses
│
├── scripts/                       # Cluster control and pipeline execution
│   ├── start_cluster.sh           # Starts Spark master and worker processes
│   ├── start_edge_agents.sh       # Starts Flask agents on all Raspberry Pis
│   ├── submit_etl_pipeline.sh     # Unified entry point to trigger Spark jobs
│
└── README.md                      # Project documentation and setup guide
```