"""Tests for configuration loading and overrides."""


import gpt_image_mcp.config as config_module


def test_default_models():
    settings = config_module.Settings()
    assert settings.image_model == "gpt-image-1"
    assert settings.default_model == "gpt-image-1"
    assert settings.fallback_model == "dall-e-3"
    assert settings.analysis_model == "gpt-4o"


def test_server_name_default(monkeypatch):
    monkeypatch.delenv("SERVER_NAME", raising=False)
    settings = config_module.Settings(_env_file=None)
    assert settings.server_name == "gpt-image-mcp"


def test_env_override(monkeypatch):
    monkeypatch.setenv("IMAGE_MODEL", "dall-e-3")
    monkeypatch.setenv("ANALYSIS_MODEL", "gpt-4o-mini")
    settings = config_module.Settings()
    assert settings.image_model == "dall-e-3"
    assert settings.analysis_model == "gpt-4o-mini"


def test_openai_client_config(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-123")
    settings = config_module.Settings()
    cfg = settings.openai_client_config
    assert cfg["api_key"] == "sk-test-123"
