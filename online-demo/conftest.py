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

from pathlib import Path

import pytest

from nrfupytesteos.conftest import *
from pyeapi.eapilib import ConnectionError


class NRFUconfig(object):
    """ for NRFU specific config / runtime """
    pass


def pytest_sessionstart(session):
    config = session.config

    # Store the instance of the Path to the test-case dir since we'll be using
    # it many times in each of the test function modules.

    config._nrfu = NRFUconfig()
    config._nrfu.testcases_dir = Path(config.option.nrfu_testcasedir).absolute()

    device_name = config.getoption("--nrfu-device")
    ssh_config_file = config.getoption('--ssh-config')
    dev = Device(device_name, ssh_config_file=ssh_config_file)

    # first probe IP/hostname of the device to ensure it is reachable.

    if not dev.probe():
        pytest.exit(f"Device unreachable, check --nrfu-device value: {device_name}.")

    # next try to run a show command to ensure the credentials are valid.

    try:
        dev.execute('show version')

    except Exception as exc:
        if isinstance(exc, ConnectionError):
            pytest.exit("Unable to access device.\nCheck you $EOS_USER and $EOS_PASSWORD env")

        pytest.exit(f"Unable to access device {device_name}: {str(exc)}")

    # I am now going to attach this device object to the session config data
    # since we have it, and we can then reference it for use by the device
    # fixture so we don't need to re-connect to the device a second time. ;-)

    config._nrfu.device = dev


@pytest.fixture(scope='session')
def device(request):
    """
    This fixture will be called once to return the existing Device instance
    that was setup in the session start hook function.
    """

    return request.config._nrfu.device
