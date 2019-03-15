from __future__ import unicode_literals

from datetime import date
from unittest import TestCase

from pycoda.records import (
    ExtraMessageRecord,
    FinalRecord,
    InformationDetailRecord,
    InformationPurposeRecord,
    InformationRecord,
    InitialRecord,
    NewBalanceRecord,
    OldBalanceRecord,
    Record,
    TransactionDetailRecord,
    TransactionPurposeRecord,
    TransactionRecord,
)


class DummyRecordTest(TestCase):
    class DummyRecord(Record):
        def __init__(self):
            super(Record, self).__init__()

            self._dummy = None
            self._fields = (self._dummy,)

    def setUp(self):
        self.record = self.DummyRecord()

    def test_field_dict(self):
        """Check that if a field is set without the suffix `_field`, it does not show up"""
        assert self.record.field_dict() == {}


class InitialRecordTest(TestCase):
    RAW = (
        "0000019091672505        00417969  VIKINGCO NV               KRED"
        "BEBB   00886946917 00000                                       2"
    )

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
        self.record.reference = "00417969"
        assert self.record.reference == "00417969"

    def test_addressee(self):
        self.record.addressee = "Unleashed NV"
        assert self.record.addressee == "Unleashed NV"

    def test_bic(self):
        self.record.bic = "KREDBEBB"
        assert self.record.bic == "KREDBEBB"

    def test_account_holder_reference(self):
        self.record.account_holder_reference = "00886946917"
        assert self.record.account_holder_reference == "00886946917"

    def test_free(self):
        self.record.free = "12345"
        assert self.record.free == "12345"

    def test_transaction_reference(self):
        self.record.transaction_reference = "abc123xyz"
        assert self.record.transaction_reference == "abc123xyz"

    def test_related_reference(self):
        self.record.related_reference = "qwerty"
        assert self.record.related_reference == "qwerty"

    def test_get_unknown_field_value_raises(self):
        with self.assertRaises(AttributeError):
            x = self.record.some_value  # noqa

    def test_set_unknown_field_value_passes(self):
        self.record.some_value = "something wicked"

    def test_field_dict_creation_date(self):
        self.record.creation_date = date(1986, 3, 28)
        assert self.record.field_dict()["creation_date"] == date(1986, 3, 28)

    def test_field_dict_bank_identification_number(self):
        self.record.bank_identification_number = 123
        assert self.record.field_dict()["bank_identification_number"] == 123

    def test_field_dict_application_code(self):
        self.record.application_code = "05"
        assert self.record.field_dict()["application_code"] == "05"

    def test_field_dict_duplicate(self):
        self.record.duplicate = True
        assert self.record.field_dict()["duplicate"]

    def test_field_dict_reference(self):
        self.record.reference = "QWERTY"
        assert self.record.field_dict()["reference"] == "QWERTY"

    def test_field_dict_addressee(self):
        self.record.addressee = "Some guy"
        assert self.record.field_dict()["addressee"] == "Some guy"

    def test_field_dict_bic(self):
        self.record.bic = "KREDBEBB"
        assert self.record.field_dict()["bic"] == "KREDBEBB"

    def test_field_dict_account_holder_reference(self):
        self.record.account_holder_reference = "QWERTY"
        assert self.record.field_dict()["account_holder_reference"] == "QWERTY"

    def test_field_dict_free(self):
        self.record.free = "WILLY"
        assert self.record.field_dict()["free"] == "WILLY"

    def test_field_dict_transaction_reference(self):
        self.record.transaction_reference = "AZERTY"
        assert self.record.field_dict()["transaction_reference"] == "AZERTY"

    def test_field_dict_related_reference(self):
        self.record.related_reference = "DVORAK"
        assert self.record.field_dict()["related_reference"] == "DVORAK"


class OldBalanceRecordTest(TestCase):
    RAW = (
        "12256BE02737026917240                  EUR0000005020346650150916"
        "VIKINGCO NV               KBC-Bedrijfsrekening               119"
    )

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
    RAW = (
        "2100010000OL1002OFFASCTOVSOVERS000000000001000018081600150000110"
        "1048573874287                                      18081623001 0"
    )

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
    RAW = (
        "2200220000                                                     C"
        "20160903040112-0001F                                         0 0"
    )

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
    RAW = (
        "2300230105BEBEBEBEBEBEBEBE                     mvstagingpos20iii"
        "iiiiiiiii Test    1-trtrtrtr                            0    0 1"
    )

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
    RAW = (
        "3100230106AQPJ06455 SDDBCDBCRFN505500001001mvstagingpos20iiiiiii"
        "iiiii Test                                                   0 0"
    )

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
    RAW = (
        "8231BE02737026917240                  EUR0000005973199110180816 "
        "                                                               0"
    )

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
    RAW = (
        "9               027972000000000322000000000142995170            "
        "                                                               2"
    )

    def setUp(self):
        self.record = FinalRecord()

    def test_field_positions_are_consecutive(self):
        field_iterator = zip(self.record._fields[:-1], self.record._fields[1:])
        for field, next_field in field_iterator:
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_raw_record(self):
        self.record.loads(self.RAW)
        assert self.record.dumps() == self.RAW
