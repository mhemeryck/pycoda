# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

from pycoda.fields import (NumericField, StringField, ZeroesField, DateField, EmptyField)


class StringFieldTest(TestCase):
    def test_dumps(self):
        field = StringField(0, 3, value='foo')
        assert field.dumps() == 'foo'

    def test_loads(self):
        field = StringField(0, 3)
        field.loads('foo')
        assert field.value == 'foo'

    def test_loads_dumps(self):
        field = StringField(0, 3)
        field.loads('foo')
        assert field.dumps() == 'foo'

    def test_loads_from_dumps(self):
        field = StringField(0, 3, value='foo')
        field.loads(field.dumps())
        assert field.value == 'foo'

    def test_new_field_from_dumps(self):
        field = StringField(0, 3, value='foo')
        new_field = StringField(0, 3, field.dumps())
        assert new_field.value == 'foo'

    def test_init_length_shorter_than_value(self):
        field = StringField(0, 2, value='foo')
        assert field.value == 'foo'

    def test_init_length_longer_than_value(self):
        field = StringField(0, 4, value='foo')
        assert field.value == 'foo'

    def test_init_empty_value(self):
        field = StringField(0, 1, value=' ')
        assert field.value == ' '

    def test_init_leading_space(self):
        field = StringField(0, 4, value=' foo')
        assert field.value == ' foo'

    def test_init_trailing_space(self):
        field = StringField(0, 4, value='foo ')
        assert field.value == 'foo '

    def test_loads_length_shorter_than_value(self):
        field = StringField(0, 2)
        with self.assertRaises(ValueError):
            field.loads('foo')

    def test_loads_length_longer_than_value(self):
        field = StringField(0, 4)
        with self.assertRaises(ValueError):
            field.loads('foo')

    def test_loads_empty_string(self):
        field = StringField(0, 1)
        field.loads(' ')
        assert field.value == ' '

    def test_loads_leading_space(self):
        field = StringField(0, 4)
        field.loads(' foo')
        assert field.value == ' foo'

    def test_loads_trailing_space(self):
        field = StringField(0, 4)
        field.loads('foo ')
        assert field.value == 'foo '

    def test_loads_with_spaces(self):
        field = StringField(0, 11)
        field.loads('foo bar qux')
        assert field.value == 'foo bar qux'

    def test_dumps_length_shorter_than_value(self):
        field = StringField(0, 2, value='foo')
        assert field.dumps() == 'fo'

    def test_dumps_length_longer_than_value(self):
        field = StringField(0, 4, value='foo')
        assert field.dumps() == 'foo '

    def test_dumps_empty_string(self):
        field = StringField(0, 1, value=' ')
        assert field.dumps() == ' '

    def test_dumps_empty_value(   self):
        field = StringField(0, 3)
        assert field.dumps() == '   '

    def test_dumps_leading_space(self):
        field = StringField(0, 4, value=' foo')
        assert field.dumps() == ' foo'

    def test_dumps_trailing_space(self):
        field = StringField(0, 4, value= 'foo ')
        assert field.dumps() == 'foo '

    def test_dumps_init_none_value(self):
        field = StringField(0, 3)
        assert field.dumps() == '   '

    def test_dumps_align_left(self):
        field = StringField(0, 4, value='foo', pad=' ', align='<')
        assert field.dumps() == 'foo '

    def test_dumps_align_right(self):
        field = StringField(0, 4, value='foo', pad=' ', align='>')
        assert field.dumps() == ' foo'

    def test_dumps_align_left_pad_zero(self):
        field = StringField(0, 6, value='foo', pad='0', align='<')
        assert field.dumps() == 'foo000'

    def test_dumps_align_right_pad_zero(self):
        field = StringField(0, 6, value='foo', pad='0', align='>')
        assert field.dumps() == '000foo'

    def test_dumps_pad_zero(self):
        field = StringField(0, 3, pad=0)
        assert field.dumps() == '000'


class EmptyFieldTest(TestCase):
    def test_loads(self):
        field = EmptyField(0, 4)
        field.loads('    ')
        assert field.value == '    '

    def test_dumps(self):
        field = EmptyField(0, 4)
        assert field.dumps() == '    '

    def test_load_from_dumps(self):
        field = EmptyField(0, 4)
        field.loads(field.dumps())
        assert field.value == '    '


class ZeroesFieldTest(TestCase):
    def test_loads(self):
        field = ZeroesField(0, 3)
        field.loads('000')
        assert field.value == '000'

    def test_dumps(self):
        field = ZeroesField(0, 10)
        assert field.dumps() == '0' * 10

    def test_loads_from_dumps(self):
        field = StringField(0, 3)
        field.loads(field.dumps())
        assert field.value == '   '


class NumericFieldTest(TestCase):
    def test_dumps_length_value_equal(self):
        field = NumericField(0, 1, value=1)
        assert field.dumps() == '1'

    def test_dumps_length_longer_than_value(self):
        field = NumericField(0, 2, value=1)
        assert field.dumps() == '1 '

    def test_dumps_length_shorter_than_value(self):
        field = NumericField(0, 1, value=12)
        assert field.dumps() == '1'

    def test_loads_length_string_equal(self):
        field = NumericField(0, 10)
        field.loads('1234567890')
        assert field.value == 1234567890

    def test_loads_length_longer_than_string(self):
        field = NumericField(0, 2)
        with self.assertRaises(ValueError):
            field.loads('1')

    def test_loads_trailing_space(self):
        field = NumericField(0, 2)
        field.loads('1 ')
        assert field.value == 1

    def test_loads_leading_space(self):
        field = NumericField(0, 2)
        field.loads(' 1')
        assert field.value == 1

    def test_loads_length_shorter_than_string(self):
        field = NumericField(0, 1)
        with self.assertRaises(ValueError):
            field.loads('11')

    def test_loads_dumps_equal_same_length(self):
        field = NumericField(0, 10)
        field.loads('9876543210')
        assert field.dumps() == '9876543210'

    def test_loads_dumps_equal_shorter(self):
        field = NumericField(0, 10)
        field.loads('12345     ')
        assert field.dumps() == '12345     '

    def test_loads_from_dumps(self):
        field = NumericField(0, 6, value=123)
        field.loads(field.dumps())
        assert field.value == 123

    def test_loads_leading_head(self):
        field = NumericField(0, 6, head='abc')
        field.loads('abc' + '123')
        assert field.value == 123

    def test_loads_trailing_tail(self):
        field = NumericField(0, 6, tail='abc')
        field.loads('123' + 'abc')
        assert field.value == 123

    def test_loads_leading_head_and_trailing_tail(self):
        field = NumericField(0, 12, head='000', tail='QWERTY')
        field.loads('000123QWERTY')
        assert field.value == 123

    def test_dumps_leading_head(self):
        field = NumericField(0, 6, value=456, head='lol')
        assert field.dumps() == 'lol456'

    def test_dumps_trailing_tail(self):
        field = NumericField(0, 6, value=456, tail='lol')
        assert field.dumps() == '456lol'

    def test_dumps_leading_head_trailing_tail(self):
        field = NumericField(0, 16, value=12357, head='asddfg', tail='zxcvb')
        assert field.dumps() == 'asddfg12357zxcvb'

    def test_loads_head_align_pad(self):
        field = NumericField(0, 11, head='0', pad='0', align='>')
        field.loads('00886946917')
        assert field.value == 886946917

    def test_loads_dumps_head_align_pad(self):
        field = NumericField(0, 11, head='0', pad='0', align='>')
        field.loads('00886946917')
        assert field.dumps() == '00886946917'

