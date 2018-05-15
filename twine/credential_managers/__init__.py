# Copyright 2018 Matt Bullock
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Credential managers provide hooks to obtain credential
values. Every method accepts guidance from the CLI arguments
and the pypirc configuration, but no credential manager
is obligated to use any information from them.
"""
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

import abc
import pkg_resources

import six


def load_credential_manager(name):
    """Load a registered credential manager identified by the provided name."""
    manager_loader = _registered_credential_managers()[name]
    manager = manager_loader.load()
    return manager()


def _registered_credential_managers():
    """Locate all registered credential managers."""
    registered_credential_managers = pkg_resources.iter_entry_points(group='twine.credentials')
    credential_managers = {}
    for manager in registered_credential_managers:
        if manager.name in credential_managers:
            raise ImportError('Multiple credential managers located for the name "{name}": "{existing}" and "{new}"'.format(
                name=manager.name,
                existing=credential_managers[manager.name].dist,
                new=manager.dist
            ))
        credential_managers[manager.name] = manager
    return credential_managers


@six.add_metaclass(abc.ABCMeta)
class CredentialManager(object):
    """Interface for credential managers."""

    @abc.abstractmethod
    def get_password(self, system, username, cli_value, config, interactive):
        """Get a password from keyring.

        :param str system: Package index URL
        :param str username: Known username
        :param str cli_value: Value obtained from the CLI arguments
        :param dict config: Existing configuration from pypirc
        :param bool interactive: Should this operations accept user input?
        """

    @abc.abstractmethod
    def get_username(self, system, cli_value, config, interactive):
        """Get a username from keyring.

        :param str system: Package index URL
        :param str cli_value: Value obtained from the CLI arguments
        :param dict config: Existing configuration from pypirc
        :param bool interactive: Should this operations accept user input?
        """

    @abc.abstractmethod
    def get_cacert(self, system, username, cli_value, config, interactive):
        """Get a CA certificate from keyring.

        :param str system: Package index URL
        :param str username: Known username
        :param str cli_value: Value obtained from the CLI arguments
        :param dict config: Existing configuration from pypirc
        :param bool interactive: Should this operations accept user input?
        """

    @abc.abstractmethod
    def get_clientcert(self, system, username, cli_value, config, interactive):
        """Get a client certificate from keyring.

        :param str system: Package index URL
        :param str username: Known username
        :param str cli_value: Value obtained from the CLI arguments
        :param dict config: Existing configuration from pypirc
        :param bool interactive: Should this operations accept user input?
        """
