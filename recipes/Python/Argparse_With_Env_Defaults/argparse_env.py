#!/usr/bin/env python3
# PEP 3120

# (C) 2019, Pandu POLUAN
# This source code is released to the public domain.
# If your jurisdiction does not recognize the public domain,
# you can choose one of the following licenses:
#   - The Unlicense: https://spdx.org/licenses/Unlicense.html
#   - CC0 Universal: https://spdx.org/licenses/CC0-1.0.html
#   - WTFPL: https://spdx.org/licenses/WTFPL.html
#   - BSD-3-Clause "Revised": https://spdx.org/licenses/BSD-3-Clause.html

import sys
if sys.hexversion < 0x03_06_00_00:
    raise RuntimeError("Only support Python>=3.6!")

import argparse
from argparse import Namespace
from os import environ

from typing import Union, List


class _WantEnvVar:

    def __init__(self, env_var: str, optional: bool):
        self.env_var: str = env_var
        self.optional: bool = optional
        self.action: Union[argparse.Action, None] = None


class ArgumentParserWithEnv(argparse.ArgumentParser):
    """
    ArgumentParser class with Environment Variable as default value source.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_argument(self, *args,
                     env_var: str = None,
                     env_var_optional: bool = False,
                     **kwargs):
        """
        Similar to argparse.ArgumentParser.add_argument, with the addition of the
        env_var parameter.

        Note: The "default" parameter must NOT be set!

        :param env_var: Environment variable name that will supply the default value.
        :param env_var_optional: If true, don't raise KeyError if env_var not set.
        """
        if env_var is not None:
            if 'default' in kwargs:
                raise ValueError('If env_var is set, default must not be set!')
            # Special marker so that we can recognize which arguments need to be
            # retrieved from env var
            _pge = _WantEnvVar(env_var, env_var_optional)
            kwargs['default'] = _pge
        action = super().add_argument(*args, **kwargs)
        if env_var is not None:
            # noinspection PyUnboundLocalVariable
            _pge.action = action
        return action

    @staticmethod
    def _pull_envvar(parsed: Namespace):
        _cls_pge = _WantEnvVar
        for attrib, value in vars(parsed).items():
            # Have to do it this way because argparse.Namespace is NOT iterable
            if not isinstance(value, _cls_pge):
                continue
            assert isinstance(value, _cls_pge)
            action = value.action
            if value.env_var not in environ:
                if value.optional:
                    setattr(parsed, attrib, None)
                    continue
                _optstr = action.option_strings
                raise KeyError(f"Option(s) {_optstr} not specified "
                               f"and env var {value.env_var} is not set!")
            result = environ[value.env_var]
            if action.type is not None:
                result = action.type(result)
            setattr(parsed, action.dest, result)

    def parse_args(self, *args, **kwargs) -> Namespace:
        """
        Similar to argparse.ArgumentParser.parse_args, with the difference:

        If env_var was specified during add_agument, will try to pull the default
        value from the named Environment Variable, raising a KeyError if not found.
        (IF env_var_optional was set to false)
        """
        parsed: Namespace = super().parse_args(*args, **kwargs)
        self._pull_envvar(parsed)
        return parsed

    def parse_known_args(self, *args, **kwargs) -> (Namespace, List[str]):
        """
        Similar to argparse.ArgumentParser.parse_known_args, with the difference:

        If env_var was specified during add_agument, will try to pull the default
        value from the named Environment Variable, raising a KeyError if not found.
        (IF env_var_optional was set to false)
        """
        parsed, unknown_args = super().parse_known_args(*args, **kwargs)
        self._pull_envvar(parsed)
        return parsed, unknown_args
