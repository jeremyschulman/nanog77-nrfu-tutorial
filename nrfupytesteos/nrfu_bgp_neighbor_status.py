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
This file contains the NRFU test function for BGP neighbor status.

Examples - testcase
--------
   {
      "test-case": "test-bgp-neighbors",
      "dut": "ex000102.nyc1",
      "params": {
         "peer_ip": "192.168.255.1",
         "peer_device": "ex050301",
         "interface": "Vlan4094",
         "peer_asn": "30219",
         "peer_role": "mlag-peer",
         "bgp_type": "iBGP"
      },
      "expected": {
         "state": "up"
      }
   }


Examples - "show ip bpg summary"
--------
{
    "vrfs": {
        "default": {
            "routerId": "10.127.255.5",
            "peers": {
                "10.115.124.105": {
                    "description": "\"eBGP with rs32.sccs1-eth2-1\"",
                    "msgSent": 120528,
                    "inMsgQueue": 0,
                    "prefixReceived": 1864,
                    "upDownTime": 1569593053.967133,
                    "version": 4,
                    "msgReceived": 70456,
                    "prefixAccepted": 1864,
                    "peerState": "Established",
                    "outMsgQueue": 0,
                    "underMaintenance": false,
                    "asn": "64818"
                },
"""

from nrfupytesteos import nrfu_exc as exc

TEST_CASE = "test-bgp-neighbors"

# def make_testcase(dut, lag_name, interfaces):
#     return {
#         "test-case": TEST_CASE,
#         "dut": dut,
#         "params": {
#             "name": lag_name
#         },
#         "expected": {
#             "interfaces": interfaces
#         }
#     }
#
#
# def snapshot_testdata(device):
#     return device.execute('show lacp neighbor')


# def snapshot_testcases(device):
#     data = snapshot_testdata(device)
#     lags = data.get('portChannels')
#
#     return [
#         make_testcase(dut=device.hostname,
#                       lag_name=lag_name,
#                       interfaces=list(lag_data['interfaces']))
#         for lag_name, lag_data in lags.items()
#     ]


def name_test(item):
    """ used for pytest verbose output """
    p = item['params']
    return f"{p['peer_device']} role={p['role']} via={p['peer_ip']}"


def test_bgp_nei_status(device, actual, testcase):
    """
    Verifies the operational status of a BGP neighbor.

    Parameters
    ----------
    device: Device instance (unused)

    actual: dict
        The "show ip bgp summary" dataset

    testcase: dict
        The testcase dataset

    Returns
    -------
    True when the test passes

    Raises
    ------
    MissingError:
        When an expected BGP neighbor peer IP is missing

    MismatchError:
        When the BGP neighbor is not in the "up" status
    """
    peer_ip = testcase['params']['peer_ip']
    actual_peers = actual["vrfs"]['default']['peers']

    bgp_nei = actual_peers.get(peer_ip)
    if not bgp_nei:
        raise exc.MissingError(missing=bgp_nei)

    actual_state = bgp_nei["peerState"]
    if actual_state != 'Established':
        raise exc.MismatchError(expected="Established", actual=actual_state)

    return True
