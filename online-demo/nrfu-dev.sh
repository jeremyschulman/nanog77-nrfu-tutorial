#!/bin/bash

hostname=$1
shift
set -x

pytest -v --tb=no \
    --html=${hostname}/report.html --self-contained-html \
    --nrfu-device ${hostname} \
    --nrfu-testcasedir ${hostname} "$@"
