#!/bin/bash

cd ~/pi_projects/raspberrypi_projects/price_tracker

. ./price_tracker_python_env/bin/activate

python3 ~/pi_projects/raspberrypi_projects/price_tracker/src/main.py

deactivate
