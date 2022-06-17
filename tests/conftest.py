from pathlib import Path
import os


os.environ["STAGE"] = "test"  # hardcode environment to test

_TEST_DIR = Path(__file__).parent
_MOCKS_DIR = _TEST_DIR / "mocks"
