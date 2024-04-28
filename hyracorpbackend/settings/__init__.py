import environ
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))



if env("ENVIRONMENT") == "DEVELOPMENT":
    from .local import *
    from .base import *
elif env("ENVIRONMENT") == "PRODUCTION":
    from .production import *
    from .base import *