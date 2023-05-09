import logging
import sys
from pathlib import Path


def configure_logging(log_file):
    """Configure logging to file and to console (stdout)"""

    logging.basicConfig(
        filename=Path(__file__).parent.joinpath(log_file),
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )

    # also log to stdout
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
