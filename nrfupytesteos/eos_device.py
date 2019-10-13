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

import os
import re

from first import first
from paramiko.config import SSHConfig
import pyeapi

__all__ = ['Device']

_if_shorten_find_patterns = [
    r'Ethernet(?P<E2>\d+)/1',
    r'Ethernet(?P<E1>\d+)',
    r'Management(?P<M1>\d+)',
    r'Port-Channel(?P<PO>\d+)',
    r'Vlan(?P<V>\d+)'
]

_if_shorten_replace_patterns = {
    'E1': 'E{}',
    'E2': 'E{}',
    'M1': 'M{}',
    'PO': 'Po{}',
    'V': 'V{}'
}

_if_shorten_regex = re.compile('|'.join('(%s)' % r for r in _if_shorten_find_patterns))


def _if_shorten_replace_func(mo):
    r_name, r_val = first(filter(lambda i: i[1], mo.groupdict().items()))
    return _if_shorten_replace_patterns[r_name].format(r_val)


def sorted_interfaces(if_list):
    match_numbers = re.compile(r"\d+", re.M)
    return sorted(if_list, key=lambda i: tuple(map(int, match_numbers.findall(i))))


class Device(object):
    """
    An Arista EOS Device class that provides access via the eAPI.
    """
    DEFAULT_TRANSPORT = 'https'

    def __init__(self, hostname, username=None, password=None,
                 transport=None, port=None,
                 ssh_config_file=None):

        self.hostname = hostname
        c_args = dict()

        c_args['username'] = os.getenv('EOS_USER') or os.getenv('USER') or username
        c_args['password'] = os.getenv('EOS_PASSWORD') or os.getenv('PASSWORD') or password

        if port:
            c_args['port'] = port

        ssh_config_file = ssh_config_file or os.getenv('EOS_SSH_CONFIG')
        if ssh_config_file:
            ssh_config = SSHConfig()
            ssh_config.parse(open(ssh_config_file))
            found = ssh_config.lookup(hostname)

            if 'user' in found:
                c_args['username'] = found['user']

            if 'hostname' in found:
                c_args['host'] = found['hostname']

            if 'localforward' in found:
                port = int(first(found['localforward']).split()[0])
                c_args['port'] = port
                c_args['host'] = 'localhost'

        else:
            c_args['host'] = hostname
            c_args['transport'] = transport or self.DEFAULT_TRANSPORT

        self.api = pyeapi.connect(**c_args)

    def probe(self, timeout=5):
        _orig_to = self.api.transport.timeout
        self.api.transport.timeout = timeout

        try:
            self.api.transport.connect()
            ok = True

        except Exception:
            ok = False

        finally:
            self.api.transport.timeout = _orig_to

        return ok

    def execute(self, command, encoding='json'):
        """
        Execute an operational command, "show version" for example.

        Parameters
        ----------
        command : str - command to execute

        encoding : str
            The return format encoding, defaults to 'json'.

        Returns
        -------
        dict - results of the command
        """
        res = self.api.execute(['enable', command], encoding=encoding)
        return res['result'][1]

    @staticmethod
    def shorten_if_name(if_name):
        return _if_shorten_regex.sub(_if_shorten_replace_func, if_name)
