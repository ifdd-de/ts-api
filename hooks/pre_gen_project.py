"""Validation before generation.

Rejects values that would render but not work, so a mistake shows up here and
not later as a router Traefik drops, a token the API refuses or a role that
is read as a store pattern.
"""

import re
import sys
from urllib.parse import urlsplit

values = {
    "ifdd_ts_api_prj_name": r"""{{ cookiecutter.ifdd_ts_api_prj_name }}""",
    "ifdd_ts_api_prj_slug": "{{ cookiecutter.ifdd_ts_api_prj_slug }}",
    "ifdd_ts_api_path": "{{ cookiecutter.ifdd_ts_api_path }}",
    "ifdd_ts_api_url": "{{ cookiecutter.ifdd_ts_api_url }}",
    "ifdd_ts_api_port": "{{ cookiecutter.ifdd_ts_api_port }}",
    "ifdd_ts_api_max_workers": "{{ cookiecutter.ifdd_ts_api_max_workers }}",
    "ifdd_ts_api_log_level": "{{ cookiecutter.ifdd_ts_api_log_level }}",
    "ifdd_ts_api_max_items": "{{ cookiecutter.ifdd_ts_api_max_items }}",
    "ifdd_ts_api_vm_url": "{{ cookiecutter.ifdd_ts_api_vm_url }}",
    "ifdd_ts_api_oidc_client_id": "{{ cookiecutter.ifdd_ts_api_oidc_client_id }}",
    "ifdd_ts_api_role_read": "{{ cookiecutter.ifdd_ts_api_role_read }}",
    "ifdd_ts_api_role_write": "{{ cookiecutter.ifdd_ts_api_role_write }}",
    "ifdd_ts_host": "{{ cookiecutter.ifdd_ts_host }}",
    "ifdd_ts_ingest_network": "{{ cookiecutter.ifdd_ts_ingest_network }}",
    "ifdd_proxy_network": "{{ cookiecutter.ifdd_proxy_network }}",
    "ifdd_oidc_realm": "{{ cookiecutter.ifdd_oidc_realm }}",
    "ifdd_type_url": "{{ cookiecutter.ifdd_type_url }}",
    "ifdd_context_root": "{{ cookiecutter.ifdd_context_root }}",
    "ifdd_registry_url": "{{ cookiecutter.ifdd_registry_url }}",
}

HOST = r"[A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?"
NAME = r"[A-Za-z0-9][A-Za-z0-9_.-]*"
ROLE = r"[A-Za-z0-9][A-Za-z0-9_-]*"
URL = r"https?://[^\s/]+(/[^\s]*[^\s/])?"
LABEL = r"[a-z0-9]([a-z0-9-]*[a-z0-9])?"

rules = {
    "ifdd_ts_api_prj_name": (r"[^']+", "any text without a single quote"),
    "ifdd_ts_api_prj_slug": (r"[a-z0-9][a-z0-9-]*", "lower-case letters, digits and '-'"),
    "ifdd_ts_api_path": (r"(/[a-z0-9][a-z0-9-]*)+", "a path such as /tsapi (no trailing slash)"),
    "ifdd_ts_api_url": (URL, "an http(s) URL without trailing slash"),
    "ifdd_ts_api_port": (r"[1-9][0-9]{1,4}", "a port number"),
    "ifdd_ts_api_max_workers": (r"[1-9][0-9]?", "a number of processes, 1 to 99"),
    "ifdd_ts_api_log_level": (r"critical|error|warning|info|debug", "a uvicorn log level"),
    "ifdd_ts_api_max_items": (r"[1-9][0-9]*", "a positive whole number"),
    "ifdd_ts_api_vm_url": (URL, "an http(s) URL without trailing slash"),
    "ifdd_ts_api_oidc_client_id": (NAME, "a Keycloak client id"),
    # A role with a dot would be read as a store pattern.
    "ifdd_ts_api_role_read": (ROLE, "a role name without a dot"),
    "ifdd_ts_api_role_write": (ROLE, "a role name without a dot"),
    "ifdd_ts_host": (HOST, "a host name without scheme or path"),
    "ifdd_ts_ingest_network": (NAME, "a Docker network name"),
    "ifdd_proxy_network": (NAME, "a Docker network name"),
    "ifdd_oidc_realm": (r"https://[^\s/]+(/[^\s]*[^\s/])?", "the https URL of the realm, no trailing slash"),
    "ifdd_type_url": (URL, "an http(s) URL without trailing slash"),
    "ifdd_context_root": (rf"{LABEL}(\.{LABEL})+", "at least two lower-case labels, e.g. ifdd.de"),
    "ifdd_registry_url": (r"[^\s]+", "an image registry prefix"),
}

errors = []
for key, (pattern, meaning) in rules.items():
    if not re.fullmatch(pattern, values[key]):
        errors.append(f"{key}={values[key]!r}: expected {meaning}")

if not errors:
    url = urlsplit(values["ifdd_ts_api_url"])
    if url.hostname != values["ifdd_ts_host"].lower() or url.path != values["ifdd_ts_api_path"]:
        errors.append(
            "ifdd_ts_api_url must be the host ifdd_ts_host plus the path ifdd_ts_api_path, "
            f"e.g. https://{values['ifdd_ts_host']}{values['ifdd_ts_api_path']}"
        )
    if int(values["ifdd_ts_api_port"]) > 65535:
        errors.append("ifdd_ts_api_port: at most 65535")
    if values["ifdd_ts_api_role_read"] == values["ifdd_ts_api_role_write"]:
        errors.append("ifdd_ts_api_role_read and ifdd_ts_api_role_write must differ")
    if values["ifdd_ts_ingest_network"] == values["ifdd_proxy_network"]:
        errors.append("ifdd_ts_ingest_network must not be the proxy network")

for error in errors:
    print(f"ERROR: {error}", file=sys.stderr)
sys.exit(1 if errors else 0)
