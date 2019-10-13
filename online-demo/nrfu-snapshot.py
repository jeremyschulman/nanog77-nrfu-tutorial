#!/usr/bin/env python

#  Copyright 2019 Jeremy Schulman, nwkautomaniac@gmail.com
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys
from pathlib import Path
import json

from nrfupytesteos import (
    Device,
    nrfu_cabling,
    nrfu_lag_status,
    nrfu_interface_status,
    nrfu_optic_inventory,
    nrfu_mlag_status,
    nrfu_mlag_interface_status
)


try:
    dev = Device(hostname=sys.argv[1])

except IndexError:
    sys.exit("Missing hostname")


assert dev.probe(), f"Unable to reach {dev.hostname}, exit."

snapshot_list = [
    nrfu_cabling,
    nrfu_lag_status,
    nrfu_interface_status,
    nrfu_optic_inventory,
    nrfu_mlag_status,
    nrfu_mlag_interface_status
]


def snapshot():
    snapshot_dir = Path.cwd() / dev.hostname

    print(f"Ensure directory: {snapshot_dir.name}")
    snapshot_dir.mkdir(exist_ok=True)

    for nrfu in snapshot_list:
        testcases = nrfu.snapshot_testcases(dev)
        if not testcases:
            print(f"\t[-] {nrfu.TEST_CASE_NAME} skipping, no test-cases")
            continue

        tc_file = snapshot_dir / f'{nrfu.TEST_CASE_NAME}.json'
        print(f"\t[+] {nrfu.TEST_CASE_NAME} creating {len(testcases)} test-cases")
        json.dump(testcases, tc_file.open('w+'), indent=3)


if __name__ == "__main__":
    snapshot()
