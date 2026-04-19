from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from revoltutils import Config

from subdominator.core.constants import APP_NAME, DEFAULT_DB_NAME, DEFAULT_PROVIDER_CONFIG


class RuntimeSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SUBDOMINATOR_", extra="ignore")

    timeout: float = 20.0
    retries: int = 3
    retry_backoff: float = 1.0
    concurrency: int = 8
    recursive_depth: int = 0
    save_db: bool = True
    log_level: str = "INFO"
    proxy: str | None = None
    user_agent: str | None = None
    config_path: Path | None = None
    db_path: Path | None = None
    output: Path | None = None
    output_dir: Path | None = None
    json_output: bool = False
    table_output: bool = False
    no_color: bool = False
    all_resources: bool = False
    ssl_verify: bool = True
    include_resources: list[str] = Field(default_factory=list)
    exclude_resources: list[str] = Field(default_factory=list)

    @classmethod
    def defaults(cls) -> "RuntimeSettings":
        app_config = Config(app_name=APP_NAME)
        return cls(
            config_path=app_config.get_config_path(DEFAULT_PROVIDER_CONFIG),
            db_path=app_config.get_config_path(DEFAULT_DB_NAME),
        )
