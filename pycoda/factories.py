# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from factory import Factory, fuzzy
from factory.faker import Faker

from pycoda.records import (InitialRecord, OldBalanceRecord, TransactionRecord,
                            TransactionPurposeRecord, TransactionDetailRecord,
                            InformationRecord,
                            InformationPurposeRecord, InformationDetailRecord,
                            NewBalanceRecord, ExtraMessageRecord, FinalRecord)


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


class OldBalanceRecordFactory(Factory):
    class Meta:
        model = OldBalanceRecord

    balance_date = fuzzy.FuzzyDate(date(2000, 1, 1))


class TransactionRecordFactory(Factory):
    class Meta:
        model = TransactionRecord

    balance_date = fuzzy.FuzzyDate(date(2000, 1, 1))
    booking_date = fuzzy.FuzzyDate(date(2000, 1, 1))


class TransactionPurposeRecordFactory(Factory):
    class Meta:
        model = TransactionPurposeRecord


class TransactionDetailRecordFactory(Factory):
    class Meta:
        model = TransactionDetailRecord


class InformationRecordFactory(Factory):
    class Meta:
        model = InformationRecord


class InformationPurposeRecordFactory(Factory):
    class Meta:
        model = InformationPurposeRecord


class InformationDetailRecordFactory(Factory):
    class Meta:
        model = InformationDetailRecord


class NewBalanceRecordFactory(Factory):
    class Meta:
        model = NewBalanceRecord

    balance_date = fuzzy.FuzzyDate(date(2000, 1, 1))


class ExtraMessageRecordFactory(Factory):
    class Meta:
        model = ExtraMessageRecord


class FinalRecordFactory(Factory):
    class Meta:
        model = FinalRecord
