import abc
import datetime
import decimal
import re


class Field(metaclass=abc.ABCMeta):
    def __init__(self, position, length, value=None, tag=None):
        self.position = position
        self.length = length
        self.value = value
        self.tag = tag

    @abc.abstractmethod
    def _regex(self):
        """Regular expression used in loading the value from a string"""

    def _parse(self, string):
        """Find match with regex and return if found"""
        match = re.match(self._regex(), string)
        if match is None:
            raise ValueError(
                "Specified string {} does not match field regex".format(string)
            )
        return match.group("value")

    @abc.abstractmethod
    def dumps(self):
        """Dump the value in the format such it can be picked up elsewhere"""

    @abc.abstractmethod
    def loads(self, string):
        """Parse value from given string, using the field's available regex"""


class StringField(Field):
    def __init__(self, position, length, value=None, tag=None, pad="", align="<"):
        super().__init__(position, length, value=value, tag=tag)
        self.pad = pad
        self.align = align

    def _regex(self):
        return (r"^(?P<value>[\w\s\-\&\.\/\(\)\'\,]{{{self.length}}})$").format(
            self=self
        )

    def _parse(self, string):
        return super()._parse(string)

    def dumps(self):
        value = self.value if self.value else ""
        dump_format = "{value:{self.pad}{self.align}{self.length}s}"
        return dump_format.format(self=self, value=value)[: self.length]

    def loads(self, string):
        self.value = self._parse(string)


class EmptyField(StringField):
    def __init__(self, position, length, tag=None):
        super().__init__(position, length, value=None, tag=tag)

    def _regex(self):
        return super()._regex()

    def _parse(self, string):
        return super()._parse(string)

    def dumps(self):
        return super().dumps()

    def loads(self, string):
        super().loads(string)


class ZeroesField(StringField):
    def __init__(self, position, length, tag=None):
        super().__init__(position, length, tag=tag, pad="0")

    def _regex(self):
        return super()._regex()

    def _parse(self, string):
        return super()._parse(string)

    def dumps(self):
        return super().dumps()

    def loads(self, string):
        super().loads(string)


class NumericField(StringField):
    def __init__(
        self, position, length, value=None, tag=None, pad=0, align=">", head="", tail=""
    ):
        super().__init__(position, length, value=value, tag=tag, pad=pad, align=align)
        self.head = head
        self.tail = tail

    def _regex(self):
        length = self.length - len(self.head) - len(self.tail)
        return (r"^({self.head})?(?P<value>[\d\s]{{{length}}})({self.tail})?$").format(
            self=self, length=length
        )

    def _parse(self, string):
        return super()._parse(string)

    def dumps(self):
        value = self.value if self.value else 0
        length = self.length - len(self.head) - len(self.tail)
        value_string = ("{value:{self.pad}{self.align}{length}d}").format(
            self=self, value=value, length=length
        )
        truncated = value_string[:length]
        return ("{self.head}{truncated}{self.tail}").format(
            self=self, truncated=truncated
        )

    def loads(self, string):
        self.value = int(self._parse(string))


class DateField(StringField):
    def __init__(
        self,
        position,
        length=6,
        value=None,
        tag=None,
        pad="",
        align="<",
        date_format="%d%m%y",
    ):
        super().__init__(position, length, value=value, tag=tag, pad=pad, align=align)
        self.date_format = date_format

    def _regex(self):
        return r"^(?P<value>\d{{{self.length}}})$".format(self=self)

    def _parse(self, string):
        return super()._parse(string)

    def dumps(self):
        if self.value is None:
            raise ValueError("No valid date value available")
        dump_format = "{self.value:{self.date_format}}"
        return dump_format.format(self=self)[: self.length]

    def loads(self, string):
        date_string = self._parse(string)
        self.value = datetime.datetime.strptime(date_string, self.date_format).date()


class BalanceField(Field):
    LENGTH = 15
    DECIMAL_PLACES = 3

    def __init__(self, position, value=None, tag=None, pad="0"):
        super().__init__(position, BalanceField.LENGTH, value=value, tag=tag)
        self.pad = pad

    def _regex(self):
        raise NotImplementedError()

    def _parse(self, string):
        raise NotImplementedError()

    def dumps(self):
        if self.value is None:
            value_tuple = decimal.Decimal(0).as_tuple()
        else:
            value_tuple = self.value.as_tuple()
        shifted = decimal.Decimal((value_tuple.sign, value_tuple.digits, 0))
        dump_format = "{shifted:{self.pad}{self.LENGTH}f}"
        return dump_format.format(self=self, shifted=shifted)

    def loads(self, string):
        parsed = decimal.Decimal(string)
        parsed_tuple = parsed.as_tuple()
        self.value = decimal.Decimal(
            (parsed_tuple.sign, parsed_tuple.digits, -BalanceField.DECIMAL_PLACES)
        )


class BooleanField(StringField):
    def __init__(
        self, position, length, value=False, tag=None, true_value="1", false_value=" "
    ):
        super().__init__(position, length, value=value, tag=tag)
        if len(true_value) != length:
            raise ValueError("true_value has incorrect length")
        self.true_value = true_value
        if len(false_value) != length:
            raise ValueError("false_value has incorrect length")
        self.false_value = false_value

    def _regex(self):
        return super()._regex()

    def _parse(self, string):
        return super()._parse(string)

    def dumps(self):
        if self.value:
            return self.true_value
        else:
            return self.false_value

    def loads(self, string):
        self.value = self._parse(string) == self.true_value
