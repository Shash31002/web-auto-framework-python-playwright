"""
Central place for environment/config access.
Mirrors the role your Jackson Databind config layer played in the Java
framework: one module everything else asks for settings/data instead of
reading files ad hoc.
"""
import os
import json
import yaml
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chromium")
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))


def load_json(filename: str):
    path = ROOT_DIR / "data" / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml(filename: str):
    path = ROOT_DIR / "data" / filename
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
