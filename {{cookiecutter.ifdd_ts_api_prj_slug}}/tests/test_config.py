"""Static checks of the instance configuration (no Docker, no service)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
COMPOSE = {mode: ROOT / f"docker-compose-{mode}.yml" for mode in ("production", "development")}


def dotenv() -> dict[str, str]:
    values = {}
    for line in (ROOT / "dotenv.dist").read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            key, _, value = line.partition("=")
            values[key] = value.strip("'")
    return values


def service(mode: str) -> dict:
    return yaml.safe_load(COMPOSE[mode].read_text())["services"]["api"]


def labels(mode: str) -> dict[str, str]:
    return dict(label.split("=", 1) for label in service(mode).get("labels", []))


@pytest.mark.parametrize("mode", COMPOSE)
def test_container_is_hardened(mode):
    api = service(mode)
    assert api["read_only"] is True
    assert api["cap_drop"] == ["ALL"]
    assert "no-new-privileges:true" in api["security_opt"]
    assert api["tmpfs"] == ["/tmp"]


def test_router_takes_only_the_path_on_the_grafana_host():
    env = dotenv()
    host = re.match(r"https?://([^/]+)", env["IFDD_TS_API_URL"]).group(1)
    rules = [v for k, v in labels("production").items() if k.endswith(".rule")]
    assert rules == [f"Host(`{host}`) && PathPrefix(`{env['IFDD_TS_API_PATH']}`)"]


def test_no_router_tls_or_entrypoint_labels():
    for key in labels("production"):
        assert ".tls" not in key and "entrypoints" not in key, key


def test_router_service_and_port_match():
    found = labels("production")
    routers = {k.split(".")[3] for k in found if k.startswith("traefik.http.routers.")}
    services = {k.split(".")[3] for k in found if k.startswith("traefik.http.services.")}
    assert routers == services
    (port,) = [v for k, v in found.items() if k.endswith("loadbalancer.server.port")]
    assert port == dotenv()["PORT"]


def test_security_headers():
    middlewares = [v for k, v in labels("production").items() if k.endswith(".middlewares")]
    assert middlewares == ["security-headers@file,csp-api-docs@file"]


def test_production_publishes_no_port_and_development_only_loopback():
    assert "ports" not in service("production")
    for mapping in service("development")["ports"]:
        assert mapping.startswith("127.0.0.1:")
    assert labels("development") == {"traefik.enable": "false"}
    assert service("development")["environment"]["IFDD_TS_API_AUTH_ENABLED"] == "false"


@pytest.mark.parametrize("mode", COMPOSE)
def test_networks(mode):
    document = yaml.safe_load(COMPOSE[mode].read_text())
    assert set(service(mode)["networks"]) == {"ext-proxy-net", "ingest"}
    assert all(network["external"] for network in document["networks"].values())


def test_oidc_urls_belong_to_the_realm():
    env = dotenv()
    realm = env["IFDD_OIDC_ISSUER"]
    assert env["IFDD_OIDC_JWKS_URL"] == realm + "/protocol/openid-connect/certs"
    assert env["IFDD_OIDC_TOKEN_URL"] == realm + "/protocol/openid-connect/token"
    assert env["IFDD_TS_API_AUTH_ENABLED"] == "true"


def test_roles_are_no_store_patterns():
    env = dotenv()
    assert "." not in env["IFDD_TS_ROLE_READ"] and "." not in env["IFDD_TS_ROLE_WRITE"]


def test_settings_accept_the_values():
    from app.settings import Settings

    env = dotenv()
    settings = Settings(**{k: v for k, v in env.items() if k.startswith(("IFDD_", "API_"))})
    assert settings.IFDD_TS_API_PATH == env["IFDD_TS_API_PATH"]
    assert settings.IFDD_TS_MAX_ITEMS == int(env["IFDD_TS_MAX_ITEMS"])
