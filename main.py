import logging
import time

from TM1py import TM1Service

from constants import TM1_PARAMS
from etl import Etl, EtlWithoutAsync
from setup import setup
from utils import configure_logging

if __name__ == "__main__":
    configure_logging("etl.log")

    setup()
    logging.info("Starting ETL")
    start = time.time()
    with TM1Service(**TM1_PARAMS) as tm1_conn:
        logging.info("Connected to TM1")
        etl = Etl(tm1_conn, "data.csv")
        etl.run()
        logging.info(f"Completed ETL in {time.time() - start:.2f} seconds")

    setup()
    logging.info("Starting ETL without async")
    start = time.time()
    with TM1Service(**TM1_PARAMS) as tm1_conn:
        logging.info("Connected to TM1")

        etl = EtlWithoutAsync(tm1_conn, "data.csv")
        etl.run()

        logging.info(f"Completed ETL without async in {time.time() - start:.2f} seconds")

    setup()
    with TM1Service(**TM1_PARAMS) as tm1_conn:
        start = time.time()
        logging.info("Starting ETL with pure TI")
        success, status, _ = tm1_conn.processes.execute_with_return(process_name="ETL")
        if success:
            logging.info(f"Completed ETL with pure TI in {time.time() - start:.2f} seconds")
        else:
            raise RuntimeError("Failed to execute TI process 'ETL'")
