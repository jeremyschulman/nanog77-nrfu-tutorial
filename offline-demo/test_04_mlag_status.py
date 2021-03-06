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
load NRFU MLAG test-cases based on the --nrfu-testcasedir command line option.
This file retrieves the device specific "show" output from a file rather than
an actual device to support a dev-demo environment.
"""

import json
import pytest

# import the EOS specific NRFU MLAG status module so the functions in this file
# can generate the test-case names and invoke the actual NRFU validation
# function.

from nrfupytesteos import nrfu_mlag_status as nrfu


@pytest.fixture(scope='module')
def device_mlag_status(device):
    """
    This fixture is used to return the EOS result of the 'show mlag' command as
    structured data.

    Rather than running the specific EOS show command, we are going to load the
    previously captured output.  For a real-world example, see the file
    `online-demo/test_04_mlag_status.py`.

    Parameters
    ----------
    device : Device instance

    Returns
    -------
    dict
        The dictionary output of the 'show mlag' command that was retrieve from
        a file rather than the device.
    """
    show_file = device.show_outputs_dir.joinpath(
         'show-mlag.json')

    return json.load(show_file.open())


def pytest_generate_tests(metafunc):
    """
    pytest will invoke this hook allowing us to dynamically load the device
    specific MLAG test cases based on the directory the User provided as the
    --nrfu-testcasedir command line argument.

    Parameters
    ----------
    metafunc : Metafunc instance used to parametrize the test function
    """

    testcases_file = metafunc.config._nrfu['testcase_dir'].joinpath(
        'testcases-mlag-status.json')

    metafunc.parametrize('testcase',
                         json.load(testcases_file.open()),
                         ids=nrfu.name_test)


def test_mlag_status(device, device_mlag_status, testcase):
    """
    pytest will call this function for each test-case item loaded via the
    pytest_generate_tests hook function.  This function will in turn call the
    actual NRFU EOS specific test function `nrfu.test_mlag_status` that will
    validate the specific `testcase` against the actual data
    `device_mlag_status`.  If `nrfu.test_mlag_status` detects a failure it will
    raise a specific NRFU exception.  The pytest framework will catch that
    exception and report the test as failed.

    Parameters
    ----------
    device : Device instance

    device_mlag_status : dict
        The EOS structured output of the 'show mlag' command

    testcase : dict
        A specific test-case from the list of all test-cases loaded.

    Raises
    ------
    See `nrfu.test_mlag_status` docs for details
    """
    nrfu.test_mlag_status(device=device, actual=device_mlag_status,
                          testcase=testcase)
