# Engineering Choices and Trade-Offs

## Objective

The goal was to build a working end-to-end store intelligence system within a limited evaluation timeline while maintaining reasonable engineering quality and business relevance.

Rather than optimizing for maximum detection accuracy, priority was given to producing reliable business metrics from CCTV footage.

---

## Choice 1: YOLOv8n Instead of Larger Models

### Decision

YOLOv8n was selected as the primary detection model.

### Why

* Fast inference speed
* Small model size
* Easy deployment on commodity hardware
* Sufficient accuracy for people detection

### Trade-off

A larger model such as YOLOv8m or YOLOv8l could improve detection quality but would significantly increase processing time.

For this challenge, speed and simplicity were prioritized.

---

## Choice 2: Event-Based Architecture

### Decision

Raw detections are converted into structured events.

Examples:

* ENTRY
* ZONE_ENTER
* ZONE_DWELL
* BILLING_QUEUE_JOIN

### Why

Business metrics should not depend directly on video processing logic.

Separating detection from analytics improves maintainability and allows future metrics to be added without modifying the detection pipeline.

### Trade-off

Additional event generation logic increases implementation complexity but provides a cleaner architecture.

---

## Choice 3: SQLite Instead of PostgreSQL

### Decision

SQLite was used as the event storage layer.

### Why

* Zero configuration
* Lightweight
* Easy reviewer setup
* Single-file database

### Trade-off

SQLite is not ideal for very large production deployments but is appropriate for evaluation and prototyping.

---

## Choice 4: Approximate Dwell Time Estimation

### Decision

Zone dwell events use estimated dwell duration values.

### Why

The provided CCTV footage did not contain complete cross-camera identity information.

Accurate multi-camera re-identification would require additional models and infrastructure.

### Trade-off

The system sacrifices perfect dwell accuracy in favor of generating meaningful behavioural metrics.

---

## Choice 5: Rule-Based Anomaly Detection

### Decision

Anomalies are generated using business thresholds.

Examples:

* Billing queue spike
* Low conversion rate

### Why

Business users require explainable alerts.

Rule-based alerts are transparent and easy to validate.

### Trade-off

Machine learning anomaly detection could identify more complex patterns but would reduce explainability and increase implementation complexity.

---

## Choice 6: Staff Area Exclusion

### Decision

Camera 4 is treated as a staff/back-office camera and excluded from customer analytics.

### Why

Including staff activity would distort customer metrics and conversion calculations.

### Trade-off

Some customer-related events may be missed, but metric quality improves significantly.

---
## Choice 7: Real POS Data Integration

### Decision

Instead of generating synthetic purchase events, the system integrates real POS transaction data provided with the challenge.

### Why

Retail analytics becomes significantly more valuable when behavioural events are connected with business outcomes.

By integrating transaction records, the system can calculate:

* Purchase Count
* Conversion Rate
* Revenue Estimation

This allows the analytics layer to move beyond customer observation and measure actual business impact.

### Trade-off

The provided CCTV footage and POS transactions represent different observation windows.

As a result, conversion calculations are approximate and should ideally be aligned using timestamps in a production environment.

Despite this limitation, integrating real transaction data provides more realistic business metrics than using simulated purchases.


## Edge Cases Considered

The system attempts to handle:

* Multiple people in the same frame
* Temporary occlusions
* Short-duration detections
* Staff movement
* Empty camera views
* Variable visitor counts

---

## Future Improvements

Potential future enhancements include:

### Cross-Camera Re-Identification

Track the same customer across multiple camera feeds to improve dwell accuracy and customer journey analysis.

### Timestamp-Aligned Conversion Analytics

Match CCTV events and POS transactions using aligned time windows to improve conversion rate accuracy.

### Real-Time Processing

Replace batch video processing with live camera stream ingestion.

### Advanced Anomaly Detection

Use machine learning based anomaly detection to identify unusual customer behaviour, queue patterns, or conversion drops.

### Interactive Dashboard

Provide real-time visualization of:

* Customer funnel
* Zone heatmaps
* Revenue metrics
* Queue monitoring

### Multi-Store Support

Extend the architecture to support multiple stores from a centralized analytics platform.


## Conclusion

The system prioritizes functional correctness, business relevance, deployment simplicity, and explainable analytics. The architecture was intentionally designed to balance engineering quality with the practical constraints of the challenge.
