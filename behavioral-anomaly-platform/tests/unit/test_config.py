"""Sanity tests for the config loader — first thing CI should catch if
someone breaks the YAML schema."""
from src.utils.config import get_data_config, get_model_config


def test_data_config_loads():
    cfg = get_data_config()
    assert cfg.num_events > 0
    assert 0 < cfg.anomaly_rate < 1
    assert "brute_force" in cfg.attack_taxonomy


def test_model_config_loads():
    cfg = get_model_config()
    assert cfg.detection["primary_model"] in {
        "isolation_forest", "one_class_svm", "autoencoder", "lstm", "gru", "transformer"
    }
    assert cfg.classification["model"] in {"xgboost", "lightgbm", "random_forest", "catboost"}
