"""Instance settings.

Every value comes from the environment (see .env). Add fields here only for
what belongs to this instance alone.
"""

from ifdd.ts.core import CoreSettings


class Settings(CoreSettings):
    pass


settings = Settings()
