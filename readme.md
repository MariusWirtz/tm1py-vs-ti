Performance comparison of TM1Py and TI in a realistic ETL scenario

### Setup

1. adjust `TM1_PARAMS` variable in `constants.py`
2. run `main.py`
3. compare runtime of each run in `results.csv`

Expected results

| Approach            |Records| Runtime    |
|---------------------|-------|------------|
| TM1py               |1589760| 21.79 sec  |
| TM1py-without-async |1589760| 76.03 sec  |
| Pure-TI             |1589760| 75.74 sec  |
| TM1py               |2737920| 34.13 sec  |
| TM1py-without-async |2737920| 128.52 sec |
| Pure-TI             |2737920| 131.68 sec |
| TM1py               |3974400| 48.68 sec  |
| TM1py-without-async |3974400| 184.56 sec |
| Pure-TI             |3974400| 195.58 sec |