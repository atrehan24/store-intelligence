# Store Intelligence API

## Overview

Store Intelligence API is an end-to-end retail analytics system that transforms raw CCTV footage into structured customer-behaviour events and business intelligence metrics.

The solution combines computer vision, event processing, transaction data, and analytics APIs to help retail operators understand customer movement, product engagement, queue behaviour, and store conversion performance.

The project was built as a complete pipeline starting from CCTV video streams and ending with actionable business insights.

---

## Problem Statement

Retail stores generate large amounts of CCTV footage but very little actionable intelligence from it.

Store managers need answers to questions such as:

* How many customers entered the store?
* Which sections attracted the most attention?
* How long did customers spend in specific zones?
* Are billing queues becoming too long?
* How many visitors converted into buyers?
* What revenue was generated from those visits?

This project addresses these questions by converting visual observations into structured events and business metrics.

---

## System Features

### Computer Vision Pipeline

The system processes CCTV footage using YOLOv8 object detection and ByteTrack multi-object tracking.

Generated events include:

* ENTRY
* ZONE_ENTER
* ZONE_DWELL
* BILLING_QUEUE_JOIN

### Event Ingestion API

Events are ingested through a FastAPI endpoint and stored in SQLite.

### Business Metrics

The API generates:

* Total Entries
* Unique Visitors
* Average Dwell Time
* Billing Queue Joins
* Purchases
* Conversion Rate
* Estimated Revenue

### Customer Funnel

Customer journey analytics:

Entry → Zone Visit → Billing Queue → Purchase

### Heatmap Analytics

Zone-level engagement metrics:

* Makeup Zone
* Skincare Zone
* Additional zones can be added easily

### Anomaly Detection

Business rule based anomaly detection:

* Billing Queue Spike
* Conversion Drop
* Normal Operations

---

## Technology Stack

| Layer            | Technology |
| ---------------- | ---------- |
| API              | FastAPI    |
| Database         | SQLite     |
| Computer Vision  | YOLOv8     |
| Tracking         | ByteTrack  |
| Video Processing | OpenCV     |
| Testing          | PyTest     |
| Containerization | Docker     |
| Language         | Python     |

---

## Project Structure

store-intelligence/

├── app/

├── pipeline/

├── data/

├── tests/

├── docs/

├── README.md

├── DESIGN.md

├── CHOICES.md

├── Dockerfile

├── docker-compose.yml

└── requirements.txt

---

## Running the API

Start the API server:

```bash
python -m uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Running the Detection Pipeline

Generate structured events from CCTV footage:

```bash
python pipeline/run.py
```

Send generated events to API:

```bash
python pipeline/send_events.py
```

---

## Running Tests

Execute automated tests:

```bash
python -m pytest tests/test_api.py
```
## Sample Outputs

Example API responses, pipeline execution screenshots and test results are available under:

docs/screenshots/

The repository intentionally excludes CCTV footage, model weights and POS datasets as required by the challenge guidelines.


Current status:

* 5 Tests Passing
* API Functional
* Event Pipeline Functional
* Metrics Endpoints Functional

---

## Example Outputs

### Metrics

* Total Entries
* Unique Visitors
* Conversion Rate
* Estimated Revenue

### Funnel

Entry → Zone Visit → Billing Queue → Purchase

### Heatmap

Zone-wise engagement and dwell analysis.

### Anomalies

Operational alerts generated from observed store behaviour.

---

## Future Improvements

* Real-time streaming support
* Multi-store analytics
* Advanced anomaly detection models
* Customer re-identification across cameras
* Interactive dashboard visualizations

---

## Author

Developed as part of the Store Intelligence Challenge.

Focus areas:

* Computer Vision
* Event Processing
* Retail Analytics
* Backend Engineering
* Business Intelligence
