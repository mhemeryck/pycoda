# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from abc import ABCMeta, abstractmethod

from six import with_metaclass


class Field(with_metaclass(ABCMeta, object)):
    def __init__(self, position, length, value=None, tag=None):
        self.position = position
        self.length = length
        self.value = value
        self.tag = tag

    @abstractmethod
    def _regex(self):
        """Regular expression used in loading the value from a string"""

    def _parse(self, string):
        """Find match with regex and return if found"""
        match = re.match(self._regex(), string)
        if match is None:
            raise ValueError('Specified string does not match field regex')
        return match.group('value')

    @abstractmethod
    def dumps(self):
        """Dump the value in the format such it can be picked up elsewhere"""

    @abstractmethod
    def loads(self, string):
        """Parse value from given string, using the field's available regex"""


class StringField(Field):
    def __init__(self, position, length, value=None, tag=None,
                 pad='', align='<'):
        super(StringField, self).__init__(position, length,
                                          value=value, tag=tag)
        self.pad = pad
        self.align = align

    def _regex(self):
        return r'^(?P<value>[\w\s]{{{self.length}}})$'.format(self=self)

    def _parse(self, string):
        return super(StringField, self)._parse(string)

    def dumps(self):
        value = self.value if self.value else ''
        dump_format = '{value:{self.pad}{self.align}{self.length}s}'
        return dump_format.format(self=self, value=value)[:self.length]

    def loads(self, string):
        self.value = self._parse(string)


class EmptyField(StringField):
    def __init__(self, position, length, tag=None):
        super(EmptyField, self).__init__(position, length, value=None, tag=tag)

    def _regex(self):
        return super(EmptyField, self)._regex()

    def _parse(self, string):
        return super(EmptyField, self)._parse(string)

    def dumps(self):
        return super(EmptyField, self).dumps()

    def loads(self, string):
        super(EmptyField, self).loads(string)


class ZeroesField(StringField):
    def __init__(self, position, length, tag=None):
        super(ZeroesField, self).__init__(position, length, tag=tag, pad='0')

    def _regex(self):
        return super(ZeroesField, self)._regex()

    def _parse(self, string):
        return super(ZeroesField, self)._parse(string)

    def dumps(self):
        return super(ZeroesField, self).dumps()

    def loads(self, string):
        super(ZeroesField, self).loads(string)

