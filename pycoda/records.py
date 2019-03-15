import re

from pycoda.fields import (
    BalanceField,
    BooleanField,
    DateField,
    EmptyField,
    NumericField,
    StringField,
    ZeroesField,
)


class RecordIdentification(object):
    INITIAL = 0
    OLD_BALANCE = 1
    TRANSACTION = 2
    INFORMATION = 3
    EXTRA_MESSAGE = 4
    NEW_BALANCE = 8
    FINAL = 9


class RecordArticle(object):
    DEFAULT = 1
    PURPOSE = 2
    DETAIL = 3


class Record(object):
    IDENTIFICATION = None
    ARTICLE = None

    def __init__(self):
        self._fields = ()

    def __getattr__(self, item):
        """By implementing this, all the fields their values are accessible"""
        field_name = "_{item}_field".format(item=item)
        if field_name not in self.__dict__.keys():
            raise AttributeError("Unknown value")
        return self.__dict__[field_name].value

    def __setattr__(self, key, value):
        """By implementing this, all the fields their values are accessible"""
        field_name = "_{key}_field".format(key=key)
        if field_name in self.__dict__.keys():
            self.__dict__[field_name].value = value
        else:
            super(Record, self).__setattr__(key, value)

    def dumps(self):
        return "".join(field.dumps() for field in self._fields)

    def loads(self, string):
        for field in self._fields:
            field.loads(string[field.position : field.position + field.length])

    def field_dict(self):
        """Dict-like representation of all field values"""
        regex = re.compile(r"^_(?P<name>((\w+)(_)?)+)_field")
        dictionary = {}
        for key, field in self.__dict__.items():
            if field in self._fields:
                match = regex.match(key)
                if match is not None:
                    dictionary[match.group("name")] = field.value
        return dictionary


class InitialRecord(Record):
    IDENTIFICATION = RecordIdentification.INITIAL
    ARTICLE = None
    APPLICATION_CODE = "05"
    VERSION_CODE = 2

    def __init__(
        self,
        creation_date=None,
        bank_identification_number=None,
        is_duplicate=None,
        reference=None,
        addressee=None,
        bic=None,
        account_holder_reference=None,
        free=None,
        transaction_reference=None,
        related_reference=None,
    ):
        super(Record, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=InitialRecord.IDENTIFICATION
        )
        self._zeroes_field = ZeroesField(1, 4)
        self._creation_date_field = DateField(5, 6, value=creation_date)
        self._bank_identification_number_field = NumericField(
            11, 3, value=bank_identification_number
        )
        self._application_code_field = StringField(
            14, 2, value=InitialRecord.APPLICATION_CODE
        )
        self._duplicate_field = BooleanField(
            16, 1, value=is_duplicate, true_value="D", false_value=" "
        )
        self._empty_field0 = EmptyField(17, 7)
        self._reference_field = StringField(24, 10, value=reference)
        self._addressee_field = StringField(34, 26, value=addressee)
        self._bic_field = StringField(60, 11, value=bic)
        self._account_holder_reference_field = NumericField(
            71, 11, value=account_holder_reference, head="0"
        )
        self._empty_field1 = EmptyField(82, 1)
        self._free_field = StringField(83, 5, value=free)
        self._transaction_reference_field = StringField(
            88, 16, value=transaction_reference, tag="20/1"
        )
        self._related_reference_field = StringField(
            104, 16, value=related_reference, tag="21/1"
        )
        self._empty_field2 = EmptyField(120, 7)
        self._version_code_field = NumericField(
            127, 1, value=InitialRecord.VERSION_CODE
        )

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


class OldBalanceRecord(Record):
    IDENTIFICATION = RecordIdentification.OLD_BALANCE
    ARTICLE = None

    def __init__(
        self,
        account_structure=None,
        serial_number=None,
        account_number=None,
        balance_sign=None,
        old_balance=None,
        balance_date=None,
        account_holder_name=None,
        account_description=None,
        bank_statement_serial_number=None,
    ):
        super(OldBalanceRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=OldBalanceRecord.IDENTIFICATION
        )
        self._account_structure_field = NumericField(1, 1, value=account_structure)
        self._serial_number_field = NumericField(2, 3, value=serial_number, tag="28c/1")
        self._account_number_field = StringField(5, 37, value=account_number)
        self._balance_sign_field = NumericField(42, 1, value=balance_sign, tag="60F/1")
        self._old_balance_field = BalanceField(43, value=old_balance, tag="60F/4")
        self._balance_date_field = DateField(58, 6, value=balance_date, tag="60F/2")
        self._account_holder_name_field = StringField(64, 26, value=account_holder_name)
        self._account_description_field = StringField(90, 35, value=account_description)
        self._bank_statement_serial_number_field = NumericField(
            125, 3, value=bank_statement_serial_number
        )

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


class TransactionRecord(Record):
    IDENTIFICATION = RecordIdentification.TRANSACTION
    ARTICLE = RecordArticle.DEFAULT

    def __init__(
        self,
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
        information_sequence=None,
    ):
        super(TransactionRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=TransactionPurposeRecord.IDENTIFICATION
        )
        self._article_field = NumericField(1, 1, value=TransactionRecord.ARTICLE)
        self._serial_number_field = NumericField(2, 4, value=serial_number)
        self._detail_number_field = NumericField(6, 4, value=detail_number)
        self._bank_reference_number_field = StringField(
            10, 21, value=bank_reference_number, tag="61/8"
        )
        self._balance_sign_field = NumericField(31, 1, value=balance_sign, tag="61/3")
        self._balance_field = BalanceField(32, value=balance, tag="61/5")
        self._balance_date_field = DateField(47, 6, value=balance_date, tag="61/1")
        self._transaction_code_field = NumericField(
            53, 8, value=transaction_code, tag="61/6"
        )
        self._reference_type_field = NumericField(61, 1, value=reference_type)
        self._reference_field = StringField(62, 53, value=reference, tag="61/9")
        self._booking_date_field = DateField(115, 6, value=booking_date, tag="61/2")
        self._bank_statement_serial_number_field = NumericField(
            121, 3, value=bank_statement_serial_number, tag="28/c"
        )
        self._globalisation_code_field = NumericField(124, 1, value=globalisation_code)
        self._transaction_sequence_field = BooleanField(
            125, 1, value=transaction_sequence, true_value="1", false_value="0"
        )
        self._empty_field = EmptyField(126, 1)
        self._information_sequence_field = BooleanField(
            127, 1, value=information_sequence, true_value="1", false_value="0"
        )

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


class TransactionPurposeRecord(Record):
    IDENTIFICATION = RecordIdentification.TRANSACTION
    ARTICLE = RecordArticle.PURPOSE

    def __init__(
        self,
        serial_number=None,
        detail_number=None,
        bank_statement=None,
        client_reference=None,
        bic=None,
        purpose_category=None,
        purpose=None,
        transaction_sequence=None,
        information_sequence=None,
    ):
        super(Record, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=TransactionPurposeRecord.IDENTIFICATION
        )
        self._article_field = NumericField(1, 1, value=TransactionPurposeRecord.ARTICLE)
        self._serial_number_field = NumericField(2, 4, value=serial_number)
        self._detail_number_field = NumericField(6, 4, value=detail_number)
        self._bank_statement_field = StringField(10, 53, value=bank_statement)
        self._client_reference_field = StringField(63, 35, value=client_reference)
        self._bic_field = StringField(98, 11, value=bic)
        self._empty_field0 = EmptyField(109, 8)
        self._purpose_category_field = StringField(117, 4, value=purpose_category)
        self._purpose_field = StringField(121, 4, value=purpose)
        self._transaction_sequence_field = BooleanField(
            125, 1, value=transaction_sequence, true_value="1", false_value="0"
        )
        self._empty_field1 = EmptyField(126, 1)
        self._information_sequence_field = BooleanField(
            127, 1, value=information_sequence, true_value="1", false_value="0"
        )

        self._fields = (
            self._identification_field,
            self._article_field,
            self._serial_number_field,
            self._detail_number_field,
            self._bank_statement_field,
            self._client_reference_field,
            self._bic_field,
            self._empty_field0,
            self._purpose_category_field,
            self._purpose_field,
            self._transaction_sequence_field,
            self._empty_field1,
            self._information_sequence_field,
        )


class TransactionDetailRecord(Record):
    IDENTIFICATION = RecordIdentification.TRANSACTION
    ARTICLE = RecordArticle.DETAIL

    def __init__(
        self,
        serial_number=None,
        detail_number=None,
        account_number=None,
        account_holder_name=None,
        description=None,
        information_sequence=None,
    ):
        super(TransactionDetailRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=TransactionDetailRecord.IDENTIFICATION
        )
        self._article_field = NumericField(1, 1, value=TransactionDetailRecord.ARTICLE)
        self._serial_number_field = NumericField(2, 4, value=serial_number)
        self._detail_number_field = NumericField(6, 4, value=detail_number)
        self._account_number_field = StringField(10, 37, value=account_number)
        self._account_holder_name_field = StringField(47, 35, value=account_holder_name)
        self._description_field = StringField(82, 43, value=description)
        self._sequence_code_field = ZeroesField(125, 1)
        self._empty_field = EmptyField(126, 1)
        self._information_sequence_field = BooleanField(
            127, 1, value=information_sequence, true_value="1", false_value="0"
        )

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


class InformationRecord(Record):
    IDENTIFICATION = RecordIdentification.INFORMATION
    ARTICLE = RecordArticle.DEFAULT

    def __init__(
        self,
        serial_number=None,
        detail_number=None,
        reference_number=None,
        transaction_code=None,
        reference_type=None,
        reference=None,
        transaction_sequence=None,
        information_sequence=None,
    ):
        super(InformationRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=InformationRecord.IDENTIFICATION
        )
        self._article_field = NumericField(1, 1, value=InformationRecord.ARTICLE)
        self._serial_number_field = NumericField(2, 4, value=serial_number)
        self._detail_number_field = NumericField(6, 4, value=detail_number)
        self._reference_number_field = StringField(
            10, 21, value=reference_number, tag="61/8"
        )
        self._transaction_code_field = NumericField(
            31, 8, value=transaction_code, tag="61/6"
        )
        self._reference_type_field = NumericField(39, 1, value=reference_type)
        self._reference_field = StringField(40, 73, value=reference, tag="86")
        self._empty_field0 = EmptyField(113, 12)
        self._transaction_sequence_field = BooleanField(
            125, 1, value=transaction_sequence, true_value="1", false_value="0"
        )
        self._empty_field1 = EmptyField(126, 1)
        self._information_sequence_field = BooleanField(
            127, 1, value=information_sequence, true_value="1", false_value="0"
        )

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
            self._information_sequence_field,
        )


class InformationPurposeRecord(Record):
    IDENTIFICATION = RecordIdentification.INFORMATION
    ARTICLE = RecordArticle.PURPOSE

    def __init__(
        self,
        serial_number=None,
        detail_number=None,
        bank_reference_number=None,
        information_sequence0=None,
        information_sequence1=None,
    ):
        super(InformationPurposeRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=InformationPurposeRecord.IDENTIFICATION
        )
        self._article_field = NumericField(1, 1, value=InformationPurposeRecord.ARTICLE)
        self._serial_number_field = NumericField(2, 4, value=serial_number)
        self._detail_number_field = NumericField(6, 4, value=detail_number)
        self._bank_reference_number_field = StringField(
            10, 105, value=bank_reference_number
        )
        self._empty_field0 = EmptyField(115, 10)
        self._information_sequence_field0 = BooleanField(
            125, 1, value=information_sequence0, true_value="1", false_value="0"
        )
        self._empty_field1 = EmptyField(126, 1)
        self._information_sequence_field1 = BooleanField(
            127, 1, value=information_sequence1, true_value="1", false_value="0"
        )

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


class InformationDetailRecord(Record):
    IDENTIFICATION = RecordIdentification.INFORMATION
    ARTICLE = RecordArticle.DETAIL

    def __init__(
        self,
        serial_number=None,
        detail_number=None,
        bank_reference_number=None,
        information_sequence=None,
    ):
        super(InformationDetailRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=InformationPurposeRecord.IDENTIFICATION
        )
        self._article_field = NumericField(1, 1, value=InformationPurposeRecord.ARTICLE)
        self._serial_number_field = NumericField(2, 4, value=serial_number)
        self._detail_number_field = NumericField(6, 4, value=detail_number)
        self._bank_reference_number_field = StringField(
            10, 90, value=bank_reference_number
        )
        self._empty_field0 = EmptyField(100, 25)
        self._sequence_code_field = ZeroesField(125, 1)
        self._empty_field1 = EmptyField(126, 1)
        self._information_sequence_field = BooleanField(
            127, 1, value=information_sequence, true_value="1", false_value="0"
        )

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


class NewBalanceRecord(Record):
    IDENTIFICATION = RecordIdentification.NEW_BALANCE
    ARTICLE = None

    def __init__(
        self,
        serial_number=None,
        account_number=None,
        balance_sign=None,
        new_balance=None,
        balance_date=None,
        sequence=None,
    ):
        super(NewBalanceRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=NewBalanceRecord.IDENTIFICATION
        )
        self._serial_number_field = NumericField(1, 3, value=serial_number, tag="28c/1")
        self._account_number_field = StringField(4, 37, value=account_number)
        self._balance_sign_field = NumericField(41, 1, value=balance_sign, tag="62F/1")
        self._new_balance_field = BalanceField(42, value=new_balance, tag="62F/4")
        self._balance_date_field = DateField(57, 6, value=balance_date, tag="62F/2")
        self._empty_field = EmptyField(63, 64)
        self._sequence_field = BooleanField(
            127, 1, value=sequence, true_value="1", false_value="0"
        )

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


class ExtraMessageRecord(Record):
    IDENTIFICATION = RecordIdentification.EXTRA_MESSAGE
    ARTICLE = None

    def __init__(
        self,
        serial_number=None,
        detail_number=None,
        extra_message=None,
        has_sequence=None,
    ):
        super(ExtraMessageRecord, self).__init__()

        self._identification_field = NumericField(
            0, 1, value=ExtraMessageRecord.IDENTIFICATION
        )
        self._empty_field0 = EmptyField(1, 1)
        self._serial_number_field = NumericField(2, 4, value=serial_number)
        self._detail_number_field = NumericField(6, 4, value=detail_number)
        self._empty_field1 = EmptyField(10, 22)
        self._extra_message_field = StringField(32, 80, value=extra_message)
        self._empty_field2 = EmptyField(112, 15)
        self._sequence_field = BooleanField(
            127, 1, value=has_sequence, true_value="1", false_value="0"
        )

        self._fields = (
            self._identification_field,
            self._empty_field0,
            self._serial_number_field,
            self._detail_number_field,
            self._empty_field1,
            self._extra_message_field,
            self._empty_field2,
            self._sequence_field,
        )


class FinalRecord(Record):
    IDENTIFICATION = RecordIdentification.FINAL
    ARTICLE = None

    def __init__(self, number_records=None, debit=None, credit=None, has_sequence=None):
        super(FinalRecord, self).__init__()

        self._identification_field = NumericField(0, 1, FinalRecord.IDENTIFICATION)
        self._empty_field0 = EmptyField(1, 15)
        self._number_records_field = NumericField(16, 6, value=number_records)
        self._debit_field = BalanceField(22, value=debit)
        self._credit_field = BalanceField(37, value=credit)
        self._empty_field1 = EmptyField(52, 75)
        self._sequence_field = BooleanField(
            127, 1, value=has_sequence, true_value="1", false_value="2"
        )

        self._fields = (
            self._identification_field,
            self._empty_field0,
            self._number_records_field,
            self._debit_field,
            self._credit_field,
            self._empty_field1,
            self._sequence_field,
        )
