import csv
import random
from pathlib import Path

import pandas as pd
from TM1py import TM1Service, Dimension, Hierarchy, Cube, ElementAttribute, Process

from constants import TM1_PARAMS, CUBE_NAME, YEARS, MONTHS, VERSIONS, REGIONS, PRODUCTS, CUSTOMERS, MEASURES, \
    DIMENSION_NAMES, DIMENSION_BATTLE_CUSTOMER, DIMENSION_BATTLE_REGION, DIMENSION_BATTLE_PRODUCT, CITIES, \
    DIMENSION_BATTLE_CITY

MDX = """
    SELECT 
  NON EMPTY 
   {[Battle Cube Measure].[Battle Cube Measure].Members}  
  ON COLUMNS , 
  NON EMPTY 
   {[Battle Customer].[Battle Customer].Members}  
  ON ROWS 
FROM [Battle Cube] 
WHERE 
  (
   [Battle Year].[Battle Year].[Total Battle Year],
   [Battle Month].[Battle Month].[Total Battle Month],
   [Battle Version].[Battle Version].[Total Battle Version],
   [Battle Region].[Battle Region].[Total Battle Region],
   [Battle Product].[Battle Product].[Total Battle Product]
  )
    """


def setup():
    with TM1Service(**TM1_PARAMS) as tm1:
        # create ETL process
        with open("process.json", "r") as file:
            process = Process.from_json(file.read())
        tm1.processes.update_or_create(process)

        if tm1.cubes.exists(CUBE_NAME):
            tm1.cubes.delete(CUBE_NAME)
        build_main_cube(tm1)

        build_city_dimension(tm1)

        # execute dummy MDX to avoid locking on first request
        tm1.cells.execute_mdx_cellcount(MDX)


def build_city_dimension(tm1):
    create_dimension(tm1, DIMENSION_BATTLE_CITY, CITIES)
    tm1.elements.add_element_attributes(
        dimension_name=DIMENSION_BATTLE_CITY,
        hierarchy_name=DIMENSION_BATTLE_CITY,
        element_attributes=[ElementAttribute(name="Region", attribute_type="String")])

    cells = {
        ("Munich", "Region"): "DE",
        ("Gent", "Region"): "BE",
        ("Amsterdam", "Region"): "NL",
        ("Zurich", "Region"): "CH",
        ("Vienna", "Region"): "AU",
    }
    tm1.cells.write("}ElementAttributes_" + DIMENSION_BATTLE_CITY, cells)


def build_main_cube(tm1):
    records = [DIMENSION_NAMES + ["Value"]]
    # create csv
    for year in YEARS:
        for month in MONTHS:
            for version in VERSIONS:
                for city in CITIES:
                    for product in PRODUCTS:
                        for customer in CUSTOMERS:
                            for measure in MEASURES:
                                record = [year, month, version, city, product, customer, measure, '1']
                                records.append(record)

    # write local data.csv
    with open("data.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(records)

    # write data.csv for TI in C:/temp/data.csv
    path = Path("C:/temp/data.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(records)

    df = pd.read_csv("data.csv", dtype={dimension_name: str for dimension_name in DIMENSION_NAMES})

    for dimension_name in DIMENSION_NAMES:
        if dimension_name == DIMENSION_BATTLE_REGION:
            create_dimension(tm1, dimension_name, REGIONS)
        else:
            element_names = df[dimension_name].unique().astype(str)
            create_dimension(tm1, dimension_name, element_names)

    # create cube
    cube = Cube(CUBE_NAME, DIMENSION_NAMES)
    tm1.cubes.create(cube)

    # delete some elements in each dimension
    for customer in random.sample(CUSTOMERS, 10):
        tm1.elements.delete(DIMENSION_BATTLE_CUSTOMER, DIMENSION_BATTLE_CUSTOMER, customer)

    for product in random.sample(PRODUCTS, 2):
        tm1.elements.delete(DIMENSION_BATTLE_PRODUCT, DIMENSION_BATTLE_PRODUCT, product)


def create_dimension(tm1, dimension_name, element_names):
    if tm1.dimensions.exists(dimension_name):
        tm1.dimensions.delete(dimension_name)

    hierarchy = Hierarchy(name=dimension_name, dimension_name=dimension_name)
    total = "Total " + dimension_name
    hierarchy.add_element(total, "Consolidated")
    for year in element_names:
        hierarchy.add_component(parent_name=total, component_name=year, weight=1)
    dimension = Dimension(name=dimension_name, hierarchies=[hierarchy])
    tm1.dimensions.create(dimension)


if __name__ == "__main__":
    setup()
