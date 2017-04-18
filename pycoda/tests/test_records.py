# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from unittest import TestCase

from pycoda.records import (InitialRecord, OldBalanceRecord, TransactionRecord,
                            TransactionPurposeRecord, TransactionDetailRecord,
                            InformationRecord, InformationPurposeRecord,
                            InformationDetailRecord, NewBalanceRecord,
                            ExtraMessageRecord, FinalRecord)


class InitialRecordTest(TestCase):
    RAW = ('0000019091672505        00417969  VIKINGCO NV               KRED'
           'BEBB   00886946917 00000                                       2')

    def setUp(self):
        self.record = InitialRecord()

    def test_field_positions_are_consecutive(self):
        field_iterator = zip(self.record._fields[:-1], self.record._fields[1:])
        for field, next_field in field_iterator:
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_raw_record(self):
        self.record.loads(self.RAW)
        assert self.record.dumps() == self.RAW

    def test_creation_date(self):
        self.record.creation_date = date(2017, 3, 28)
        assert self.record.creation_date == date(2017, 3, 28)

    def test_bank_identification_number(self):
        self.record.bank_identification_number = 725
        assert self.record.bank_identification_number == 725

    def test_duplicate_code_true(self):
        self.record.is_duplicate = True
        assert self.record.is_duplicate

    def test_duplicate_code_false(self):
        self.record.is_duplicate = False
        assert not self.record.is_duplicate

    def test_reference(self):
        self.record.reference = '00417969'
        assert self.record.reference == '00417969'

    def test_addressee(self):
        self.record.addressee = 'Unleashed NV'
        assert self.record.addressee == 'Unleashed NV'

    def test_bic(self):
        self.record.bic = 'KREDBEBB'
        assert self.record.bic == 'KREDBEBB'

    def test_account_holder_reference(self):
        self.record.account_holder_reference = '00886946917'
        assert self.record.account_holder_reference == '00886946917'

    def test_free(self):
        self.record.free = '12345'
        assert self.record.free == '12345'

    def test_transaction_reference(self):
        self.record.transaction_reference = 'abc123xyz'
        assert self.record.transaction_reference == 'abc123xyz'

    def test_related_reference(self):
        self.record.related_reference = 'qwerty'
        assert self.record.related_reference == 'qwerty'


class OldBalanceRecordTest(TestCase):
    RAW = ('12256BE02737026917240                  EUR0000005020346650150916'
           'VIKINGCO NV               KBC-Bedrijfsrekening               119')

    def setUp(self):
        self.record = OldBalanceRecord()

    def test_field_positions_are_consecutive(self):
        field_iterator = zip(self.record._fields[:-1], self.record._fields[1:])
        for field, next_field in field_iterator:
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_raw_record(self):
        self.record.loads(self.RAW)
        assert self.record.dumps() == self.RAW


class TransactionRecordTest(TestCase):
    RAW = ('2100010000OL1002OFFASCTOVSOVERS000000000001000018081600150000110'
           '1048573874287                                      18081623001 0')

    def setUp(self):
        self.record = TransactionRecord()

    def test_field_positions_are_consecutive(self):
        field_iterator = zip(self.record._fields[:-1], self.record._fields[1:])
        for field, next_field in field_iterator:
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_raw_record(self):
        self.record.loads(self.RAW)
        assert self.record.dumps() == self.RAW


class TransactionPurposeRecordTest(TestCase):
    RAW = ('2200220000                                                     C'
           '20160903040112-0001F                                         0 0')

    def setUp(self):
        self.record = TransactionPurposeRecord()

    def test_field_positions_are_consecutive(self):
        field_iterator = zip(self.record._fields[:-1], self.record._fields[1:])
        for field, next_field in field_iterator:
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_raw_record(self):
        self.record.loads(self.RAW)
        assert self.record.dumps() == self.RAW


class TransactionDetailRecordTest(TestCase):
    RAW = ('2300230105BEBEBEBEBEBEBEBE                     mvstagingpos20iii'
           'iiiiiiiii Test    1-trtrtrtr                            0    0 1')

    def setUp(self):
        self.record = TransactionDetailRecord()

    def test_field_positions_are_consecutive(self):
        field_iterator = zip(self.record._fields[:-1], self.record._fields[1:])
        for field, next_field in field_iterator:
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_raw_record(self):
        self.record.loads(self.RAW)
        assert self.record.dumps() == self.RAW


class InformationRecordTest(TestCase):
    RAW = ('3100230106AQPJ06455 SDDBCDBCRFN505500001001mvstagingpos20iiiiiii'
           'iiiii Test                                                   0 0')

    def setUp(self):
        self.record = InformationRecord()

    def test_field_positions_are_consecutive(self):
        field_iterator = zip(self.record._fields[:-1], self.record._fields[1:])
        for field, next_field in field_iterator:
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_raw_record(self):
        self.record.loads(self.RAW)
        assert self.record.dumps() == self.RAW


class InformationPurposeRecordTest(TestCase):
    def setUp(self):
        self.record = InformationPurposeRecord()

    def test_field_positions_are_consecutive(self):
        field_iterator = zip(self.record._fields[:-1], self.record._fields[1:])
        for field, next_field in field_iterator:
            assert field.position + field.length == next_field.position


class InformationDetailRecordTest(TestCase):
    def setUp(self):
        self.record = InformationDetailRecord()

    def test_field_positions_are_consecutive(self):
        field_iterator = zip(self.record._fields[:-1], self.record._fields[1:])
        for field, next_field in field_iterator:
            assert field.position + field.length == next_field.position


class NewBalanceRecordTest(TestCase):
    RAW = ('8231BE02737026917240                  EUR0000005973199110180816 '
           '                                                               0')

    def setUp(self):
        self.record = NewBalanceRecord()

    def test_field_positions_are_consecutive(self):
        field_iterator = zip(self.record._fields[:-1], self.record._fields[1:])
        for field, next_field in field_iterator:
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_raw_record(self):
        self.record.loads(self.RAW)
        assert self.record.dumps() == self.RAW


class ExtraMessageRecordTest(TestCase):
    def setUp(self):
        self.record = ExtraMessageRecord()

    def test_field_positions_are_consecutive(self):
        field_iterator = zip(self.record._fields[:-1], self.record._fields[1:])
        for field, next_field in field_iterator:
            assert field.position + field.length == next_field.position


class FinalRecordTest(TestCase):
    RAW = ('9               027972000000000322000000000142995170            '
           '                                                               2')

    def setUp(self):
        self.record = FinalRecord()

    def test_field_positions_are_consecutive(self):
        field_iterator = zip(self.record._fields[:-1], self.record._fields[1:])
        for field, next_field in field_iterator:
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_raw_record(self):
        self.record.loads(self.RAW)
        assert self.record.dumps() == self.RAW
