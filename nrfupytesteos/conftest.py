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

import pytest
from nrfupytesteos import Device

__all__ = [
    'pytest_addoption',
    'device',
    'Device'
]


def pytest_addoption(parser):
    parser.addoption("--nrfu-device",
                     required=True,
                     help='device name or IP address')

    parser.addoption("--nrfu-testcasedir",
                     required=True,
                     help='directory storing device test-case files')

    parser.addoption("--ssh-config", help='path to SSH config file')


@pytest.fixture(scope='session')
def device(request):
    device_name = request.config.getoption("--nrfu-device")
    ssh_config_file = request.config.getoption('--ssh-config')
    return Device(device_name, ssh_config_file=ssh_config_file)
