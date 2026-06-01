import json
import csv
from fastapi import FastAPI
from typing import List
from app.models import Event
from app.database import init_db, get_connection

app = FastAPI(title="Store Intelligence API")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "store-intelligence-api"
    }


@app.post("/events/ingest")
def ingest_events(events: List[Event]):
    conn = get_connection()
    cur = conn.cursor()

    inserted = 0
    duplicates = 0

    for event in events:
        try:
            cur.execute("""
                INSERT INTO events (
                    event_id, store_id, camera_id, visitor_id, event_type,
                    timestamp, zone_id, dwell_ms, is_staff, confidence, metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.event_id,
                event.store_id,
                event.camera_id,
                event.visitor_id,
                event.event_type,
                event.timestamp.isoformat(),
                event.zone_id,
                event.dwell_ms,
                int(event.is_staff),
                event.confidence,
                json.dumps(event.metadata)
            ))
            inserted += 1
        except Exception:
            duplicates += 1

    conn.commit()
    conn.close()

    return {
        "received": len(events),
        "inserted": inserted,
        "duplicates": duplicates
    }



@app.get("/stores/{store_id}/metrics")
def get_metrics(store_id: str):
    conn = get_connection()
    cur = conn.cursor()

    total_entries = cur.execute("""
        SELECT COUNT(*) FROM events
        WHERE store_id = ? AND event_type = 'ENTRY' AND is_staff = 0
    """, (store_id,)).fetchone()[0]

    unique_visitors = cur.execute("""
        SELECT COUNT(DISTINCT visitor_id) FROM events
        WHERE store_id = ? AND is_staff = 0
    """, (store_id,)).fetchone()[0]

    avg_dwell = cur.execute("""
        SELECT AVG(dwell_ms) FROM events
        WHERE store_id = ? AND event_type = 'ZONE_DWELL' AND is_staff = 0
    """, (store_id,)).fetchone()[0]

    queue_events = cur.execute("""
        SELECT COUNT(*) FROM events
        WHERE store_id = ? AND event_type = 'BILLING_QUEUE_JOIN' AND is_staff = 0
    """, (store_id,)).fetchone()[0]

    purchase_invoices = set()
    revenue = 0.0

    csv_store_id = "ST1008" if store_id == "STORE_001" else store_id

    try:
        with open("data/pos_transactions.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if row["store_id"] == csv_store_id and row["invoice_type"] == "sales":
                    purchase_invoices.add(row["invoice_number"])
                    revenue += float(row["NMV"])
    except:
        purchase_invoices = set()
        revenue = 0.0

    purchase_count = len(purchase_invoices)

    conversion_rate = 0
    if unique_visitors > 0:
        conversion_rate = round((purchase_count / unique_visitors) * 100, 2)

    conn.close()

    return {
        "store_id": store_id,
        "total_entries": total_entries,
        "unique_visitors": unique_visitors,
        "average_dwell_ms": avg_dwell or 0,
        "billing_queue_joins": queue_events,
        "purchases": purchase_count,
        "conversion_rate": conversion_rate,
        "estimated_revenue": revenue
    }
@app.get("/stores/{store_id}/funnel")
def get_funnel(store_id: str):
    conn = get_connection()
    cur = conn.cursor()

    entry = cur.execute("""
        SELECT COUNT(DISTINCT visitor_id) FROM events
        WHERE store_id = ? AND event_type = 'ENTRY' AND is_staff = 0
    """, (store_id,)).fetchone()[0]

    zone_visit = cur.execute("""
        SELECT COUNT(DISTINCT visitor_id) FROM events
        WHERE store_id = ? AND event_type = 'ZONE_ENTER' AND is_staff = 0
    """, (store_id,)).fetchone()[0]

    billing_queue = cur.execute("""
        SELECT COUNT(DISTINCT visitor_id) FROM events
        WHERE store_id = ? AND event_type = 'BILLING_QUEUE_JOIN' AND is_staff = 0
    """, (store_id,)).fetchone()[0]

    conn.close()

    csv_store_id = "ST1008" if store_id == "STORE_001" else store_id
    purchase_invoices = set()

    try:
        with open("data/pos_transactions.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["store_id"] == csv_store_id and row["invoice_type"] == "sales":
                    purchase_invoices.add(row["invoice_number"])
    except:
        purchase_invoices = set()

    purchase_count = len(purchase_invoices)

    return {
        "store_id": store_id,
        "funnel": {
            "entry": entry,
            "zone_visit": zone_visit,
            "billing_queue": billing_queue,
            "purchase": purchase_count
        }
    }


@app.get("/stores/{store_id}/heatmap")
def get_heatmap(store_id: str):
    conn = get_connection()
    cur = conn.cursor()

    rows = cur.execute("""
        SELECT zone_id, COUNT(*) as visits, AVG(dwell_ms) as avg_dwell_ms
        FROM events
        WHERE store_id = ?
        AND event_type IN ('ZONE_ENTER', 'ZONE_DWELL')
        AND zone_id IS NOT NULL
        AND is_staff = 0
        GROUP BY zone_id
    """, (store_id,)).fetchall()

    conn.close()

    heatmap = {}
    for row in rows:
        heatmap[row["zone_id"]] = {
            "visits": row["visits"],
            "avg_dwell_ms": row["avg_dwell_ms"] or 0
        }

    return {
        "store_id": store_id,
        "heatmap": heatmap
    }


@app.get("/stores/{store_id}/anomalies")
def get_anomalies(store_id: str):
    conn = get_connection()
    cur = conn.cursor()

    queue_depth = cur.execute("""
        SELECT MAX(CAST(json_extract(metadata, '$.queue_depth') AS INTEGER))
        FROM events
        WHERE store_id = ?
        AND event_type = 'BILLING_QUEUE_JOIN'
        AND is_staff = 0
    """, (store_id,)).fetchone()[0]

    unique_visitors = cur.execute("""
        SELECT COUNT(DISTINCT visitor_id)
        FROM events
        WHERE store_id = ?
        AND is_staff = 0
    """, (store_id,)).fetchone()[0]

    conn.close()

    csv_store_id = "ST1008" if store_id == "STORE_001" else store_id
    purchase_invoices = set()

    try:
        with open("data/pos_transactions.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["store_id"] == csv_store_id and row["invoice_type"] == "sales":
                    purchase_invoices.add(row["invoice_number"])
    except:
        purchase_invoices = set()

    purchase_count = len(purchase_invoices)

    conversion_rate = 0
    if unique_visitors > 0:
        conversion_rate = (purchase_count / unique_visitors) * 100

    anomalies = []

    if queue_depth and queue_depth >= 5:
        anomalies.append({
            "type": "BILLING_QUEUE_SPIKE",
            "severity": "WARN",
            "message": "Billing queue depth crossed threshold.",
            "suggested_action": "Open another billing counter or assign staff to billing area."
        })

    if conversion_rate < 20:
        anomalies.append({
            "type": "CONVERSION_DROP",
            "severity": "WARN",
            "message": "Conversion rate below target threshold.",
            "suggested_action": "Improve product placement, promotions, or staff assistance."
        })

    if not anomalies:
        anomalies.append({
            "type": "NORMAL",
            "severity": "INFO",
            "message": "No major anomaly detected.",
            "suggested_action": "No action required."
        })

    return {
        "store_id": store_id,
        "anomalies": anomalies
    }