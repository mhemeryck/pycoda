# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os import linesep
from unittest import TestCase

from pycoda.codafile import CodaFile
from pycoda.tests.test_records import (InitialRecordTest, OldBalanceRecordTest,
                                       TransactionRecordTest, FinalRecordTest,
                                       NewBalanceRecordTest)


class CodaFileTest(TestCase):
    """Build a minimum test from previous record tests"""
    def setUp(self):
        self.lines = (
            InitialRecordTest.RAW,
            OldBalanceRecordTest.RAW,
            TransactionRecordTest.RAW,
            NewBalanceRecordTest.RAW,
            FinalRecordTest.RAW,
        )
        self.sep = linesep
        self.string = self.sep.join(self.lines)
        self.coda = CodaFile()

    def test_loads_from_dumps(self):
        self.coda.loads(self.string)
        assert self.coda.dumps() == self.string
