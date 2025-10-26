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
