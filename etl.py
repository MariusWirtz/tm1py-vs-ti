import logging
import time

import pandas as pd
from TM1py import TM1Service, Element

from constants import TM1_PARAMS, CUBE_NAME, DIMENSION_NAMES, DIMENSION_BATTLE_CUBE_MEASURE, DIMENSION_BATTLE_CUSTOMER, \
    DIMENSION_BATTLE_PRODUCT, DIMENSION_BATTLE_CITY
from utils import configure_logging


class Etl:

    def __init__(self, tm1, file_name):
        self.tm1 = tm1
        self.file_name = file_name

    def run(self):
        df = self._extract()
        logging.info(f"Completed reading CSV with shape: {df.shape}")

        df = self._transform(df)
        logging.info("Completed Transformation")

        self._load_metadata(df)
        logging.info("Completed Dimension Updates")

        self._clear()
        logging.info("Completed Clear")

        self._load_data(df)
        logging.info("Completed Write")

    def _load_data(self, df):
        self.tm1.cells.write_dataframe_async(CUBE_NAME, df, slice_size_of_dataframe=400_000)

    def _clear(self):
        self.tm1.processes.execute_ti_code(lines_prolog=[f"CubeClearData('{CUBE_NAME}');"])

    def _load_metadata(self, df):
        existing_customers = set(
            self.tm1.elements.get_element_names(DIMENSION_BATTLE_CUSTOMER, DIMENSION_BATTLE_CUSTOMER))
        self.add_elements(
            dimension_name=DIMENSION_BATTLE_CUSTOMER,
            elements=set(df[DIMENSION_BATTLE_CUSTOMER].unique()) - existing_customers)

        existing_products = set(self.tm1.elements.get_element_names(DIMENSION_BATTLE_PRODUCT, DIMENSION_BATTLE_PRODUCT))
        self.add_elements(
            dimension_name=DIMENSION_BATTLE_PRODUCT,
            elements=set(df[DIMENSION_BATTLE_PRODUCT].unique()) - existing_products)

    def _transform(self, df):
        # substitute values according to lookup cube
        lookups = self.retrieve_lookups()
        df["Battle Region"] = df["Battle Region"].replace(lookups)

        # conditional multiplication
        df.loc[
            df[DIMENSION_BATTLE_CUBE_MEASURE] == 'Revenue',
            ['Value']] *= 1000

        return df

    def _extract(self):
        df = pd.read_csv(
            filepath_or_buffer=self.file_name,
            dtype={dimension_name: str for dimension_name in DIMENSION_NAMES})

        return df

    def add_elements(self, dimension_name, elements):
        logging.info(f"Adding {len(elements)} elements to dimension {dimension_name}")

        self.tm1.elements.add_elements(
            dimension_name=dimension_name,
            hierarchy_name=dimension_name,
            elements=[
                Element(elem, "Numeric")
                for elem
                in elements])

        self.tm1.elements.add_edges(
            dimension_name=dimension_name,
            hierarchy_name=dimension_name,
            edges={
                ("Total " + dimension_name, elem): 1
                for elem
                in elements})

    def retrieve_lookups(self):
        return self.tm1.elements.get_attribute_of_elements(
            dimension_name=DIMENSION_BATTLE_CITY,
            hierarchy_name=DIMENSION_BATTLE_CITY,
            attribute="Region")


class EtlWithoutAsync(Etl):

    def _load_data(self, df):
        self.tm1.cells.write_dataframe(CUBE_NAME, df, use_blob=True)

