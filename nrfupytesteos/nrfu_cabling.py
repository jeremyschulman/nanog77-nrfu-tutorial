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

"""
This file contains the NRFU test to verify the interface LLDP neighbor is as
epxected.


The test-case dictionary has the form (example):
   {
      "test-case": "test-cabling",
      "dut": "rs2105.dnvr1",
      "params": {
         "interface": "Ethernet49/1"
      },
      "expected": {
         "remote-hostname": "rs21.dnvr1",
         "remote-interface": "Ethernet3/1"
      }
   }

The EOS LLDP neighbor information is available from the "show lldp neighbors"
output in the 'interfacesStatuses' dict.  This dict has the form as shown
below.

Examples
--------
{
   "lldpNeighbors": [
      {
         "ttl": 120,
         "neighborDevice": "switch-21.bld1",
         "neighborPort": "Ethernet3/1",
         "port": "Ethernet49/1"
      },
      {
         "ttl": 120,
         "neighborDevice": "switch-22.bld1",
         "neighborPort": "Ethernet3/1",
         "port": "Ethernet50/1"
      },
      {
         "ttl": 120,
         "neighborDevice": "switch-2106.bld1",
         "neighborPort": "Ethernet59/1",
         "port": "Ethernet59/1"
      },
      {
         "ttl": 120,
         "neighborDevice": "switch-2106.bld1",
         "neighborPort": "Ethernet60/1",
         "port": "Ethernet60/1"
      }
   ]
}
"""

from first import first
from nrfupytesteos import nrfu_exc as exc

TEST_CASE_NAME = 'test-cabling'


def make_testcase(dut, interface, remote_host, remote_interface, role='role=na', **extra_params):
    tc = {
        "test-case": TEST_CASE_NAME,
        "dut": dut,
        "params": {
            "interface": interface,
            "role": role,
        },
        "expected": {
            "remote-hostname": remote_host,
            "remote-interface": remote_interface
        }
    }
    tc.update(**extra_params)
    return tc


def snapshot_testdata(device):
    return device.execute("show lldp neighbors")


def snapshot_testcases(device):
    data = snapshot_testdata(device)
    lldp_nbrs = data['lldpNeighbors']

    return [make_testcase(dut=device.hostname,
                          interface=entry['port'],
                          remote_host=entry['neighborDevice'],
                          remote_interface=entry['neighborPort'])
            for entry in lldp_nbrs]


def name_test(item):
    """ used for pytest verbose output """
    rmt_host = item['expected']['remote-hostname']
    rmt_ifn = item['expected']['remote-interface']
    return f"{item['params']['interface']}<[{item['params']['role']}]->{rmt_host}:{rmt_ifn}"


def test_cabling(device, actual, testcase):
    """
    This function will return a tuple (bool, str) to indicate
    if the testcase passes or fails.

    Parameters
    ----------
    device : Device instance (unused)
    actual : dict - EOS device lldp neighbors data (all interfaces)
    testcase : dict - testcase

    Returns
    -------
    True: when test case passes

    Raises
    -------
    MissingError:
        When the requested interface does not exist in the dataset

    MismatchError:
        When either no neighbor is found, or
        the wrong neighbor is found.
    """
    lldp_nbrs = actual['lldpNeighbors']
    if_name = testcase['params']['interface']

    lldp_if_nbr = first(nei for nei in lldp_nbrs if nei['port'] == if_name)
    if not lldp_if_nbr:
        raise exc.MissingError(
            f"Interface not found",
            missing=if_name)

    actual_rmt_dev = lldp_if_nbr['neighborDevice']
    actual_rmt_ifn = lldp_if_nbr['neighborPort']

    expect_rmt_dev = testcase['expected']['remote-hostname']
    expect_rmt_ifn = testcase['expected']['remote-interface']

    emsg = []

    if actual_rmt_dev.lower() != expect_rmt_dev.lower():
        emsg.append(f"Wrong remote-device: {actual_rmt_dev}")

    if actual_rmt_ifn.lower() != expect_rmt_ifn.lower():
        emsg.append(f"Wrong remote-interface: {actual_rmt_ifn}")

    if emsg:
        raise exc.MismatchError(
            ', '.join(emsg),
            expected=f"{expect_rmt_dev}:{expect_rmt_ifn}",
            actual=f"{actual_rmt_dev}:{actual_rmt_ifn}"
        )

    return True
