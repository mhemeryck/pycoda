# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from factory import Factory, fuzzy
from factory.faker import Faker

from pycoda.records import InitialRecord


class InitialRecordFactory(Factory):
    class Meta:
        model = InitialRecord

    creation_date = fuzzy.FuzzyDate(date(2000, 1, 1))
    bank_identification_number = fuzzy.FuzzyInteger(999)
    is_duplicate = Faker(b'boolean', chance_of_getting_true=10)
    reference = fuzzy.FuzzyText(length=10)
    addressee = Faker(b'name')
    bic = fuzzy.FuzzyChoice(('KREDBEBB', 'GKCCBEBB', 'BBRUBEBB'))
    account_holder_reference = fuzzy.FuzzyInteger(99999999999)
    free = fuzzy.FuzzyText(length=5)
    transaction_reference = None
    related_reference = None
