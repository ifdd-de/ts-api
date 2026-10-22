"""Check the image setup of a rendered instance.

    python tests/check_image.py <rendered instance>

The API uses a plain python base image, runs as an unprivileged user and
starts uvicorn with the application of the instance (app.main:app).
"""

import sys
from pathlib import Path

ROOT_USERS = {"root", "0"}


def code_lines(text):
    """Non-comment, non-blank lines."""
    return [l for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#")]


def main(instance):
    inst = Path(instance)
    errors = []
    lines = code_lines((inst / "Dockerfile").read_text())
    first = next(l for l in lines if l.startswith("FROM "))
    if not first.startswith("FROM python:"):
        errors.append(f"base image is not python:*, got {first!r}")
    users = [l.split(None, 1)[1].strip() for l in lines if l.startswith("USER ")]
    if not users or users[-1].split(":")[0] in ROOT_USERS:
        errors.append("the container runs as root")
    if not any("HEALTHCHECK" in l for l in lines):
        errors.append("no HEALTHCHECK")
    start = "\n".join(code_lines((inst / "start.sh").read_text()))
    if "uvicorn app.main:app" not in start:
        errors.append("start.sh does not start app.main:app with uvicorn")
    if "--reload" in start:
        errors.append("start.sh uses --reload")
    for error in errors:
        print(f"FAIL  {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
