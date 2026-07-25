# Build plan

Tracks progress against the full project scope. Check items off as we
complete each session.

## Done
- [x] Repository scaffolding (folder structure, configs, Docker, CI)
- [x] `configs/data_config.yaml` — attack taxonomy with MITRE ATT&CK mapping
- [x] `configs/model_config.yaml` — model/detection/risk-scoring parameters
- [x] `src/utils/config.py` — typed config loader
- [x] `src/api/main.py` — FastAPI skeleton with route contracts
- [x] `docker-compose.yml` + per-service Dockerfiles
- [x] GitHub Actions CI (lint + test + dashboard build)

## Next (in order)
- [ ] `data_generator/` — synthetic entity + session generator (Faker-based)
- [ ] `data_generator/attacks.py` — 17 attack-pattern injectors from the taxonomy
- [ ] `src/features/` — rolling-window, geo-velocity, entropy, drift features
- [ ] `src/models/profiling/` — per-entity baseline (rolling stats + autoencoder)
- [ ] `src/models/detection/` — sequence anomaly detector (start with Isolation
      Forest + Autoencoder as fast baselines, then LSTM/Transformer)
- [ ] `src/models/classification/` — XGBoost attack-type classifier
- [ ] `src/explainability/` — SHAP + natural-language alert generator
- [ ] `src/risk_engine/` — calibrated risk score
- [ ] `src/alerting/` — dedup + alert-budget enforcement
- [ ] `src/streaming/worker.py` — Kafka consumer wiring the pipeline together
- [ ] `dashboard/` — React SOC UI (alert queue, timeline, risk gauge, explain panel)
- [ ] `scripts/generate_data.py`, `build_features.py`, `train.py`, `evaluate.py`
- [ ] `tests/` — unit tests per module, integration test for full pipeline
- [ ] `reports/evaluation_report.md` — metrics, assumptions, known limitations
- [ ] Presentation deck
- [ ] IEEE-format paper

## Design decisions log
- **Imbalance strategy**: train detector unsupervised/semi-supervised on
  mostly-normal data; use labels only for classification stage and evaluation.
- **Alert budget**: fixed at top 1% of scored events by default
  (`configs/model_config.yaml: detection.alert_budget_pct`), tunable per demo.
- **Cold start**: new entities fall back to a population-level baseline
  (grouped by `entity_type`) until they accumulate enough history for a
  personal baseline — see `src/models/profiling/` once implemented.
