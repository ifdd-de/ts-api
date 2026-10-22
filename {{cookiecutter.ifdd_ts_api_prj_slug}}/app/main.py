"""Application entry point: the API of ifdd-ts-core with the settings of this instance."""

from ifdd.ts.core import create_app

from app.settings import settings

app = create_app(settings)
