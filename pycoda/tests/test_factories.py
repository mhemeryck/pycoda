from __future__ import unicode_literals

from unittest import TestCase

from pycoda.factories import (
    CodaFileFactory,
    ExtraMessageRecordFactory,
    FinalRecordFactory,
    InformationDetailRecordFactory,
    InformationPurposeRecordFactory,
    InformationRecordFactory,
    InitialRecordFactory,
    NewBalanceRecordFactory,
    OldBalanceRecordFactory,
    TransactionDetailRecordFactory,
    TransactionPurposeRecordFactory,
    TransactionRecordFactory,
)


class InitialRecordFactoryTest(TestCase):
    def setUp(self):
        self.record = InitialRecordFactory()

    def test_loads_from_dumps(self):
        raw = self.record.dumps()
        self.record.loads(raw)
        assert self.record.dumps() == raw


class OldBalanceRecordFactoryTest(TestCase):
    def setUp(self):
        self.record = OldBalanceRecordFactory()

    def test_loads_from_dumps(self):
        raw = self.record.dumps()
        self.record.loads(raw)
        assert self.record.dumps() == raw


class TransactionRecordFactoryTest(TestCase):
    def setUp(self):
        self.record = TransactionRecordFactory()

    def test_loads_from_dumps(self):
        raw = self.record.dumps()
        self.record.loads(raw)
        assert self.record.dumps() == raw


class TransactionPurposeRecordFactoryTest(TestCase):
    def setUp(self):
        self.record = TransactionPurposeRecordFactory()

    def test_loads_from_dumps(self):
        raw = self.record.dumps()
        self.record.loads(raw)
        assert self.record.dumps() == raw


class TransactionDetailRecordFactoryTest(TestCase):
    def setUp(self):
        self.record = TransactionDetailRecordFactory()

    def test_loads_from_dumps(self):
        raw = self.record.dumps()
        self.record.loads(raw)
        assert self.record.dumps() == raw


class InformationRecordFactoryTest(TestCase):
    def setUp(self):
        self.record = InformationRecordFactory()

    def test_loads_from_dumps(self):
        raw = self.record.dumps()
        self.record.loads(raw)
        assert self.record.dumps() == raw


class InformationPurposeRecordFactoryTest(TestCase):
    def setUp(self):
        self.record = InformationPurposeRecordFactory()

    def test_loads_from_dumps(self):
        raw = self.record.dumps()
        self.record.loads(raw)
        assert self.record.dumps() == raw


class InformationDetailRecordFactoryTest(TestCase):
    def setUp(self):
        self.record = InformationDetailRecordFactory()

    def test_loads_from_dumps(self):
        raw = self.record.dumps()
        self.record.loads(raw)
        assert self.record.dumps() == raw


class NewBalanceRecordFactoryTest(TestCase):
    def setUp(self):
        self.record = NewBalanceRecordFactory()

    def test_loads_from_dumps(self):
        raw = self.record.dumps()
        self.record.loads(raw)
        assert self.record.dumps() == raw


class ExtraMessageRecordFactoryTest(TestCase):
    def setUp(self):
        self.record = ExtraMessageRecordFactory()

    def test_loads_from_dumps(self):
        raw = self.record.dumps()
        self.record.loads(raw)
        assert self.record.dumps() == raw


class FinalRecordFactoryTest(TestCase):
    def setUp(self):
        self.record = FinalRecordFactory()

    def test_loads_from_dumps(self):
        raw = self.record.dumps()
        self.record.loads(raw)
        assert self.record.dumps() == raw


class CodaFileFactoryTest(TestCase):
    def setUp(self):
        self.codafile = CodaFileFactory()

    def test_loads_from_dumps(self):
        raw = self.codafile.dumps()
        self.codafile.loads(raw)
        assert self.codafile.dumps() == raw


class CodaFileFactoryDirectDebitTest(TestCase):
    def setUp(self):
        self.codafile = CodaFileFactory(direct_debit=True)

    def test_loads_from_dumps(self):
        raw = self.codafile.dumps()
        self.codafile.loads(raw)
        assert self.codafile.dumps() == raw
