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
This file provides the pytest framework and test functions used to dynamically
load NRFU MLAG interface status  test-cases based on the --nrfu-testcasedir
command line option. This file retrieves the device specific "show" output
directly from the device.
"""

# import the EOS specific NRFU MLAG interface status module so the functions in
# this file can generate the test-case names and invoke the actual NRFU
# validation function.

import json
import pytest

# import the EOS specific NRFU MLAG interface status module so the functions in
# this file can generate the test-case names and invoke the actual NRFU
# validation function.

import nrfupytesteos.nrfu_mlag_interface_status as nrfu


@pytest.fixture(scope='module')
def device_mlag_interfaces_status(device):
    """
    This fixture is used to return the EOS result of the 'show mlag interfaces'
    command as structured data.

    Parameters
    ----------
    device : Device instance

    Returns
    -------
    dict
        The dictionary output of the 'show mlag interfaces' command
    """
    return nrfu.snapshot_testdata(device)


def pytest_generate_tests(metafunc):
    """
    pytest will invoke this hook allowing us to dynamically load the device
    specific MLAG interface status test cases based on the directory the User
    provided as the --nrfu-testcasedir command line argument.

    Parameters
    ----------
    metafunc : Metafunc instance used to parametrize the test function
    """
    testcases_file = metafunc.config._nrfu.testcases_dir.joinpath(
        f'{nrfu.TEST_CASE_NAME}.json')

    if not testcases_file.exists():
        metafunc.parametrize('testcase', [], ids=['no-tests'])
        return

    metafunc.parametrize('testcase',
                         json.load(testcases_file.open()),
                         ids=nrfu.name_test)

def test_mlag_interface_status(device, device_mlag_interfaces_status, testcase):
    """
    pytest will call this function for each test-case item loaded via the
    pytest_generate_tests hook function.  This function will in turn call the
    actual NRFU EOS specific test function `nrfu.test_mlag_interface_status`
    that will validate the specific `testcase` against the actual data
    `device_mlag_interfaces_status`.  If `nrfu.test_mlag_interface_status`
    detects a failure it will raise a specific NRFU exception.  The pytest
    framework will catch that exception and report the test as failed.

    Parameters
    ----------
    device : Device instance

    device_mlag_interfaces_status : dict
        The EOS structured output of the 'show mlag interfaces' command

    testcase : dict
        A specific test-case from the list of all test-cases loaded.

    Raises
    ------
    See `nrfu.test_mlag_interface_status` docs for details
    """
    nrfu.test_mlag_interface_status(
        device=device,
        actual=device_mlag_interfaces_status,
        testcase=testcase)
