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

