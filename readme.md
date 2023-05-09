### Setup

Performance comparison of TM1Py and TI in a realistic ETL scenario

1. adjust `TM1_PARAMS` variable in `constants.py`
2. run `main.py`
3. compare runtime of each run in `etl.log`

Expected results

|                         | Run Time |
|-------------------------------|-------|
|Turbo Integrator                             |186.28 sec |
|TM1Py                          |63.41 sec |
|TM1Py _(without async)_          |180.69 sec |