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
This file is used to validate the operational state of the MLAG control protocol.  The actual
status is obtained from the "show mlag" command (see example JSON output below).  For this test-case
to succeed, we will check both the state is "active" and the negotiated status is "connected".

Examples - Test case
--------
   {
      "test-case": "test-mlag-status",
      "dut": "lf5e1b01.nyc1",
      "params": {
         "peer_link": "Port-Channel2000",
         "peer_ip": "10.127.253.117",
         "vlan_name": "MLAG_CTRLVLAN",
         "vlan_id": 4094,
         "vlan_ipif": "10.127.253.116/31"
      },
      "expected": {
         "state": "up"
      }
   }

Examples - "show mlag"
--------
{
   "localInterface": "Vlan4094",
   "systemId": "76:83:ef:ed:66:5d",
   "domainId": "MLAG_CTRLVLAN",
   "peerLink": "Port-Channel2000",
   "dualPrimaryDetectionState": "disabled",
   "localIntfStatus": "up",
   "peerLinkStatus": "up",
   "peerAddress": "192.168.255.2",
   "configSanity": "consistent",
   "portsErrdisabled": false,
   "state": "active",
   "reloadDelay": 600,
   "reloadDelayNonMlag": 600,
   "negStatus": "connected",
   "mlagPorts": {
      "Disabled": 0,
      "Active-partial": 0,
      "Inactive": 18,
      "Configured": 0,
      "Active-full": 1
   }
}

"""

from nrfupytesteos import nrfu_exc as exc

TEST_CASE_NAME = "test-mlag-status"


def make_testcase(dut, domain, interface, peer_link, peer_ip):
    return {
        "test-case": TEST_CASE_NAME,
        "dut": dut,
        "params": {
            "interface": interface,
            "peer_link": peer_link,
            "peer_ip": peer_ip,
            "domain": domain,
        },
        "expected": {
            "state": "up"
        }
    }


def snapshot_testdata(device):
    return device.execute("show mlag")


def snapshot_testcases(device):
    data = snapshot_testdata(device)

    if data['state'] == 'disabled':
        return []

    return [make_testcase(
        dut=device.hostname,
        domain=data['domainId'],
        interface=data['localInterface'],
        peer_link=data['peerLink'],
        peer_ip=data['peerAddress']
    )]


def name_test(item):
    """ used for pytest verbose output """
    return f"{item['params']['peer_link']}"


def test_mlag_status(device, actual, testcase):
    """
    Verify MLAG control protocol operational status. This test only verifies that
    the MLAG control plane is active/connected.

    TODO: add support to check the status to be expected in a down condition.

    Parameters
    ----------
    device : Device instance (unused)
    actual : dict - EOS device mlag status
    testcase : dict - testcase

    Raises
    -------
    MismatchError:
        When the MLAG control plane status is not active/connected.

    Returns
    -------
    True: when testcase passes
    """
    has_state = actual['state']
    exp_state = testcase['expected']['state']

    is_up = (exp_state == 'up' and has_state == 'active')
    has_neg_st = actual['negStatus']
    is_neg = has_neg_st == "connected"

    if is_up and is_neg:
        return True

    raise exc.MismatchError(
        expected=('active', 'connected'),
        actual=(has_state, has_neg_st)
    )
