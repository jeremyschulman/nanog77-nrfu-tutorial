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
This file contains the NRFU test to verify the interface in the expected
administrative state and operational state.


The test-case dictionary has the form (example):
   {
      "test-case": "test-interface-status",
      "dut": "ex000102.nyc1",
      "params": {
         "interface": "Ethernet1",
         "role": "extern-inet"
      },
      "expected": {
         "state": "down"
      }
   }

The EOS interface information is available from the "show interfaces"
output. This dict has the form as shown below.

If the expected state is 'down', then the test should look for the 'linkStatus'
equal to 'disabled'

If the expected state is 'up', then the test should look for the 'linkStatus' equal
to "connected"

Examples
--------
{
    "interfaces": {
        "Ethernet10": {
            "interfaceStatistics": {
                "inBitsRate": 0.0,
                "inPktsRate": 0.0,
                "outBitsRate": 0.0,
                "updateInterval": 300.0,
                "outPktsRate": 0.0
            },
            "lanes": 0,
            "name": "Ethernet10",
            "interfaceStatus": "notconnect",
            "autoNegotiate": "off",
            "burnedInAddress": "74:83:ef:ed:66:67",
            "loopbackMode": "loopbackNone",
            "mtu": 10178,
            "hardware": "ethernet",
            "duplex": "duplexFull",
            "bandwidth": 10000000000,
            "forwardingModel": "dataLink",
            "lineProtocolStatus": "notPresent",
            "interfaceCounters": {
                "outBroadcastPkts": 0,
                "outUcastPkts": 0,
                "lastClear": 1562933487.5561786,
                "inMulticastPkts": 0,
                "counterRefreshTime": 1562940525.192617,
                "inBroadcastPkts": 0,
                "outputErrorsDetail": {
                    "deferredTransmissions": 0,
                    "txPause": 0,
                    "collisions": 0,
                    "lateCollisions": 0
                },
                "inOctets": 0,
                "outDiscards": 0,
                "outOctets": 0,
                "inUcastPkts": 0,
                "inTotalPkts": 0,
                "inputErrorsDetail": {
                    "runtFrames": 0,
                    "rxPause": 0,
                    "fcsErrors": 0,
                    "alignmentErrors": 0,
                    "giantFrames": 0,
                    "symbolErrors": 0
                },
                "linkStatusChanges": 0,
                "outMulticastPkts": 0,
                "totalInErrors": 0,
                "inDiscards": 0,
                "totalOutErrors": 0
            },
            "interfaceMembership": "Member of Port-Channel16",
            "interfaceAddress": [],
            "physicalAddress": "74:83:ef:ed:66:67",
            "description": "\"ob000101.nyc1-E51\""
        }
    }
}
"""



from nrfupytesteos import nrfu_exc as exc

TEST_CASE_NAME = "test-interface-status"


def make_testcase(dut, interface, state):
    return {
        "test-case": TEST_CASE_NAME,
        "dut": dut,
        "params": {
            "interface": interface
        },
        "expected": {
            "state": state
        }
    }


def snapshot_testdata(device):
    return device.execute('show interfaces')


def snapshot_testcases(device):
    data = snapshot_testdata(device)

    return [
        make_testcase(dut=device.hostname,
                      interface=if_name,
                      state=(
                          'up' if if_data['interfaceStatus'] == 'connected'
                          else 'down'))

        for if_name, if_data in data['interfaces'].items()
    ]


def name_test(item):
    """ used for pytest verbose output """
    return f"{item['params']['interface']}:{item['expected']['state']}"


def test_interface_status(device, actual, testcase):
    """
    This function will return a tuple (bool, str) to indicate
    if the testcase passes or fails.

    Parameters
    ----------
    device : Device instance

    actual : dict
        EOS device interfaces data as shown in the file comments

    testcase : dict - testcase


    Returns
    -------
    True: when testcase passes

    Raises
    ------
    MissingError:
        When the requested interface does not exist in the actual dataset

    MismatchError:
        When the interface is not the expected state (up/down)
    """
    status = actual['interfaces']
    if_name = testcase['params']['interface']
    if_status = status.get(if_name)

    if not if_status:
        raise exc.MissingError(
            'No status for interface',
            missing=if_name)

    actual_state = if_status['interfaceStatus']
    expected_state = testcase['expected']['state']

    # check expected down state condition

    if expected_state == 'down':
        if actual_state != 'disabled':
            raise exc.MismatchError(
                f'Interface {if_name} not down as expected',
                expected=expected_state,
                actual=actual_state
            )

        # if here, then interface is down as expected
        return True

    # check expected up state condition

    if actual_state != 'connected':
        raise exc.MismatchError(
            f'Interface {if_name} not up as expected',
            expected=expected_state,
            actual=actual_state
        )

    return True
