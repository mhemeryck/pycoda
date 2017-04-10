# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pycoda.fields import NumericField, StringField, ZeroesField, DateField, EmptyField, BalanceField


class Record(object):
    def __init__(self):
        self._fields = ()

    def dumps(self):
        return ''.join(field.dumps() for field in self._fields)

    def loads(self, string):
        for field in self._fields:
            field.loads(string[field.position:field.position + field.length])


class InitialRecord(Record):
    RECORD_IDENTIFICATION = 0
    APPLICATION_CODE = '05'
    VERSION_CODE = 2

    def __init__(self,
                 creation_date=None,
                 bank_identification_number=None,
                 duplicate_code=None,
                 reference=None,
                 addressee=None,
                 bic=None,
                 account_holder_reference=None,
                 free=None,
                 transaction_reference=None,
                 related_reference=None,):
        super(Record, self).__init__()

        self._identification_field = NumericField(0, 1, value=InitialRecord.RECORD_IDENTIFICATION)
        self._zeroes_field = ZeroesField(1, 4)
        self._creation_date_field = DateField(5, 6, value=creation_date)
        self._bank_identification_number_field = NumericField(11, 3,
            value=bank_identification_number, pad=0)
        self._application_code_field = StringField(14, 2, value=InitialRecord.APPLICATION_CODE)
        self._duplicate_field = StringField(16, 1, value=duplicate_code)
        self._empty_field0 = EmptyField(17, 7)
        self._reference_field = StringField(24, 10, value=reference)
        self._addressee_field = StringField(34, 26, value=addressee)
        self._bic_field = StringField(60, 11, value=bic)
        self._account_holder_reference_field = NumericField(71, 11, value=account_holder_reference,
                                                            pad='0', align='>', head='0')
        self._empty_field1 = EmptyField(82, 1)
        self._free_field = StringField(83, 5, value=free)
        self._transaction_reference_field = StringField(88, 16,
            value=transaction_reference, tag='20/1')
        self._related_reference_field = StringField(104, 16,
            value=related_reference, tag='21/1')
        self._empty_field2 = EmptyField(120, 7)
        self._version_code_field = NumericField(127, 1, value=InitialRecord.VERSION_CODE)

        self._fields = (
            self._identification_field,
            self._zeroes_field,
            self._creation_date_field,
            self._bank_identification_number_field,
            self._application_code_field,
            self._duplicate_field,
            self._empty_field0,
            self._reference_field,
            self._addressee_field,
            self._bic_field,
            self._account_holder_reference_field,
            self._empty_field1,
            self._free_field,
            self._transaction_reference_field,
            self._related_reference_field,
            self._empty_field2,
            self._version_code_field,
        )

    def dumps(self):
        return super(InitialRecord, self).dumps()

    def loads(self, string):
        super(InitialRecord, self).loads(string)

    def creation_date(self):
        return self._creation_date_field.value

    def bank_identification_number(self):
        return self._bank_identification_number_field.value

    def is_duplicate(self):
        return self._duplicate_field.value == 'D'

    def reference(self):
        return self._reference_field.value

    def addressee(self):
        return self._addressee_field.value

    def bic(self):
        return self._bic_field.value

    def account_holder_reference(self):
        return self._account_holder_reference_field.value

    def free(self):
        return self._free_field.value

    def transaction_reference(self):
        return self._transaction_reference_field.value

    def related_reference(self):
        return self._related_reference_field.value


class OldBalanceRecord(Record):
    RECORD_IDENTIFICATION = 1

    def __init__(self,
                 account_structure=None,
                 serial_number=None,
                 account_number=None,
                 balance_sign=None,
                 old_balance=None,
                 balance_date=None,
                 account_holder_name=None,
                 account_description=None,
                 bank_statement_serial_number=None):
        super(OldBalanceRecord, self).__init__()

        self._identification_field = NumericField(0, 1, value=OldBalanceRecord.RECORD_IDENTIFICATION)
        self._account_structure_field = NumericField(1, 1, value=account_structure)
        self._serial_number_field = NumericField(2, 3, value=serial_number, tag='28c/1')
        self._account_number_field = StringField(5, 37, value=account_number)
        self._balance_sign_field = NumericField(42, 1, value=balance_sign, tag='60F/1')
        self._old_balance_field = BalanceField(43, value=old_balance, tag='60F/4')
        self._balance_date_field = DateField(58, 6, value=balance_date, tag='60F/2')
        self._account_holder_name_field = StringField(64, 26, value=account_holder_name)
        self._account_description_field = StringField(90, 35, value=account_description)
        self._bank_statement_serial_number_field = NumericField(125, 3, value=bank_statement_serial_number,
                                                                pad=0, align='>')
        self._fields = (
            self._identification_field,
            self._account_structure_field,
            self._serial_number_field,
            self._account_number_field,
            self._balance_sign_field,
            self._old_balance_field,
            self._balance_date_field,
            self._account_holder_name_field,
            self._account_description_field,
            self._bank_statement_serial_number_field,
        )

    def dumps(self):
        return super(OldBalanceRecord, self).dumps()

    def loads(self, string):
        super(OldBalanceRecord, self).loads(string)
