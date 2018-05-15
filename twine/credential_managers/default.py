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

from . import keyring, user
from .keyring import KeyringCredentialManager
from .user import UserInputCredentialManager


class DefaultCredentialManager(KeyringCredentialManager):
    """Default credential manager.

    This behaves like ``KeyringCredentialManager`` but will
    fall back to user input if the password is not found in keyring.
    """

    @staticmethod
    def get_password(system, username, cli_value, config, interactive):
        """Get a password from keyring.

        :param str system: Package index URL
        :param str username: Known username
        :param str cli_value: Value obtained from the CLI arguments
        :param dict config: Existing configuration from pypirc
        :param bool interactive: Should this operations accept user input?
        """
        password_from_keyring = KeyringCredentialManager.get_password(
            system,
            username,
            cli_value,
            config,
            interactive
        )
        if password_from_keyring is not None:
            return password_from_keyring

        return UserInputCredentialManager.get_password(
            system,
            username,
            cli_value,
            config,
            interactive
        )
