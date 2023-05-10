import logging
import time

from TM1py import TM1Service
from pandas import DataFrame

from constants import TM1_PARAMS, FILE_NAME
from etl import Etl, EtlWithoutAsync
from setup import setup
from utils import configure_logging

if __name__ == "__main__":
    configure_logging("etl.log")
    runtimes = []

    # run for 40%, then 70%, then 100%
    for size in (0.4, 0.7, 1):

        num_records = setup(size)
        logging.info("Starting ETL")
        start = time.time()
        with TM1Service(**TM1_PARAMS) as tm1_conn:
            logging.info("Connected to TM1")
            etl = Etl(tm1_conn, FILE_NAME)
            etl.run()
            runtime = time.time() - start
            logging.info(f"Completed ETL in {runtime:.2f} seconds")
        runtimes.append(("TM1py", num_records, f"{runtime:.2f} sec"))

        num_records = setup(size)
        logging.info("Starting ETL without async")
        start = time.time()
        with TM1Service(**TM1_PARAMS) as tm1_conn:
            logging.info("Connected to TM1")

            etl = EtlWithoutAsync(tm1_conn, FILE_NAME)
            etl.run()
            runtime = time.time() - start
            logging.info(f"Completed ETL in {runtime:.2f} seconds")
        runtimes.append(("TM1py-without-async", num_records, f"{runtime:.2f} sec"))

        num_records = setup(size)
        with TM1Service(**TM1_PARAMS) as tm1_conn:
            start = time.time()
            logging.info("Starting ETL with pure TI")
            success, status, _ = tm1_conn.processes.execute_with_return(process_name="ETL")
            if success:
                runtime = time.time() - start
                logging.info(f"Completed ETL in {runtime:.2f} seconds")
                runtimes.append(("Pure-TI", num_records, f"{runtime:.2f} sec"))
            else:
                raise RuntimeError("Failed to execute TI process 'ETL'")

    stats = DataFrame(runtimes, columns=("Approach", "Records", "Runtime"))
    with open("results.csv", "w") as file:
        stats.to_csv(file, index=False)
    print(stats)
