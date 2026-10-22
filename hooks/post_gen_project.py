"""After generation: create .env from dotenv.dist (mode 0600).

The API has no secret of its own: it only checks tokens. An existing .env is
left alone, so running the hook again (cruft update renders into a temporary
directory) never replaces local values.
"""

import os
import shutil
from pathlib import Path

root = Path.cwd()
env = root / ".env"
if not env.exists():
    shutil.copyfile(root / "dotenv.dist", env)
    os.chmod(env, 0o600)
