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
This file contains the network ready for use test for an MLAG interface status.

Examples - test case
--------
{
    "test-case": "test-mlag-interface-status",
    "dut": "rs2101.dnvr1",
    "params": {
        "mlag": "302",
        "interface": "Port-Channel302",
        "peer_interface": "Port-Channel302"
    },
    "expected": {
        "state": "up"
    }
}


Examples - "show mlag interfaces"
--------
{
    "interfaces": {
        "300": {
            "localInterface": "Port-Channel300",
            "peerInterface": "Port-Channel300",
            "peerInterfaceStatus": "down",
            "localInterfaceStatus": "down",
            "status": "inactive",
            "localInterfaceDescription": "MLB-DD201.MLB.ORG"
        },
"""

from nrfupytesteos import nrfu_exc as exc

TEST_CASE_NAME = "test-mlag-interface-status"


def make_testcase(dut, mlag, interface, peer_interface=None, state='up'):
    return {
        "test-case": TEST_CASE_NAME,
        "dut": dut,
        "params": {
            "mlag": mlag,
            "interface": interface,
            "peer_interface": peer_interface or interface
        },
        "expected": {
            "state": state
        }
    }


def snapshot_testdata(device):
    return device.execute('show mlag interfaces')


def snapshot_testcases(device):
    data = snapshot_testdata(device)
    mlag_interfaces = data.get('interfaces')

    return [
        make_testcase(dut=device.hostname,
                      mlag=mlag,
                      interface=mlag_data['localInterface'],
                      peer_interface=mlag_data['peerInterface'],
                      state=('up' if mlag_data['status'] == "active-full"
                             else 'down'))

        for mlag, mlag_data in mlag_interfaces.items()
    ]


def name_test(item):
    """ used for pytest verbose output """
    return f"{item['params']['mlag']}:{item['expected']['state']}"


def test_mlag_interface_status(device, actual, testcase):
    """
    Verifies the operational status of the MLAG interface.

    Parameters
    ----------
    device: Device instance
        (unused)

    actual: dict
        The result of the "show mlag interfaces" command

    testcase: dict
        The test case dataset

    Returns
    -------
    bool:
        `True` when the test passes, otherwise an exception is raised.

    Raises
    ------
    MissingError:
        When an expected MLAG  is missing

    MismatchError:
        When an MLAG is not in the expect "up" or "down" condition.
    """

    mlag_ifs = actual['interfaces']

    mlag = testcase['params']['mlag']
    mlag_ifstatus = mlag_ifs.get(mlag)

    if not mlag_ifstatus:
        raise exc.MissingError(
            f"MLAG {mlag} not found",
            missing=mlag)

    actual_state = mlag_ifstatus['status']
    expected_state = testcase['expected']['state']

    # check expected "up" condition

    if expected_state == 'up':
        if actual_state != 'active-full':
            raise exc.MismatchError(
                f'MLAG {mlag} not up as expected',
                expected=expected_state,
                actual=actual_state
            )

        # if here, then interface is down as expected
        return True

    # check expected up state condition

    if actual_state != 'inactive':
        raise exc.MismatchError(
            f'MLAG {mlag} not down as expected',
            expected=expected_state,
            actual=actual_state
        )

    return True
