from __future__ import unicode_literals

from datetime import date, datetime
from decimal import Decimal

from factory import Factory, LazyAttribute, LazyFunction, Trait, fuzzy
from factory.faker import Faker

from pycoda.codafile import CodaFile
from pycoda.records import (
    ExtraMessageRecord,
    FinalRecord,
    InformationDetailRecord,
    InformationPurposeRecord,
    InformationRecord,
    InitialRecord,
    NewBalanceRecord,
    OldBalanceRecord,
    TransactionDetailRecord,
    TransactionPurposeRecord,
    TransactionRecord,
)


class InitialRecordFactory(Factory):
    class Meta:
        model = InitialRecord

    creation_date = fuzzy.FuzzyDate(date(2000, 1, 1))
    bank_identification_number = fuzzy.FuzzyInteger(999)
    is_duplicate = Faker("boolean", chance_of_getting_true=10)
    reference = fuzzy.FuzzyText(length=10)
    addressee = Faker("name")
    bic = fuzzy.FuzzyChoice(("KREDBEBB", "GKCCBEBB", "BBRUBEBB"))
    account_holder_reference = fuzzy.FuzzyInteger(99999999999)
    free = None
    transaction_reference = None
    related_reference = None

    class Params:
        direct_debit = Trait(
            bank_identification_number=725,
            reference="00417969",
            addressee="UNLEASHED NV",
            bic="KREDBEBB",
            account_holder_reference=886946917,
            free="00000",
        )


class OldBalanceRecordFactory(Factory):
    class Meta:
        model = OldBalanceRecord

    old_balance = fuzzy.FuzzyDecimal(1e6, precision=3)
    balance_date = fuzzy.FuzzyDate(date(2000, 1, 1))

    class Params:
        direct_debit = Trait(
            account_structure=2,
            serial_number=256,
            account_number="BE02737026917240                  EUR",
            balance_sign=0,
            account_holder_name="UNLEASHED NV",
            account_description="Bedrijfsrekening",
            bank_statement_serial_number=119,
        )


class TransactionRecordFactory(Factory):
    class Meta:
        model = TransactionRecord

    serial_number = fuzzy.FuzzyInteger(1e4 - 1)
    balance = fuzzy.FuzzyDecimal(1e6, precision=3)
    balance_date = fuzzy.FuzzyDate(date(2000, 1, 1))
    booking_date = fuzzy.FuzzyDate(date(2000, 1, 1))

    class Params:
        direct_debit = Trait(
            detail_number=1,
            bank_reference_number="AQQE12627 BHKDGLGTESC",
            balance_sign=1,
            balance=Decimal("15.000"),
            balance_date=LazyFunction(datetime.now),
            transaction_code=350000,
            reference_type=0,
            reference=None,
            booking_date=LazyFunction(datetime.now),
            bank_statement_serial_number=256,
            globalisation_code=1,
            transaction_sequence=True,
            information_sequence=True,
        )


class TransactionPurposeRecordFactory(Factory):
    class Meta:
        model = TransactionPurposeRecord

    serial_number = fuzzy.FuzzyInteger(1e4 - 1)

    class Params:
        collect_file_id = 1234
        direct_debit = Trait(
            detail_number=2,
            client_reference=LazyAttribute(
                lambda o: "C20160903040112-{o.collect_file_id}F".format(o=o)
            ),
            transaction_sequence=True,
            information_sequence=True,
        )


class TransactionDetailRecordFactory(Factory):
    class Meta:
        model = TransactionDetailRecord

    serial_number = fuzzy.FuzzyInteger(1e3 - 1)
    account_holder_name = Faker("name")

    class Params:
        payment_id = 1
        direct_debit = Trait(
            account_number="BE68539007547034",
            description=LazyAttribute(lambda o: "1-{o.payment_id}".format(o=o)),
            serial_number=22,
        )


class InformationRecordFactory(Factory):
    class Meta:
        model = InformationRecord

    class Params:
        direct_debit = Trait(
            detail_number=4,
            information_sequence=False,
            transaction_sequence=False,
            reference="001Martijn",
            reference_number="CVYC01435BSCTOBAOVERS",
            reference_type=1,
            serial_number=22,
            transaction_code=150000,
        )


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

    credit = fuzzy.FuzzyDecimal(1e6, precision=3)
    debit = fuzzy.FuzzyDecimal(1e6, precision=3)
    number_records = fuzzy.FuzzyInteger(1e6 - 1)

    class Params:
        direct_debit = Trait(has_sequence=False)


class CodaFileFactory(Factory):
    class Meta:
        model = CodaFile

    records = [
        InitialRecordFactory(),
        OldBalanceRecordFactory(),
        TransactionRecordFactory(),
        NewBalanceRecordFactory(),
        FinalRecordFactory(),
    ]

    class Params:
        direct_debit = Trait(
            records=[
                InitialRecordFactory(direct_debit=True),
                OldBalanceRecordFactory(direct_debit=True),
                TransactionRecordFactory(direct_debit=True),
                TransactionPurposeRecordFactory(direct_debit=True),
                TransactionDetailRecordFactory(direct_debit=True),
                InformationRecordFactory(direct_debit=True),
                FinalRecordFactory(direct_debit=True),
            ]
        )
