from dataclasses import dataclass
from typing import List
import os, sys, yaml, logging, logging.config

APP_LOGGER = logging.getLogger("cosmetics")

@dataclass(frozen=True)
class AppConfig:
    model: str
    request_timeout_s: int
    max_retries: int
    retry_backoff_s: int
    cors_allowed_origins: List[str]

def _load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def init_config(app_yaml: str = "configs/app.yaml",
                logging_yaml: str = "configs/logging.yaml") -> AppConfig:
    if not (os.path.exists(app_yaml) and os.path.exists(logging_yaml)):
        print("Missing configs/app.yaml or configs/logging.yaml", file=sys.stderr)
        sys.exit(2)

    # set up logging first so subsequent logs are formatted
    with open(logging_yaml, "r", encoding="utf-8") as f:
        logging.config.dictConfig(yaml.safe_load(f))

    data = _load_yaml(app_yaml)
    if "app" not in data:
        print("configs/app.yaml must contain a top-level 'app' key", file=sys.stderr)
        sys.exit(2)
    raw = data["app"]

    # Strict file-based config (raise if missing)
    try:
        cfg = AppConfig(
            model=raw["model"],
            request_timeout_s=int(raw["request_timeout_s"]),
            max_retries=int(raw["max_retries"]),
            retry_backoff_s=int(raw["retry_backoff_s"]),
            cors_allowed_origins=raw.get("cors", {}).get("allowed_origins", []),
        )
    except KeyError as e:
        print(f"Missing required config key: {e}", file=sys.stderr)
        sys.exit(2)

    # Simple sanity checks
    if cfg.request_timeout_s <= 0 or cfg.max_retries < 0 or cfg.retry_backoff_s < 0:
        print("Timeout/retries/backoff must be positive integers.", file=sys.stderr)
        sys.exit(2)

    APP_LOGGER.info("Config loaded.", extra={"extra": {"model": cfg.model}})
    return cfg
