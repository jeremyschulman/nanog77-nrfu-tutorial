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
This file contains the NRFU test function for LAG interfaces.  It ensures that only the interfaces
that are defined in the test case are actually present on the device.

Examples - testcase
--------
   {
      "test-case": "test-lag-status",
      "dut": "ob050301.nyc1",
      "params": {
         "name": "Port-Channel2000"
      },
      "expected": {
         "interfaces": [
            "Ethernet51",
            "Ethernet52"
         ]
      }
   }


Examples - "show lacp neighbor"
--------
{
    "portChannels": {
        "Port-Channel2000": {
            "interfaces": {
                "Ethernet51": {
                    "partnerPortPriority": 32768,
                    "partnerPortState": {
                        "collecting": true,
                        "distributing": true,
                        "synchronization": true,
                        "defaulted": false,
                        "timeout": false,
                        "activity": true,
                        "expired": false,
                        "aggregation": true
                    },
                    "partnerSystemId": "8000,76-83-ef-ed-66-5d",
                    "partnerOperKey": "0x000a",
                    "actorPortStatus": "bundled",
                    "partnerPortId": 15
                },
"""


from nrfupytesteos import nrfu_exc as exc

TEST_CASE_NAME = "test-lag-status"


def make_testcase(dut, lag_name, interfaces):
    return {
        "test-case": TEST_CASE_NAME,
        "dut": dut,
        "params": {
            "name": lag_name
        },
        "expected": {
            "interfaces": interfaces
        }
    }


def snapshot_testdata(device):
    return device.execute('show lacp neighbor')


def snapshot_testcases(device):
    data = snapshot_testdata(device)
    lags = data.get('portChannels')

    return [
        make_testcase(dut=device.hostname,
                      lag_name=lag_name,
                      interfaces=list(lag_data['interfaces']))
        for lag_name, lag_data in lags.items()
    ]


def name_test(item):
    """ used for pytest verbose output """
    return f"{item['params']['name']}"


def test_lag_status(device, actual, testcase):
    """
    Verifies the operational status of the LAG.

    Parameters
    ----------
    device: Device instance (unused)

    actual: dict
        The "show lacp neighbor" dataset

    testcase: dict
        The testcase dataset

    Returns
    -------
    True when the test passes

    Raises
    ------
    MissingError:
        When an expected interface is missing

    UnexpectedError:
        When an interface is present that does not belong

    MismatchError:
        When an interface is not in the "good" status
    """
    lag_name = testcase['params']['name']
    actual_lag = actual['portChannels'].get(lag_name)
    if not actual_lag:
        raise exc.MissingError(missing=lag_name)

    actual_if_names = set(actual_lag['interfaces'])
    exp_if_names = set(testcase['expected']['interfaces'])

    # first see if there are any missing interfaces,
    # if so raise a mismatch error.

    missing_if_names = exp_if_names - actual_if_names
    if missing_if_names:
        raise exc.MismatchError(
            expected=exp_if_names,
            actual=actual_if_names)

    # next check to see if there are any interfaces that should not be here

    unexp_if_names = actual_if_names - exp_if_names
    if unexp_if_names:
        raise exc.UnexpectedError(unexpected=unexp_if_names)

    # now for each interface, ensure that it is in the "good" state, which is
    # "bundled"

    if not actual_lag['interfaces']:
        raise exc.MismatchError(
            'No interfaces found in LAG',
            expected=exp_if_names,
            actual=""
        )

    for if_name, if_data in actual_lag['interfaces'].items():
        port_status = if_data["actorPortStatus"]
        if port_status != "bundled":
            raise exc.MismatchError(
                expected='bundled',
                actual=port_status
            )

    return True
