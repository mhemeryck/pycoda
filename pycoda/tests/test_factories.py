# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

from pycoda.factories import InitialRecordFactory


class InitialRecordFactoryTest(TestCase):
    def setUp(self):
        self.record = InitialRecordFactory()

    def test_loads_from_dumps(self):
        raw = self.record.dumps()
        self.record.loads(raw)
        assert self.record.dumps() == raw
