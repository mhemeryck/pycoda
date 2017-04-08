# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from abc import ABCMeta, abstractmethod
from datetime import datetime

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


class NumericField(StringField):
    def __init__(self, position, length, value=None, tag=None,
                 pad='', align='<', head='', tail=''):
        super(NumericField, self).__init__(position, length,
                                           value=value, tag=tag,
                                           pad=pad, align=align)
        self.head = head
        self.tail = tail

    def _regex(self):
        length = self.length - len(self.head) - len(self.tail)
        return r'^({self.head})?(?P<value>[\d\s]{{{length}}})({self.tail})?$'.format(self=self, length=length)

    def _parse(self, string):
        return super(NumericField, self)._parse(string)

    def dumps(self):
        value = self.value if self.value else 0
        length = self.length - len(self.head) - len(self.tail)
        dump_format = '{value:{self.pad}{self.align}{length}d}'
        value_string = dump_format.format(self=self, value=value, length=length)[:length]
        return '{self.head}{value_string}{self.tail}'.format(self=self, value_string=value_string)

    def loads(self, string):
        self.value = int(self._parse(string))


class DateField(StringField):
    def __init__(self, position, length=6, value=None, tag=None,
                 pad='', align='<', date_format='%d%m%y'):
        super(DateField, self).__init__(position, length, value=value, tag=tag,
                                        pad=pad, align=align)
        self.date_format = date_format

    def _regex(self):
        return r'^(?P<value>\d{{{self.length}}})$'.format(self=self)

    def _parse(self, string):
        return super(DateField, self)._parse(string)

    def dumps(self):
        if self.value is None:
            raise ValueError('No valid date value available')
        dump_format = '{self.value:{self.date_format}}'
        return dump_format.format(self=self)[:self.length]

    def loads(self, string):
        date_string = self._parse(string)
        self.value = datetime.strptime(date_string, self.date_format).date()
