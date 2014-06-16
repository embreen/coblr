from __future__ import unicode_literals
from unittest import TestCase

from coblr import Coblr, Schema


class TestCoblr(TestCase):

    def setUp(self):
        self.database_name = 'foodb'
        self.schema_directory = 'schema'
        self.coblr = Coblr(self.database_name, self.schema_directory)

    def test_contruct_schema_from_filesystem(self):
        expected_schema = {
            u'ns1': {
                u'transactions': {
                    u'columns': [
                        'status',
                        'description',
                        'created_at',
                        'funding_instrument_id',
                        'amount',
                        'customer_id',
                        'type',
                        'id'
                    ]
                }
            },
            u'ns2': {
                u'transactions': {
                    u'columns': [
                        'status',
                        'description',
                        'created_at',
                        'funding_instrument_id',
                        'amount',
                        'customer_id',
                        'type',
                        'id']
                }
            }
        }
        result = self.coblr.construct_schema_from_filesystem(self.schema_directory)
        for ns in result:
            for table in result[ns]:
                result[ns][table].pop('files')
        self.assertEqual(result, expected_schema)

    def test_schema_from_dict(self):
        dikt = {
            u'ns1': {
                u'transactions': {
                    u'columns': [
                        'status',
                        'description',
                        'created_at',
                        'funding_instrument_id',
                        'amount',
                        'customer_id',
                        'type',
                        'id'
                    ],
                    u'files': [
                        u'txns1.csv',
                        u'txns2.csv'
                    ]
                }
            },
            u'ns2': {
                u'transactions': {
                    u'columns': [
                        'status',
                        'description',
                        'created_at',
                        'funding_instrument_id',
                        'amount',
                        'customer_id',
                        'type',
                        'id'],
                    u'files': [
                        u'txns1.csv',
                        u'txns2.csv'
                    ]
                }
            }
        }
        schema = Schema(dikt)
    
    def test_create_database(self):
        self.coblr.create_database()
