#!/bin/bash

set -x
device=$1
shift

pytest -v --tb=no \
    --nrfu-device ${device} \
    --nrfu-testcasedir ${device}-testcases \
    --html reports/${device}.html \
    --self-contained-html \
    "$@"
