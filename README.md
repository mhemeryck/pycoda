# pycoda

[![CI status](https://github.com/mhemeryck/pycoda/actions/workflows/main.yaml/badge.svg)](https://github.com/mhemeryck/pycoda/actions/workflows/main.yaml)
[![Coverage Status](https://coveralls.io/repos/github/mhemeryck/pycoda/badge.svg)](https://coveralls.io/github/mhemeryck/pycoda)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/codapy.svg)](https://badge.fury.io/py/codapy)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Quickstart

Generate a CODA file from a factory:
```python
>>> from pycoda.factories import CodaFileFactory
>>> coda_file = CodaFileFactory()
>>> print coda_file.dumps()
0000029050288805        TWlscjlKSUAnthony Hicks             GKCCBEBB   06141120086                                             2
10000                                     0000000026785942011208                                                             000
2121170000                     0000000700448471091015000000000                                                     15030900000 0
8000                                     0000000000000000160417                                                                0
9               134803000000336605556000000724123462                                                                           2
```

Check the values of the first record:
```python
>>> coda_file.records[0].field_dict()
{'account_holder_reference': 61411200863,
 'addressee': u'Anthony Hicks',
 'application_code': u'05',
 'bank_identification_number': 888,
 'bic': u'GKCCBEBB',
 'creation_date': datetime.date(2002, 5, 29),
 'duplicate': False,
 'empty': None,
 'free': None,
 'identification': 0,
 'reference': u'TWlscjlKSU',
 'related_reference': None,
 'transaction_reference': None,
 'version_code': 2,
 'zeroes': None}
```

Update a named field of the first record:
```python
>>> coda_file.records[0].addressee = u'John Doe'
>>> print coda_file.records[0].dumps()
0000029050288805        TWlscjlKSUJohn Doe                  GKCCBEBB   06141120086                                             2
```

Make a new CODA file object and load the records / fields from the previous object string representation:
```python
>>> plain = coda_file.dumps()
>>> from pycoda.codafile import CodaFile
>>> new_coda = CodaFile()
>>> new_coda.loads(plain)
>>> print new_coda.dumps()
0000029050288805        TWlscjlKSUJohn Doe                  GKCCBEBB   06141120086                                             2
10000                                     0000000026785942011208                                                             000
2121170000                     0000000700448471091015000000000                                                     15030900000 0
8000                                     0000000000000000160417                                                                0
9               134803000000336605556000000724123462                                                                           2
>>> new_coda.dumps() == coda_file.dumps()
True
```

## Model

The following model hierarchy is employed:
  * CODA file: can consist of multiple records of given type
  * Record type: each of the record types hold different specified named fields of given type
  * Field type: the fields hold the actual values. All the parsing / printing footwork is done at this level

For each of those levels, the objects can:
  * loads: set value from string representation
  * dumps: generate string representation from value
