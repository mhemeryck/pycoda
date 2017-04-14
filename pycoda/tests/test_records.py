# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from unittest import TestCase

from pycoda.records import (InitialRecord, OldBalanceRecord, TransactionRecord, TransactionPurposeRecord,
                            TransactionDetailRecord, InformationRecord)


FAIL_PAYMENT_RAW = """0000019091672505        00417969  VIKINGCO NV               KREDBEBB   00886946917 00000                                       2
12256BE02737026917240                  EUR0000005020346650150916VIKINGCO NV               KBC-Bedrijfsrekening               119
2100220000AQQE12627 BHKDGLGTESC0000000000000460140916105500000                                                     14091625611 0
2200220000                                                     C20160903040112-0001F                                         0 0
2100230105AQPJ06455 SDDBCDBCRFN1000000000022000ddmmyy505500001127ddmmyy310BE02ZZZ0886946917                  M13178ddmmyy25601 0
22000100270U332767051                  Direct Debit payment CLPCLP1-trtrtrtr                                    2MS03        1 0
2300230105BEBEBEBEBEBEBEBE                     mvstagingpos20iiiiiiiiiiii Test    1-trtrtrtr                            0    0 1
3100230106AQPJ06455 SDDBCDBCRFN505500001001mvstagingpos20iiiiiiiiiiii Test                                                   0 0
9               019320000000000482010000000112273820                                                                           2
"""  # nopep8

SUCCESS_PAYMENT_RAW = """0000019091672505        00417969  VIKINGCO NV               KREDBEBB   00886946917 00000                                       2
12256BE02737026917240                  EUR0000005020346650150916VIKINGCO NV               KBC-Bedrijfsrekening               119
2100220000AQQE12627 BHKDGLGTESC0000000000000460140916105500000                                                     14091625611 0
2200220000                                                     C20160903040112-0001F                                         0 0
2100230105AQPJ06455 SDDBCDBCRFN0000000000022000ddmmyy505500001127ddmmyy310BE02ZZZ0886946917                  M13178ddmmyy25601 0
22000100270U332767051                  Direct Debit payment CLPCLP1-trtrtrtr                                                 1 0
2300230105BEBEBEBEBEBEBEBE                     mvstagingpos20iiiiiiiiiiii Test    1-trtrtrtr                            0    0 1
3100230106AQPJ06455 SDDBCDBCRFN505500001001mvstagingpos20iiiiiiiiiiii Test                                                   0 0
9               019320000000000482010000000112273820                                                                           2
"""  # nopep8

SUCCESS_OGM_RAW = """0000019091672505        00417969  VIKINGCO NV               KREDBEBB   00886946917 00000                                       2
12256BE02737026917240                  EUR0000005020346650150916VIKINGCO NV               KBC-Bedrijfsrekening               119
2100220000AQQE12627 BHKDGLGTESC0000000000000460140916105500000                                                     14091625611 0
2200220000                                                     C20160903040112-0001F                                         0 0
2100060000CVYC01435BSCTOBAOVERS0000000000022000ddmmyy001500000+++TTT/TTTT/TTTTT+++                                 ddmmyy26401 0
2200060000                                                                                        KREDBEBB                   1 0
2300060000BE10734024724804                     PEETERS ALEXIA                                                                0 1
3100060001CVYC01435BSCTOBAOVERS001500001001PEETERS ALEXIA                                                                    1 0
9               019320000000000482010000000112273820                                                                           2
"""  # nopep8


class InitialRecordTest(TestCase):
    def test_field_positions_are_consecutive(self):
        record = InitialRecord()
        for field, next_field in zip(record._fields[:-1], record._fields[1:]):
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_success_payment(self):
        record = InitialRecord()
        record.loads(SUCCESS_PAYMENT_RAW[:128])
        assert record.dumps() == SUCCESS_PAYMENT_RAW[:128]

    def test_example_loads_dumps_fail_payment(self):
        record = InitialRecord()
        record.loads(FAIL_PAYMENT_RAW[:128])
        assert record.dumps() == FAIL_PAYMENT_RAW[:128]

    def test_example_loads_dumps_success_ogm(self):
        record = InitialRecord()
        record.loads(SUCCESS_OGM_RAW[:128])
        assert record.dumps() == SUCCESS_OGM_RAW[:128]

    def test_creation_date(self):
        record = InitialRecord(creation_date=date(2017, 3, 28))
        assert record.creation_date() == date(2017, 3, 28)

    def test_bank_identification_number(self):
        record = InitialRecord(bank_identification_number=725)
        assert record.bank_identification_number() == 725

    def test_duplicate_code_true(self):
        record = InitialRecord(duplicate_code='D')
        assert record.is_duplicate()

    def test_duplicate_code_false(self):
        record = InitialRecord(duplicate_code=' ')
        assert not record.is_duplicate()

    def test_reference(self):
        record = InitialRecord(reference='00417969')
        assert record.reference() == '00417969'

    def test_addressee(self):
        record = InitialRecord(addressee='Unleashed NV')
        assert record.addressee() == 'Unleashed NV'

    def test_bic(self):
        record = InitialRecord(bic='KREDBEBB')
        assert record.bic() == 'KREDBEBB'

    def test_account_holder_reference(self):
        record = InitialRecord(account_holder_reference='00886946917')
        assert record.account_holder_reference() == '00886946917'

    def test_free(self):
        record = InitialRecord(free='12345')
        assert record.free() == '12345'

    def test_transaction_reference(self):
        record = InitialRecord(transaction_reference='abc123xyz')
        assert record.transaction_reference() == 'abc123xyz'

    def test_related_reference(self):
        record = InitialRecord(related_reference='qwerty')
        assert record.related_reference() == 'qwerty'


class OldBalanceRecordTest(TestCase):
    def test_field_positions_are_consecutive(self):
        record = OldBalanceRecord()
        for field, next_field in zip(record._fields[:-1], record._fields[1:]):
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_success_payment(self):
        record = OldBalanceRecord()
        record.loads(SUCCESS_PAYMENT_RAW[129:257])
        assert record.dumps() == SUCCESS_PAYMENT_RAW[129:257]

    def test_example_loads_dumps_fail_payment(self):
        record = OldBalanceRecord()
        record.loads(FAIL_PAYMENT_RAW[129:257])
        assert record.dumps() == FAIL_PAYMENT_RAW[129:257]

    def test_example_loads_dumps_success_ogm(self):
        record = OldBalanceRecord()
        record.loads(SUCCESS_OGM_RAW[129:257])
        assert record.dumps() == SUCCESS_OGM_RAW[129:257]


class TransactionRecordTest(TestCase):
    def setUp(self):
        self.record = TransactionRecord()
        self.success_payment_string = SUCCESS_PAYMENT_RAW.splitlines()[2]
        self.fail_payment_string = FAIL_PAYMENT_RAW.splitlines()[2]
        self.success_ogm_string = SUCCESS_OGM_RAW.splitlines()[2]

    def test_field_positions_are_consecutive(self):
        for field, next_field in zip(self.record._fields[:-1], self.record._fields[1:]):
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_success_payment(self):
        self.record.loads(self.success_payment_string)
        assert self.record.dumps() == self.success_payment_string

    def test_example_loads_dumps_fail_payment(self):
        self.record.loads(self.fail_payment_string)
        assert self.record.dumps() == self.fail_payment_string

    def test_example_loads_dumps_success_ogm(self):
        self.record.loads(self.success_ogm_string)
        assert self.record.dumps() == self.success_ogm_string


class TransactionPurposeRecordTest(TestCase):
    def setUp(self):
        self.record = TransactionPurposeRecord()
        self.success_payment_string = SUCCESS_PAYMENT_RAW.splitlines()[3]
        self.fail_payment_string = FAIL_PAYMENT_RAW.splitlines()[3]
        self.success_ogm_string = SUCCESS_OGM_RAW.splitlines()[3]

    def test_field_positions_are_consecutive(self):
        for field, next_field in zip(self.record._fields[:-1], self.record._fields[1:]):
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_success_payment(self):
        self.record.loads(self.success_payment_string)
        assert self.record.dumps() == self.success_payment_string

    def test_example_loads_dumps_fail_payment(self):
        self.record.loads(self.fail_payment_string)
        assert self.record.dumps() == self.fail_payment_string

    def test_example_loads_dumps_success_ogm(self):
        self.record.loads(self.success_ogm_string)
        assert self.record.dumps() == self.success_ogm_string


class TransactionDetailRecordTest(TestCase):
    def setUp(self):
        self.record = TransactionDetailRecord()
        self.success_payment_string = SUCCESS_PAYMENT_RAW.splitlines()[6]
        self.fail_payment_string = FAIL_PAYMENT_RAW.splitlines()[6]
        self.success_ogm_string = SUCCESS_OGM_RAW.splitlines()[6]

    def test_field_positions_are_consecutive(self):
        for field, next_field in zip(self.record._fields[:-1], self.record._fields[1:]):
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_success_payment(self):
        self.record.loads(self.success_payment_string)
        assert self.record.dumps() == self.success_payment_string

    def test_example_loads_dumps_fail_payment(self):
        self.record.loads(self.fail_payment_string)
        assert self.record.dumps() == self.fail_payment_string

    def test_example_loads_dumps_success_ogm(self):
        self.record.loads(self.success_ogm_string)
        assert self.record.dumps() == self.success_ogm_string


class InformationRecordTest(TestCase):
    def setUp(self):
        self.record = InformationRecord()
        self.success_payment_string = SUCCESS_PAYMENT_RAW.splitlines()[7]
        self.fail_payment_string = FAIL_PAYMENT_RAW.splitlines()[7]
        self.success_ogm_string = SUCCESS_OGM_RAW.splitlines()[7]

    def test_field_positions_are_consecutive(self):
        for field, next_field in zip(self.record._fields[:-1], self.record._fields[1:]):
            assert field.position + field.length == next_field.position

    def test_example_loads_dumps_success_payment(self):
        self.record.loads(self.success_payment_string)
        assert self.record.dumps() == self.success_payment_string

    def test_example_loads_dumps_fail_payment(self):
        self.record.loads(self.fail_payment_string)
        assert self.record.dumps() == self.fail_payment_string

    def test_example_loads_dumps_success_ogm(self):
        self.record.loads(self.success_ogm_string)
        assert self.record.dumps() == self.success_ogm_string
