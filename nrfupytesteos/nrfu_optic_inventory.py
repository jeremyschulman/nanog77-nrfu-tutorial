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
This file contains the NRFU test to verify the optic inventory information for
a given interface.

The test-case dictionary has the form (example):

   {
      "test-case": "test-optic-inventory",
      "dut": "ex000102.nyc1",
      "params": {
         "interface": "Ethernet1",
         "role": "extern-inet"
      },
      "expected": {
         "optic": "SFP-10G-LR-P"
      }
   }

If no optic is expected, then set the `optic` value to the empty-string ('').

The EOS transceiver inventory information is available from the "show
inventory" output in the 'xcvrSlots' dict.  This dict has the form:

    key: str - <port-number>
    val: dict as shown in examples below


Examples
--------
    "56": {
        "modelName": "",                        # <-- no optic present in interface
        "serialNum": "",
        "mfgName": "Not Present",
        "hardwareRev": ""
    }

    "60": {
        "modelName": "QSFP28-LR4-100G",
        "serialNum": "G1807348871",
        "mfgName": "Arista Networks",
        "hardwareRev": "01"
    }
"""



from nrfupytesteos import nrfu_exc as exc

TEST_CASE_NAME = "test-optic-inventory"


def make_testcase(dut, interface, optic):
    return {
        "test-case": TEST_CASE_NAME,
        "dut": dut,
        "params": {
            "interface": interface
        },
        "expected": {
            "optic": optic or ''
        }
    }


def snapshot_testdata(device):
    return device.execute('show inventory')


def snapshot_testcases(device):
    data = snapshot_testdata(device)

    xcvrs = data['xcvrSlots']
    return [
        make_testcase(dut=device.hostname,
                      interface=port_num,
                      optic=port_data['modelName'])
        for port_num, port_data in xcvrs.items()
    ]


def name_test(item):
    """ used for pytest verbose output """
    return f"{item['params']['interface']}:{item['expected']['optic'] or 'none'}"


def test_optic_inventory(device, actual, testcase):
    """
    This test will verify that the given interface has the optic type as expected.
    If no optic is expected in the interface, then the test-case data should have
    the expected optic value set to empty-string.

    Parameters
    ----------
    device : Device instance

    actual : dict
        output of "show inventory" command

    testcase : dict
        test case data

    Returns
    -------
    True when test case passes

    Raises
    -------
    MissingError:
        When requested interface does not show up in the inventory dataset.

    MismatchError:
        - When optic found does not match expected value.
    """
    xcvrs = actual['xcvrSlots']
    if_name = testcase['params']['interface']
    port_no = device.shorten_if_name(if_name).split('E')[-1]

    xcvr_data = xcvrs.get(port_no)
    if not xcvr_data:
        raise exc.MissingError(
            "Interface not found",
            missing=if_name)

    expect_model = testcase['expected']['optic']
    actual_model = xcvr_data['modelName']

    if actual_model == expect_model:
        return True

    # if here then there is a mismatch.  if expecting an optic then the error
    # message should indicate that the wrong optic is present and if an optic
    # is not expected, then the error message should indicate that no optic was
    # expected.  We don't use an Unexpected exception here because that is
    # meant to server as 'unexpected additional information'

    wrong = "Wrong" if actual_model else "No"
    err_msg = (f"{wrong} optic found on interface {if_name}" if expect_model
               else f"No optic expected, but found on interface {if_name}")

    raise exc.MismatchError(
        err_msg,
        actual=actual_model,
        expected=expect_model)
