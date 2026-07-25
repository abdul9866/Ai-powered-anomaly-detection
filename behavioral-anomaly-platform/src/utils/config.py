"""Centralized configuration loader.

Loads YAML configs from /configs and exposes them as typed settings objects
so every service (data generator, training scripts, API, streaming worker)
reads from a single source of truth instead of hardcoding paths/params.
"""
from __future__ import annotations

from pathlib import Path
from functools import lru_cache

import yaml
from pydantic import BaseModel

ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT_DIR / "configs"


class DataConfig(BaseModel):
    num_events: int
    anomaly_rate: float
    random_seed: int
    entities: dict
    fields: list[str]
    attack_taxonomy: dict


class ModelConfig(BaseModel):
    paths: dict
    profiling: dict
    detection: dict
    classification: dict
    explainability: dict
    risk_scoring: dict
    evaluation: dict


def _load_yaml(name: str) -> dict:
    path = CONFIG_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    with open(path, "r") as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def get_data_config() -> DataConfig:
    return DataConfig(**_load_yaml("data_config.yaml"))


@lru_cache(maxsize=1)
def get_model_config() -> ModelConfig:
    return ModelConfig(**_load_yaml("model_config.yaml"))
