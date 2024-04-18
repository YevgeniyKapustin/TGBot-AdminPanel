import sys
from pathlib import Path

from dotenv import load_dotenv

from src.config import Config

load_dotenv()
config: Config = Config()
sys.path.append(str(Path(sys.path[0]).joinpath('..')))
