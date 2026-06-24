# 🚕 Real-Time Dynamic Ride-Hailing Pricing Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-CUDA%20Accelerated-orange.svg)
![PyArrow](https://img.shields.io/badge/PyArrow-Zero%20Copy-green.svg)

## 📌 Project Overview

This project is a lightweight, real-time dynamic pricing engine designed to simulate and process live ride-hailing requests similar to Uber and Lyft surge pricing systems.

Traditional big-data architectures often rely on Apache Spark, Kafka, and JVM-heavy infrastructure, which can be resource intensive. This system was intentionally designed to operate on constrained hardware environments while still supporting real-time feature engineering and machine learning inference.

The architecture leverages asynchronous streaming, zero-copy memory access, and GPU-accelerated machine learning to process millions of ride records efficiently.

### ✨ Key Engineering Features

* **Zero-Copy Data Ingestion**

  * Streams large Parquet datasets using `pyarrow.parquet.iter_batches`.
  * Processes data in micro-batches to avoid excessive memory consumption.

* **Stateful Feature Engineering**

  * Maintains rolling demand statistics using `collections.deque`.
  * Supports efficient O(1) insertion and eviction for sliding-window calculations.

* **GPU-Accelerated Pricing Model**

  * Uses XGBoost with CUDA acceleration.
  * Optimized for low-VRAM environments through shallow trees and warm-start initialization.

* **Asynchronous Streaming Architecture**

  * Simulates live ride requests directly from historical trip data.
  * Enables real-time demand analysis and dynamic price generation.

---

## 💾 Dataset Acquisition (NYC TLC)

This project uses the official New York City Taxi and Limousine Commission (TLC) trip records dataset.

### Download Instructions

1. Visit the NYC TLC Trip Record Data portal:
   https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

2. Navigate to the **Yellow Taxi Trip Records** section.

3. Download a recent Parquet dataset.

4. Example dataset:

   https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet

5. Place the downloaded file inside:

```text
data/raw/
```

Example:

```text
data/raw/yellow_tripdata_2023-01.parquet
```

**Note:** The January 2023 Parquet file is approximately 48 MB compressed and contains over 3 million ride records.

---

## 🚀 Setup & Installation

### 1. Prerequisites

* Python 3.10+
* NVIDIA GPU (optional, for CUDA acceleration)
* Latest NVIDIA Drivers
* CUDA Toolkit 12.x (recommended)

### 2. Clone the Repository

```bash
git clone https://github.com/YourUsername/pricing-engine.git
cd pricing-engine
```

### 3. Create a Virtual Environment

```bash
python -m venv pricing_engine_venv
```

Activate the environment:

**Windows**

```bash
pricing_engine_venv\Scripts\activate
```

**Linux / macOS**

```bash
source pricing_engine_venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure

```text
pricing_engine/
│
├── data/
│   └── raw/
│       └── yellow_tripdata_2023-01.parquet
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── simulator.py
│   ├── pipeline.py
│   └── model.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

### Component Overview

| File               | Purpose                                              |
| ------------------ | ---------------------------------------------------- |
| `app.py`           | Main application entry point                         |
| `simulator.py`     | Simulates real-time ride events from Parquet batches |
| `pipeline.py`      | Stateful feature engineering and demand aggregation  |
| `model.py`         | Dynamic pricing model implementation                 |
| `requirements.txt` | Project dependencies                                 |

---

## ⚡ Running the Pricing Engine

After downloading the dataset and installing dependencies:

```bash
python src/app.py
```

---

## 📈 Sample Output

```text
--- Starting Dynamic Pricing Engine ---

Loading historical data...
Initializing pricing model...

--- Listening to Live Ride Stream ---

Processed Batch 10

Pickup Zone: 148
10-Minute Demand: 298
Dynamic Price: $258.79

Pickup Zone: 68
10-Minute Demand: 244
Dynamic Price: $156.73
```

---

## 🧠 System Architecture

```text
NYC TLC Parquet Dataset
          │
          ▼
  Async Streaming Engine
      (simulator.py)
          │
          ▼
 Stateful Feature Pipeline
      (pipeline.py)
          │
          ▼
 Dynamic Pricing Model
       (model.py)
          │
          ▼
 Real-Time Price Output
```

---

## 📊 Performance Characteristics

### Memory Efficiency

* Processes millions of rows without loading the entire dataset into RAM.
* Uses PyArrow batch streaming for efficient data access.
* Maintains only rolling-window state in memory.

### GPU Utilization

When CUDA is enabled:

* XGBoost training and inference execute on the GPU.
* VRAM usage remains low through optimized model configuration.

### Monitoring GPU Usage

#### Windows

1. Open Task Manager.
2. Navigate to **Performance → GPU**.
3. Switch the graph view to **CUDA**.

#### Linux

```bash
watch -n 1 nvidia-smi
```

Monitor:

* GPU Utilization
* Memory Usage
* Active Processes

---

## 🔮 Future Enhancements

* Real-time API deployment using FastAPI
* Live Kafka integration
* Geospatial demand clustering
* Multi-city support
* Online model retraining
* Containerization with Docker
* Cloud deployment pipelines

---

## 👨‍💻 Author

Built as an end-to-end demonstration of:

* Streaming data pipelines
* Real-time feature engineering
* Dynamic pricing systems
* GPU-accelerated machine learning
* Memory-efficient large-scale data processing
