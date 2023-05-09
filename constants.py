DIMENSION_BATTLE_CUBE_MEASURE = "Battle Cube Measure"
DIMENSION_BATTLE_CUSTOMER = "Battle Customer"
DIMENSION_BATTLE_PRODUCT = "Battle Product"
DIMENSION_BATTLE_REGION = "Battle Region"
DIMENSION_BATTLE_VERSION = "Battle Version"
DIMENSION_BATTLE_MONTH = "Battle Month"
DIMENSION_BATTLE_YEAR = "Battle Year"
DIMENSION_BATTLE_CITY = "Battle City"

CUBE_NAME = "Battle Cube"
DIMENSION_NAMES = [
    DIMENSION_BATTLE_YEAR,
    DIMENSION_BATTLE_MONTH,
    DIMENSION_BATTLE_VERSION,
    DIMENSION_BATTLE_REGION,
    DIMENSION_BATTLE_PRODUCT,
    DIMENSION_BATTLE_CUSTOMER,
    DIMENSION_BATTLE_CUBE_MEASURE]

YEARS = [str(year) for year in range(2000, 2023)]
MONTHS = [str(y).zfill(2) for y in range(1, 13, 1)]
VERSIONS = ["Actual", "Budget"]
REGIONS = ["DE", "CH", "AU", "BE", "NL"]
PRODUCTS = [
    "Arteon",
    "Caddy",
    "Jetta",
    "Passat",
    "Golf",
    "Golf GTI",
    "Golf R",
    "Atlas",
    "Atlas Cross Sport",
    "Taos",
    "T4",
    "Tiguan",
    "Beetle",
    "Golf SportWagen",
    "Golf Alltrack",
    "ID.4"
]
CITIES = [
    "Munich",
    "Gent",
    "Amsterdam",
    "Zurich",
    "Vienna",
]
CUSTOMERS = [
    "CarMax",
    "AutoNation",
    "Gran Turino",
    "Carvana",
    "Europcar"
    "Enterprise Car Sales",
    "Carmax Autocare Center",
    "CarZone USA",
    "CarZone UK",
    "DriveTime",
    "CarTime",
    "Hertz Car Sales",
    "Sixt",
    "Penske Automotive Group",
    "Sonic Automotive"
    "Vroom",
    "Top Gear",
    "Zoom",
    "TrueCar",
    "GoodCar",
    "Shift",
    "CarSense",
    "CarPooling",
    "CarSoup",
    "Off Lease Only",
    "EchoPark Automotive",
    "Auto Lenders",
    "Auto Stars",
    "CarGurus",
    "The STIG",
    "SwissCar",
    "All The Best Cars",
    "SwissAuto",
    "CarNation",
    "I Can Car",
    "Bentley Cars",
    "The GRID",
    "Cars Cars Cars",
    "SuperCar",
    "Fiat 5000",
    "Edmunds",
    "Auto Time",
    "Car Patrol",
    "Fast Cars",
    "Shiny Cars",
    "Tiny Cars",
    "Real Cars",
]
MEASURES = ["Quantity", "Revenue"]

TM1_PARAMS = {
    "address": "",
    "port": 8010,
    "ssl": True,
    "user": "Admin",
    "password": "apple"
}
