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
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

from functools import partial

from twine import utils
from . import CredentialManager


def _get_value(cli_value, config, key, prompter=None):
    """Get a value from user input.

    :param str cli_value: Value obtained from the CLI arguments
    :param dict config: Existing configuration from pypirc
    :param str key: Key of value in config to use if present
    :param callable prompter: If cli_value is not set and key is
        not present in config, this is called to obtain the value
        (optional)
    """
    if cli_value is not None:
        return cli_value

    config_pass = config.get('password')
    if config_pass:
        return config_pass

    if prompter is not None:
        return prompter()

    return None


class UserInputCredentialManager(CredentialManager):
    """Credential manager to request unknown credentials
    values from the user via command line input.
    """

    @staticmethod
    def get_password(system, username, cli_value, config, interactive):
        """Get a password from user input.

        :param str system: Package index URL
        :param str username: Known username
        :param str cli_value: Value obtained from the CLI arguments
        :param dict config: Existing configuration from pypirc
        :param bool interactive: Should this operations accept user input?
        """
        if interactive:
            prompter = partial(
                utils.get_password,
                'Enter your password: '
            )
        else:
            prompter = None

        return _get_value(
            cli_value,
            config,
            'password',
            prompter
        )

    @staticmethod
    def get_username(system, cli_value, config, interactive):
        """Get a username from user input.

        :param str system: Package index URL
        :param str cli_value: Value obtained from the CLI arguments
        :param dict config: Existing configuration from pypirc
        :param bool interactive: Should this operations accept user input?
        """
        if interactive:
            prompter = partial(
                utils.input_func,
                'Enter your username: '
            )
        else:
            prompter = None

        return _get_value(
            cli_value,
            config,
            'username',
            prompter
        )

    @staticmethod
    def get_cacert(system, username, cli_value, config, interactive):
        """Get a username from user input.

        :param str system: Package index URL
        :param str username: Known username
        :param str cli_value: Value obtained from the CLI arguments
        :param dict config: Existing configuration from pypirc
        :param bool interactive: Should this operations accept user input?
        """
        return _get_value(
            cli_value,
            config,
            'ca_cert'
        )

    @staticmethod
    def get_clientcert(system, username, cli_value, config, interactive):
        """Get a username from user input.

        :param str system: Package index URL
        :param str username: Known username
        :param str cli_value: Value obtained from the CLI arguments
        :param dict config: Existing configuration from pypirc
        :param bool interactive: Should this operations accept user input?
        """
        return _get_value(
            cli_value,
            config,
            'client_cert'
        )
