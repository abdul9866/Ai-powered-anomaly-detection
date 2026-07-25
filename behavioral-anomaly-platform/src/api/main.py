"""FastAPI entrypoint serving the SOC dashboard.

Endpoints here will be backed by src/streaming/worker.py (writes scored
alerts to Postgres/Redis) once the detection pipeline is built. For now
this exposes health checks and the route contracts the dashboard expects,
so frontend and backend can be developed in parallel.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.config import get_model_config

app = FastAPI(
    title="Behavioral Anomaly Detection API",
    version="0.1.0",
    description="Serves scored alerts, entity risk history, and explainability data to the SOC dashboard.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/config")
def config() -> dict:
    """Expose non-sensitive detection config so the dashboard can display
    the active alert budget, primary model, etc."""
    cfg = get_model_config()
    return {
        "primary_model": cfg.detection["primary_model"],
        "alert_budget_pct": cfg.detection["alert_budget_pct"],
        "classification_model": cfg.classification["model"],
    }


@app.get("/alerts")
def list_alerts(limit: int = 50) -> list[dict]:
    """Returns the most recent ranked alerts. Backed by Postgres once
    src/alerting/engine.py is implemented; stubbed here with the response
    contract the dashboard expects."""
    return []


@app.get("/alerts/{alert_id}")
def get_alert(alert_id: str) -> dict:
    """Returns a single alert with full explainability payload
    (top features, SHAP values, natural-language reason, timeline)."""
    return {}
