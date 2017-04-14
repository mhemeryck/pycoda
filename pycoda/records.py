# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pycoda.fields import (NumericField, StringField, ZeroesField, DateField,
                           EmptyField, BalanceField)


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

        self._identification_field = NumericField(
            0, 1, value=InitialRecord.RECORD_IDENTIFICATION)
        self._zeroes_field = ZeroesField(1, 4)
        self._creation_date_field = DateField(5, 6, value=creation_date)
        self._bank_identification_number_field = NumericField(
            11, 3, value=bank_identification_number, pad=0)
        self._application_code_field = StringField(
            14, 2, value=InitialRecord.APPLICATION_CODE)
        self._duplicate_field = StringField(16, 1, value=duplicate_code)
        self._empty_field0 = EmptyField(17, 7)
        self._reference_field = StringField(24, 10, value=reference)
        self._addressee_field = StringField(34, 26, value=addressee)
        self._bic_field = StringField(60, 11, value=bic)
        self._account_holder_reference_field = NumericField(
            71, 11, value=account_holder_reference,
            pad='0', align='>', head='0')
        self._empty_field1 = EmptyField(82, 1)
        self._free_field = StringField(83, 5, value=free)
        self._transaction_reference_field = StringField(
            88, 16, value=transaction_reference, tag='20/1')
        self._related_reference_field = StringField(
            104, 16, value=related_reference, tag='21/1')
        self._empty_field2 = EmptyField(120, 7)
        self._version_code_field = NumericField(
            127, 1, value=InitialRecord.VERSION_CODE)

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

        self._identification_field = NumericField(
            0, 1, value=OldBalanceRecord.RECORD_IDENTIFICATION)
        self._account_structure_field = NumericField(
            1, 1, value=account_structure)
        self._serial_number_field = NumericField(
            2, 3, value=serial_number, tag='28c/1')
        self._account_number_field = StringField(5, 37, value=account_number)
        self._balance_sign_field = NumericField(
            42, 1, value=balance_sign, tag='60F/1')
        self._old_balance_field = BalanceField(
            43, value=old_balance, tag='60F/4')
        self._balance_date_field = DateField(
            58, 6, value=balance_date, tag='60F/2')
        self._account_holder_name_field = StringField(
            64, 26, value=account_holder_name)
        self._account_description_field = StringField(
            90, 35, value=account_description)
        self._bank_statement_serial_number_field = NumericField(
            125, 3, value=bank_statement_serial_number, pad=0, align='>')

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


class TransactionRecord(Record):
    RECORD_IDENTIFICATION = 2
    RECORD_ARTICLE = 1

    def __init__(self,
                 serial_number=None,
                 detail_number=None,
                 bank_reference_number=None,
                 balance_sign=None,
                 balance=None,
                 balance_date=None,
                 transaction_code=None,
                 reference_type=None,
                 reference=None,
                 booking_date=None,
                 bank_statement_serial_number=None,
                 globalisation_code=None,
                 transaction_sequence=None,
                 information_sequence=None):
        super(TransactionRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=TransactionRecord.RECORD_IDENTIFICATION)
        self._article_field = NumericField(
            1, 1, value=TransactionRecord.RECORD_ARTICLE)
        self._serial_number_field = NumericField(
            2, 4, value=serial_number, pad='0', align='>')
        self._detail_number_field = NumericField(
            6, 4, value=detail_number, pad='0', align='>')
        self._bank_reference_number_field = StringField(
            10, 21, value=bank_reference_number, tag='61/8')
        self._balance_sign_field = NumericField(
            31, 1, value=balance_sign, tag='61/3')
        self._balance_field = BalanceField(32, value=balance, tag='61/5')
        self._balance_date_field = DateField(
            47, 6, value=balance_date, tag='61/1')
        self._transaction_code_field = NumericField(
            53, 8, value=transaction_code, tag='61/6')
        self._reference_type_field = NumericField(61, 1, value=reference_type)
        self._reference_field = StringField(
            62, 53, value=reference, tag='61/9')
        self._booking_date_field = DateField(
            115, 6, value=booking_date, tag='61/2')
        self._bank_statement_serial_number_field = NumericField(
            121, 3, value=bank_statement_serial_number,
            pad=0, align='>', tag='28/c')
        self._globalisation_code_field = NumericField(
            124, 1, value=globalisation_code)
        self._transaction_sequence_field = NumericField(
            125, 1, value=transaction_sequence)
        self._empty_field = EmptyField(126, 1)
        self._information_sequence_field = NumericField(
            127, 1, value=information_sequence)

        self._fields = (
            self._identification_field,
            self._article_field,
            self._serial_number_field,
            self._detail_number_field,
            self._bank_reference_number_field,
            self._balance_sign_field,
            self._balance_field,
            self._balance_date_field,
            self._transaction_code_field,
            self._reference_type_field,
            self._reference_field,
            self._booking_date_field,
            self._bank_statement_serial_number_field,
            self._globalisation_code_field,
            self._transaction_sequence_field,
            self._empty_field,
            self._information_sequence_field,
        )

    def dumps(self):
        return super(TransactionRecord, self).dumps()

    def loads(self, string):
        super(TransactionRecord, self).loads(string)


class TransactionPurposeRecord(Record):
    RECORD_IDENTIFICATION = 2
    RECORD_ARTICLE = 2

    def __init__(self,
                 serial_number=None,
                 detail_number=None,
                 bank_statement=None,
                 client_reference=None,
                 bic=None,
                 purpose_category=None,
                 purpose=None,
                 transaction_sequence=None,
                 information_sequence=None):
        super(Record, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=TransactionPurposeRecord.RECORD_IDENTIFICATION)
        self._article_field = NumericField(
            1, 1, value=TransactionPurposeRecord.RECORD_ARTICLE)
        self._serial_number_field = NumericField(
            2, 4, value=serial_number, pad='0', align='>')
        self._detail_number_field = NumericField(
            6, 4, value=detail_number, pad='0', align='>')
        self._bank_statement_field = StringField(10, 53, value=bank_statement)
        self._client_reference_field = StringField(
            63, 35, value=client_reference)
        self._bic_field = StringField(98, 11, value=bic)
        self._empty_field0 = EmptyField(109, 8)
        self._purpose_catefory_field = StringField(
            117, 4, value=purpose_category)
        self._purpose_field = StringField(121, 4, value=purpose)
        self._transaction_sequence_field = NumericField(
            125, 1, value=transaction_sequence)
        self._empty_field1 = EmptyField(126, 1)
        self._information_sequence_field = NumericField(
            127, 1, value=information_sequence)

        self._fields = (
            self._identification_field,
            self._article_field,
            self._serial_number_field,
            self._detail_number_field,
            self._bank_statement_field,
            self._client_reference_field,
            self._bic_field,
            self._empty_field0,
            self._purpose_catefory_field,
            self._purpose_field,
            self._transaction_sequence_field,
            self._empty_field1,
            self._information_sequence_field,
        )

    def dumps(self):
        return super(TransactionPurposeRecord, self).dumps()

    def loads(self, string):
        super(TransactionPurposeRecord, self).loads(string)


class TransactionDetailRecord(Record):
    RECORD_IDENTIFICATION = 2
    RECORD_ARTICLE = 3

    def __init__(self,
                 serial_number=None,
                 detail_number=None,
                 account_number=None,
                 account_holder_name=None,
                 description=None,
                 information_sequence=None):
        super(TransactionDetailRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=TransactionDetailRecord.RECORD_IDENTIFICATION)
        self._article_field = NumericField(
            1, 1, value=TransactionDetailRecord.RECORD_ARTICLE)
        self._serial_number_field = NumericField(
            2, 4, value=serial_number, pad='0', align='>')
        self._detail_number_field = NumericField(
            6, 4, value=detail_number, pad='0', align='>')
        self._account_number_field = StringField(10, 37, value=account_number)
        self._account_holder_name_field = StringField(
            47, 35, value=account_holder_name)
        self._description_field = StringField(82, 43, value=description)
        self._sequence_code_field = ZeroesField(125, 1)
        self._empty_field = EmptyField(126, 1)
        self._information_sequence_field = NumericField(
            127, 1, value=information_sequence)

        self._fields = (
            self._identification_field,
            self._article_field,
            self._serial_number_field,
            self._detail_number_field,
            self._account_number_field,
            self._account_holder_name_field,
            self._description_field,
            self._sequence_code_field,
            self._empty_field,
            self._information_sequence_field,
        )

        def dumps(self):
            return super(TransactionDetailRecord, self).dumps()

        def loads(self, string):
            super(TransactionDetailRecord, self).loads(string)


class InformationRecord(Record):
    RECORD_IDENTIFICATION = 3
    RECORD_ARTICLE = 1

    def __init__(self,
                 serial_number=None,
                 detail_number=None,
                 reference_number=None,
                 transaction_code=None,
                 reference_type=None,
                 reference=None,
                 transaction_sequence=None,
                 information_sequence=None):
        super(InformationRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=TransactionDetailRecord.RECORD_IDENTIFICATION)
        self._article_field = NumericField(
            1, 1, value=TransactionDetailRecord.RECORD_ARTICLE)
        self._serial_number_field = NumericField(
            2, 4, value=serial_number, pad='0', align='>')
        self._detail_number_field = NumericField(
            6, 4, value=detail_number, pad='0', align='>')
        self._reference_number_field = StringField(
            10, 21, value=reference_number, tag='61/8')
        self._transaction_code_field = NumericField(
            31, 8, value=transaction_code, pad='0', align='>', tag='61/6')
        self._reference_type_field = NumericField(39, 1, value=reference_type)
        self._reference_field = StringField(40, 73, value=reference, tag='86')
        self._empty_field0 = EmptyField(113, 12)
        self._transaction_sequence_field = NumericField(
            125, 1, value=transaction_sequence)
        self._empty_field1 = EmptyField(126, 1)
        self._information_sequence_field = NumericField(
            127, 1, value=information_sequence)

        self._fields = (
            self._identification_field,
            self._article_field,
            self._serial_number_field,
            self._detail_number_field,
            self._reference_number_field,
            self._transaction_code_field,
            self._reference_type_field,
            self._reference_field,
            self._empty_field0,
            self._transaction_sequence_field,
            self._empty_field1,
            self._information_sequence_field
        )

        def dumps(self):
            return super(InformationRecord, self).dumps()

        def loads(self, string):
            super(InformationRecord, self).loads(string)


class InformationPurposeRecord(Record):
    RECORD_IDENTIFICATION = 3
    RECORD_ARTICLE = 2

    def __init__(self,
                 serial_number=None,
                 detail_number=None,
                 bank_reference_number=None,
                 information_sequence0=None,
                 information_sequence1=None):
        super(InformationPurposeRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=InformationPurposeRecord.RECORD_IDENTIFICATION)
        self._article_field = NumericField(
            1, 1, value=InformationPurposeRecord.RECORD_ARTICLE)
        self._serial_number_field = NumericField(
            2, 4, value=serial_number, pad='0', align='>')
        self._detail_number_field = NumericField(
            6, 4, value=detail_number, pad='0', align='>')
        self._bank_reference_number_field = StringField(
            10, 105, value=bank_reference_number)
        self._empty_field0 = EmptyField(115, 10)
        self._information_sequence_field0 = NumericField(
            125, 1, value=information_sequence0)
        self._empty_field1 = EmptyField(126, 1)
        self._information_sequence_field1 = NumericField(
            127, 1, value=information_sequence1)

        self._fields = (
            self._identification_field,
            self._article_field,
            self._serial_number_field,
            self._detail_number_field,
            self._bank_reference_number_field,
            self._empty_field0,
            self._information_sequence_field0,
            self._empty_field1,
            self._information_sequence_field1,
        )

    def dumps(self):
        return super(InformationPurposeRecord, self).dumps()

    def loads(self, string):
        super(InformationPurposeRecord, self).loads(string)


class InformationDetailRecord(Record):
    RECORD_IDENTIFICATION = 3
    RECORD_ARTICLE = 3

    def __init__(self,
                 serial_number=None,
                 detail_number=None,
                 bank_reference_number=None,
                 information_sequence=None):
        super(InformationDetailRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=InformationPurposeRecord.RECORD_IDENTIFICATION)
        self._article_field = NumericField(
            1, 1, value=InformationPurposeRecord.RECORD_ARTICLE)
        self._serial_number_field = NumericField(
            2, 4, value=serial_number, pad='0', align='>')
        self._detail_number_field = NumericField(
            6, 4, value=detail_number, pad='0', align='>')
        self._bank_reference_number_field = StringField(
            10, 90, value=bank_reference_number)
        self._empty_field0 = EmptyField(100, 25)
        self._sequence_code_field = ZeroesField(125, 1)
        self._empty_field1 = EmptyField(126, 1)
        self._information_sequence_field = NumericField(
            127, 1, value=information_sequence)

        self._fields = (
            self._identification_field,
            self._article_field,
            self._serial_number_field,
            self._detail_number_field,
            self._bank_reference_number_field,
            self._empty_field0,
            self._sequence_code_field,
            self._empty_field1,
            self._information_sequence_field,
        )

        def dumps(self):
            return super(InformationDetailRecord, self).dumps()

        def loads(self, string):
            super(InformationDetailRecord, self).loads(string)


class NewBalanceRecord(Record):
    RECORD_IDENTIFICATION = 8

    def __init__(self,
                 serial_number=None,
                 account_number=None,
                 balance_sign=None,
                 new_balance=None,
                 balance_date=None,
                 sequence=None):
        super(NewBalanceRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=NewBalanceRecord.RECORD_IDENTIFICATION)
        self._serial_number_field = NumericField(
            1, 3, value=serial_number, tag='28c/1')
        self._account_number_field = StringField(
            4, 37, value=account_number)
        self._balance_sign_field = NumericField(
            41, 1, value=balance_sign, tag='62F/1')
        self._new_balance_field = BalanceField(
            42, value=new_balance, tag='62F/4')
        self._balance_date_field = DateField(
            57, 6, value=balance_date, tag='62F/2')
        self._empty_field = EmptyField(63, 64)
        self._sequence_field = NumericField(127, 1, value=sequence)

        self._fields = (
            self._identification_field,
            self._serial_number_field,
            self._account_number_field,
            self._balance_sign_field,
            self._new_balance_field,
            self._balance_date_field,
            self._empty_field,
            self._sequence_field,
        )

    def dumps(self):
        return super(NewBalanceRecord, self).dumps()

    def loads(self, string):
        super(NewBalanceRecord, self).loads(string)
