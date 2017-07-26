#!/usr/bin/env python3
# coding: utf-8


from abc import abstractmethod, ABCMeta
from argparse import Action, ArgumentParser

from yaml import load


class SetDefaultFromFile(Action, metaclass=ABCMeta):
    """
    Populates arguments with file contents.

    This abstract class is to be inherited per type of file read.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        config = self._get_config_from_file(values)
        for key, value in config.items():
            setattr(namespace, key, value)

    @abstractmethod
    def _get_config_from_file(self, filename):
        raise NotImplementedError


class SetDefaultFromYAMLFile(SetDefaultFromFile):
    """
    Populates arguments with a YAML file contents.
    """

    def _get_config_from_file(self, filename):
        with open(filename) as f:
            config = load(f)
        return config


_TEST_FILE = 'test.yaml'
_NAME = 'spam'
_FILE_VALUE = 'eggs'
with open(_TEST_FILE, mode='w') as f:
    f.write('{}: {}'.format(_NAME, _FILE_VALUE))
_PARSER = ArgumentParser()
_PARSER.add_argument('--config', action=SetDefaultFromYAMLFile)
_PARSER.add_argument('--{}'.format(_NAME))


def test_file_content_populates_args():
    args = _PARSER.parse_args('--config {}'.format(_TEST_FILE).split())
    assert getattr(args, _NAME) == _FILE_VALUE


def test_file_content_is_erased_if_arg_given_after():
    expected = '42'
    args = _PARSER.parse_args('--config {} --spam {}'.format(_TEST_FILE,
                                                             expected).split())
    assert getattr(args, _NAME) == expected


def test_arg_is_erases_if_file_is_given_after():
    value = 12
    args = _PARSER.parse_args('--spam {} --config {}'.format(value,
                                                             _TEST_FILE).split())
    assert getattr(args, _NAME) == _FILE_VALUE
