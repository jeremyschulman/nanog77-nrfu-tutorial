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
For the purpose of demonstration and testing, we are NOT going to talk directly
to a device, but rather use captured device output so that we are not dependent
upon having live device connectivity.  For our demonstration, we will have a
device called "dev1" and the show outputs will be stored in a directory called
"dev1-show-outputs".  The test-cases for this device will be stored in a
directory called "dev1-testcases".
"""
from pathlib import Path

import pytest

from nrfupytesteos import Device

# import the pytest_addoption from the package so we pickup the pytest options
# for NRFU.  The `pytest_addoption` function needs to be scoped in this file in
# order for the pytest commandline to use the --nrfu options.

from nrfupytesteos.conftest import pytest_addoption  # noqa


def pytest_sessionstart(session):
    """
    pytest hook function called at the start of the session processing & after
    the command line arguments have been processed.

    Normally when a session starts we would attempt to connect to the device
    and verify that we can reach it.  See the `online-demo/conftest.py` for
    performing that action with EOS.  For the purposes of demonstration, we are
    going to store Path variables to the directories we will need in order to
    obtain the demo "show" output and the test-cases

    Parameters
    ----------
    session : Session - pytest Session instance
    """
    cfg_opts = session.config.option

    session.config._nrfu = dict(
        show_outputs_dir=Path.cwd().joinpath(cfg_opts.nrfu_device + "-show-outputs"),
        testcase_dir=Path(cfg_opts.nrfu_testcasedir).absolute()
    )


@pytest.fixture(scope='session')
def device(pytestconfig):
    """
    Normally when we want the device instance we would create a pyEapi session
    and return it; see the `online-demo/conftest.py` for real-world use.  Since we
    are using captured show output data, we are going to instead add a variable
    to the Device instance so that the test functions can use it to load the
    fake data.

    Parameters
    ----------
    pytestconfig : Config - the pytest Config instance

    Returns
    -------
    Device
        The device instance that will be used by the test functions
    """
    device_name = pytestconfig.option.nrfu_device
    dev = Device(device_name)
    dev.show_outputs_dir = pytestconfig._nrfu['show_outputs_dir']
    return dev
