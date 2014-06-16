#!/usr/bin/env python
from __future__ import unicode_literals
import csv
import os

import click
import sqlalchemy
from sqlalchemy import Table, Column, MetaData, Integer, Unicode, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


__version__ = '0.0.1'


class Coblr(object):

    def __init__(self, database_name, schema_directory):
        self.database_name = database_name
        self.schema_directory = schema_directory
        self.schema = Schema(
            self.construct_schema_from_filesystem(schema_directory)
        )
        self.engine = None
        self.metadata = None
        self.tables = {}

    def create_database(self):
        engine =  create_engine('postgresql+psycopg2://localhost:5432')
        session = sessionmaker(bind=engine)()
        session.connection().connection.set_isolation_level(0)
        session.execute('CREATE DATABASE {}'.format(self.database_name))
        session.connection().connection.set_isolation_level(1)

    def materialize_schema(self):
        self.engine =  create_engine(
            'postgresql+psycopg2://localhost:5432/{}'.format(self.database_name)
        )
        self.metadata = MetaData()
        for table in self.schema.tables:
            t = Table(table.name,
                      self.metadata,
                      *[Column(c, Unicode) for c in table.columns])
            self.tables[table.name] = t
        self.metadata.create_all(self.engine)

    def load_data(self):
        for table in self.schema.tables:
            for file_path in table.files:
                with open(file_path, 'cU') as fo:
                    records = list(csv.DictReader(fo))
                self.engine.execute(self.tables[table.name].insert(records))
                
    def construct_schema_from_filesystem(self, schema_path):
        namespaces = os.listdir(schema_path)
        schema_dict = {
            ns: {
                table: {
                    'files': map(
                            lambda x: os.path.abspath(os.path.join(schema_path, ns, table, x)),
                            os.listdir(os.path.join(schema_path, ns, table))
                    ),
                    'columns': self.column_schema(
                        map(
                            lambda x: os.path.abspath(os.path.join(schema_path, ns, table, x)),
                            os.listdir(os.path.join(schema_path, ns, table))
                        )
                        ),
                }
                for table in os.listdir(os.path.join(schema_path, ns))
            }
            for ns in namespaces
        }
        return schema_dict

    def column_schema(self, files):
        starting_columns = []
        for file_path in files:
            with open(file_path, 'cU') as fo:
                reader = csv.DictReader(fo)
                columns = reader.next().keys()
                if not starting_columns:
                    starting_columns = columns
                else:
                    if starting_columns != columns:
                        raise Exception(
                            'The column schemas are inconsistent for {}'
                            .format(files)
                        )
        return columns


class Schema(object):

    class Table(object):
        def __init__(self, name, columns, files):
            self.name = name
            self.columns = columns
            self.files = files
            
    def __init__(self, dikt):
        self.dikt = dikt
        table_params = [
            ('{}.{}'.format(ns, table),
             dikt[ns][table]['columns'],
             dikt[ns][table]['files'])
            for ns in dikt for table in dikt[ns]
        ]
        self.tables = [
            self.Table(name, columns, files)
            for name, columns, files in table_params
        ]


@click.group()
def cli():
    pass


@cli.command()
@click.argument('database_name')
@click.argument('schema_directory')
def cobble(database_name, schema_directory):
    coblr = Coblr(database_name, schema_directory)
    coblr.create_database()
    coblr.materialize_schema()
    coblr.load_data()


if __name__ == '__main__':
    cli()
