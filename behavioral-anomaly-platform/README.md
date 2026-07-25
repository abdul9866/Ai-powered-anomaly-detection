# Behavioral Anomaly Detection Platform for Cybersecurity

AI/ML system that learns per-entity "normal" access behavior, detects intrusions
and compromised-credential activity in near real time, classifies the anomaly
type, attaches an explainable risk score, and surfaces everything through a
SOC analyst dashboard.

## Repository layout

```
data/                   Raw, synthetic, and processed datasets (gitignored except .gitkeep)
data_generator/         Synthetic enterprise log generator + attack injectors
src/
  ingestion/            Kafka producers/consumers, schema validation
  features/             Rolling-window & behavioral feature engineering
  models/
    profiling/          Per-entity baseline models (stats / autoencoder)
    detection/          Sequence anomaly detectors (LSTM/GRU/Transformer, IF, OC-SVM)
    classification/     Attack-type classifiers (XGBoost/LightGBM)
  explainability/       SHAP/LIME + natural-language alert generation
  risk_engine/          Risk score calibration and aggregation
  alerting/             Dedup, budget enforcement, alert routing
  streaming/            Real-time scoring service (consumes Kafka, emits alerts)
  api/                  FastAPI backend serving the dashboard
  utils/                Shared config, logging, schema definitions
dashboard/              React SOC analyst dashboard
notebooks/              EDA, model comparison, evaluation notebooks
tests/                  Unit + integration tests
configs/                YAML configs (data schema, model hyperparams, thresholds)
docker/                 Dockerfiles per service
deployment/             k8s manifests, terraform (optional cloud deploy)
.github/workflows/      CI: lint, test, build
docs/                   Architecture notes, MITRE ATT&CK mapping, design decisions
reports/                Evaluation report, assumptions & limitations doc
scripts/                One-off / setup scripts (generate data, train, evaluate)
```

## Quickstart (local, no Kafka)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. Generate synthetic data
python scripts/generate_data.py --events 100000 --out data/synthetic/events.parquet

# 2. Build features
python scripts/build_features.py --in data/synthetic/events.parquet --out data/processed/features.parquet

# 3. Train baseline + detector + classifier
python scripts/train.py --config configs/model_config.yaml

# 4. Evaluate
python scripts/evaluate.py --config configs/model_config.yaml

# 5. Run the API (serves scored alerts to the dashboard)
uvicorn src.api.main:app --reload --port 8000

# 6. Run the dashboard
cd dashboard && npm install && npm run dev
```

## Status

Scaffolding stage — see `docs/BUILD_PLAN.md` for what's implemented vs. pending.
