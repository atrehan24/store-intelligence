# System Design

## 1. Objective

The objective of this system is to transform raw retail CCTV footage into structured behavioural events and actionable business intelligence metrics.

The system combines computer vision, event processing, transaction analytics, and REST APIs to provide insights into customer movement, engagement, and store performance.

---

## 2. High-Level Architecture

```text
CCTV Cameras
      │
      ▼
YOLOv8 Person Detection
      │
      ▼
ByteTrack Multi-Object Tracking
      │
      ▼
Event Generation Layer
      │
      ▼
FastAPI Ingestion Service
      │
      ▼
SQLite Event Database
      │
      ▼
Analytics & Business Logic
      │
      ▼
Metrics APIs
```

The architecture follows an event-driven design where all analytics are generated from stored events rather than directly from video frames.

---

## 3. Detection and Tracking Layer

### YOLOv8 Person Detection

YOLOv8n is used to detect people within CCTV frames.

Only the person class is processed because customer movement is the primary business signal required for store analytics.

### ByteTrack Tracking

Detected individuals are assigned tracking IDs using ByteTrack.

Benefits:

* Reduces duplicate counting
* Maintains visitor identity within a camera stream
* Enables dwell estimation
* Enables queue analytics

Each tracked individual is represented as a unique visitor.

---

## 4. Camera Configuration

The provided CCTV setup consists of five cameras with different business purposes.

| Camera   | Purpose                  | Generated Events        |
| -------- | ------------------------ | ----------------------- |
| Camera 1 | Skincare Section         | ZONE_ENTER, ZONE_DWELL  |
| Camera 2 | Makeup Section           | ZONE_ENTER, ZONE_DWELL  |
| Camera 3 | Store Entry Area         | ENTRY                   |
| Camera 4 | Staff / Back Office Area | Excluded from Analytics |
| Camera 5 | Billing Counter          | BILLING_QUEUE_JOIN      |

### Camera 4 Exclusion

Camera 4 primarily captures staff operations and inventory activities.

Including these observations would distort customer analytics and therefore the camera is intentionally excluded from behavioural metrics.

---

## 5. Event Processing Layer

Video observations are converted into structured business events.

Supported event types:

### ENTRY

Generated when a visitor enters the store.

### ZONE_ENTER

Generated when a visitor enters a product category zone.

### ZONE_DWELL

Generated when a visitor spends measurable time within a zone.

### BILLING_QUEUE_JOIN

Generated when a visitor joins the billing queue.

This event-based architecture separates computer vision logic from business analytics.

---

## 6. Event Schema

Each event contains the following fields:

| Field      | Description                 |
| ---------- | --------------------------- |
| store_id   | Store identifier            |
| camera_id  | Source camera               |
| visitor_id | Tracked visitor             |
| event_type | Event category              |
| timestamp  | Event time                  |
| zone_id    | Product zone                |
| dwell_ms   | Dwell duration              |
| is_staff   | Staff exclusion flag        |
| confidence | Detection confidence        |
| metadata   | Additional event attributes |

The schema is intentionally extensible to support future analytics.

---

## 7. Data Storage Layer

SQLite is used as the event storage engine.

Reasons:

* Lightweight deployment
* Zero configuration
* Fast local execution
* Suitable for evaluation environments

All generated events are persisted before analytics are computed.

---

## 8. POS Integration

The system integrates transaction data from POS records.

Transaction data provides:

* Purchase count
* Revenue estimation
* Conversion rate

The integration allows behavioural observations from CCTV footage to be linked with business outcomes.

---

## 9. Analytics Layer

The analytics engine computes business metrics from stored events.

### Metrics

* Total Entries
* Unique Visitors
* Average Dwell Time
* Billing Queue Joins
* Purchases
* Conversion Rate
* Estimated Revenue

### Funnel Analytics

Customer journey:

```text
Entry
  ↓
Zone Visit
  ↓
Billing Queue
  ↓
Purchase
```

### Heatmap Analytics

Zone-level engagement metrics:

* Skincare
* Makeup

### Anomaly Detection

Current anomaly rules:

* Billing Queue Spike
* Conversion Drop
* Normal Operations

---

## 10. API Layer

FastAPI exposes analytics through REST endpoints.

| Endpoint               | Purpose            |
| ---------------------- | ------------------ |
| /health                | Service health     |
| /events/ingest         | Event ingestion    |
| /stores/{id}/metrics   | Business metrics   |
| /stores/{id}/funnel    | Funnel analytics   |
| /stores/{id}/heatmap   | Zone analytics     |
| /stores/{id}/anomalies | Operational alerts |

---

## 11. Testing and Validation

The system includes automated API tests using PyTest.

Validated components:

* Health endpoint
* Metrics endpoint
* Funnel endpoint
* Heatmap endpoint
* Anomaly endpoint

Current status:

* 5 Tests Passing

---

## 12. Future Enhancements

Potential future improvements include:

* Cross-camera re-identification
* Real-time video stream processing
* Advanced anomaly detection models
* Interactive analytics dashboards
* Multi-store deployment support

---

## Conclusion

The system provides a complete pipeline from CCTV footage to business intelligence metrics. By combining computer vision, event processing, POS integration, and analytics APIs, the solution demonstrates how retail video data can be converted into actionable operational insights.
