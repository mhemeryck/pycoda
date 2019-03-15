from __future__ import unicode_literals

from os import linesep

from pycoda.records import (
    ExtraMessageRecord,
    FinalRecord,
    InformationDetailRecord,
    InformationPurposeRecord,
    InformationRecord,
    InitialRecord,
    NewBalanceRecord,
    OldBalanceRecord,
    RecordIdentification,
    TransactionDetailRecord,
    TransactionPurposeRecord,
    TransactionRecord,
)

RECORD_TYPES = (
    InitialRecord,
    OldBalanceRecord,
    TransactionRecord,
    TransactionPurposeRecord,
    TransactionDetailRecord,
    InformationRecord,
    InformationPurposeRecord,
    InformationDetailRecord,
    NewBalanceRecord,
    ExtraMessageRecord,
    FinalRecord,
)

record_map = {}
for record_type in RECORD_TYPES:
    record_map[(record_type.IDENTIFICATION, record_type.ARTICLE)] = record_type


class CodaFile(object):
    def __init__(self, records=None):
        self.records = records or []

    def _record_from_header(self, line):
        """Builds record from type, read from first 2 entries on the line"""
        record_id = int(line[0])
        if record_id in (
            RecordIdentification.TRANSACTION,
            RecordIdentification.INFORMATION,
        ):
            article_id = int(line[1])
        else:
            article_id = None
        return record_map.get((record_id, article_id))()

    def loads(self, string, append=False):
        # By default, do not append for a new load
        if not append:
            self.records = []
        for line in string.splitlines():
            record = self._record_from_header(line)
            record.loads(line)
            self.records.append(record)

    def dumps(self, sep=linesep):
        return sep.join(record.dumps() for record in self.records)
